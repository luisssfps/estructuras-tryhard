from src.services.servicio_mapa import ServicioDeMapa
from src.services.servicio_menu import ServicioDeMenu
from src.services.servicio_clientes import ServicioDeClientes
from src.services.servicio_restaurantes import ServicioDeRestaurantes
from src.services.servicio_domiciliarios import ServicioDeDomiciliarios

from src.domain import Accion, Pedido, TipoAccion, EstadoPedido
from src.utils.structures import Pila, ArbolBinarioBusqueda, ColaPrioridad


class ServicioDePedidos:
    def __init__(
        self,
        servicio_mapa: ServicioDeMapa,
        servicio_menu: ServicioDeMenu,
        servicio_clientes: ServicioDeClientes,
        servicio_restaurantes: ServicioDeRestaurantes,
        servicio_domiciliarios: ServicioDeDomiciliarios,
    ) -> None:
        self.servicio_mapa: ServicioDeMapa = servicio_mapa
        self.servicio_menu: ServicioDeMenu = servicio_menu
        self.servicio_clientes: ServicioDeClientes = servicio_clientes
        self.servicio_restaurantes: ServicioDeRestaurantes = servicio_restaurantes
        self.servicio_domiciliario: ServicioDeDomiciliarios = servicio_domiciliarios

        self.cola_pedidos: ColaPrioridad[Pedido] = ColaPrioridad()
        self.historial_acciones: Pila[Accion] = Pila()
        self.historial_pedidos: ArbolBinarioBusqueda[int, Pedido] = (
            ArbolBinarioBusqueda()
        )
        self.pedidos_activos: ArbolBinarioBusqueda[int, Pedido] = ArbolBinarioBusqueda()

    def crear_pedido(
        self, codigo_cliente: str, codigos_items: list[str], prioridad: int = 3
    ) -> Pedido | None:
        """
        Crea un nuevo pedido
        Prioridad: 1 (urgente) a 5 (normal)
        """
        cliente = self.servicio_clientes.buscar_cliente_por_codigo(codigo_cliente)
        if cliente is None:
            print(f"✗ Cliente {codigo_cliente} no encontrado")
            return None

        pedido = Pedido(cliente)

        for codigo_item in codigos_items:
            item = self.servicio_menu.buscar_item_menu_por_codigo(codigo_item)
            if item is None:
                print(f"✗ Item de menu {codigo_item} no encontrado")
                return None
            pedido.agregar_item(item)

        self.cola_pedidos.encolar(pedido, prioridad)
        self.pedidos_activos[pedido.id] = pedido

        # Registrar acción en historial
        accion = Accion(
            TipoAccion.CREAR_PEDIDO,
            f"Pedido #{pedido.id} creado para {cliente.nombre_completo}",
            pedido.id,
        )
        self.historial_acciones.apilar(accion)

        print(f"✓ Pedido #{pedido.id} creado (Prioridad: {prioridad})")
        print(f"  Cliente: {cliente.nombre_completo} ({cliente.zona})")
        print(f"  Items:\n  {'\n    '.join(str(item) for item in pedido.items_pedido)}")

        return pedido

    def asignar_pedido(self) -> Pedido | None:
        """
        Asigna el siguiente pedido de la cola al restaurante y domiciliario más cercanos
        """
        if self.cola_pedidos.esta_vacia():
            print("✗ No hay pedidos pendientes")
            return None

        pedido = self.cola_pedidos.desencolar()
        assert pedido is not None

        restaurante, distancia_rest = (
            self.servicio_restaurantes.obtener_restaurante_mas_cercano(
                pedido.cliente.zona
            )
        )

        if restaurante is None:
            return None

        pedido.restaurante = restaurante

        # Buscar domiciliario disponible más cercano
        domiciliario, distancia_dom = (
            self.servicio_domiciliario.obtener_domiciliario_mas_cercano(
                restaurante.zona
            )
        )

        if not domiciliario:
            pedido.estado = EstadoPedido.PENDIENTE
            self.cola_pedidos.encolar(pedido, 1)  # Re-encolar con alta prioridad
            return None

        pedido.domiciliario = domiciliario
        domiciliario.disponible = False
        pedido.estado = EstadoPedido.ASIGNADO

        # Registrar acción
        accion = Accion(
            TipoAccion.ASIGNAR_DOMICILIARIO,
            f"Pedido #{pedido.id} asignado a {domiciliario.nombre}",
            pedido.id,
        )
        self.historial_acciones.apilar(accion)

        print(f"\n✓ Pedido #{pedido.id} asignado exitosamente")
        print(f"  Restaurante: {restaurante.nombre} (dist: {distancia_rest} km)")
        print(f"  Domiciliario: {domiciliario.nombre} (dist: {distancia_dom} km)")
        print(f"  Total: ${pedido.total:,.0f}")

        return pedido

    def entregar_pedido(self, pedido_id: int) -> bool:
        """Marca un pedido como entregado"""
        pedido = self.pedidos_activos[pedido_id]

        if pedido is None:
            print(f"✗ Pedido #{pedido_id} no encontrado")
            return False

        if pedido.estado == EstadoPedido.CANCELADO:
            print(f"✗ Pedido #{pedido_id} está cancelado")
            return False

        if pedido.domiciliario is None:
            print(f"✗ Pedido #{pedido_id} no tiene domiciliario asignado")
            return False

        # Actualizar estado
        pedido.estado = EstadoPedido.ENTREGADO
        pedido.domiciliario.disponible = True
        pedido.domiciliario.zona_actual = pedido.cliente.zona
        pedido.domiciliario.pedidos_entregados += 1

        # Guardar en árbol de historial
        self.historial_pedidos.insertar(pedido.id, pedido)

        # Eliminar de pedidos activos
        del self.pedidos_activos[pedido_id]

        # Registrar acción
        accion = Accion(
            TipoAccion.ENTREGAR_PEDIDO,
            f"Pedido #{pedido.id} entregado por {pedido.domiciliario.nombre}",
            pedido.id,
        )
        self.historial_acciones.apilar(accion)

        print(f"✓ Pedido #{pedido_id} entregado exitosamente")
        print(
            f"  Domiciliario {pedido.domiciliario.nombre} ahora en zona {pedido.cliente.zona}"
        )

        return True

    def cancelar_pedido(self, pedido_id: int) -> bool:
        """Cancela un pedido"""
        pedido = self.pedidos_activos[pedido_id]

        if pedido is None:
            print(f"✗ Pedido #{pedido_id} no encontrado o ya finalizado")
            return False

        if pedido.estado == EstadoPedido.ENTREGADO:
            print(f"✗ Pedido #{pedido_id} ya fue entregado, no se puede cancelar")
            return False

        # Liberar domiciliario si estaba asignado
        if pedido.domiciliario is not None:
            pedido.domiciliario.disponible = True

        pedido.estado = EstadoPedido.CANCELADO

        # Guardar en historial
        self.historial_pedidos.insertar(pedido.id, pedido)

        # Eliminar de activos
        del self.pedidos_activos[pedido_id]

        # Registrar acción
        accion = Accion(
            TipoAccion.CANCELAR_PEDIDO, f"Pedido #{pedido.id} cancelado", pedido.id
        )
        self.historial_acciones.apilar(accion)

        print(f"✓ Pedido #{pedido_id} cancelado")
        return True

    def deshacer_ultima_accion(self) -> bool:
        """Deshace la última acción realizada (usando pila)"""
        if self.historial_acciones.esta_vacia():
            print("✗ No hay acciones para deshacer")
            return False

        accion = self.historial_acciones.desapilar()
        print(f"⟲ Deshaciendo: {accion}")

        # Nota: No esta implementado completamente, se agreguará en la versión 2.0 si pagas el pase de batalla :)
        return True

    def ver_pedidos_activos(self) -> None:
        """Muestra todos los pedidos activos"""
        print("\n=== PEDIDOS ACTIVOS ===")
        if len(self.pedidos_activos) == 0:
            print("No hay pedidos activos")
            return

        for _, pedido in self.pedidos_activos:
            print(f"\n  {pedido}")
            print(f"    Zona cliente: {pedido.cliente.zona}")
            if pedido.restaurante:
                print(f"    Zona restaurante: {pedido.restaurante.zona}")
            print(
                f"  Items:\n    {'\n    '.join(str(item) for item in pedido.items_pedido)}"
            )
            print(f"    Total: ${pedido.total:,.0f}")

    def ver_cola_pedidos(self) -> None:
        """Muestra los pedidos en la cola de espera"""
        print("\n=== COLA DE PEDIDOS PENDIENTES ===")
        if self.cola_pedidos.esta_vacia():
            print("La cola está vacía")
            return

        # Mostrar sin desencolar
        for prioridad, pedido in self.cola_pedidos.items:
            print(
                f"  [Prioridad {prioridad}] Pedido #{pedido.id} - {pedido.cliente.nombre_completo}"
            )

    def ver_historial_acciones(self, ultimas_n: int = 10) -> None:
        """Muestra las últimas N acciones del historial"""
        print(f"\n=== ÚLTIMAS {ultimas_n} ACCIONES ===")
        if self.historial_acciones.esta_vacia():
            print("No hay acciones registradas")
            return

        acciones = self.historial_acciones.listar_ultimos_n(ultimas_n)
        for accion in reversed(acciones):
            print(f"  {accion}")

    def ver_historial_pedidos_completo(self) -> None:
        """Muestra todo el historial de pedidos (del árbol)"""
        print("\n=== HISTORIAL COMPLETO DE PEDIDOS ===")
        pedidos = self.historial_pedidos.recorrer_inorden()

        if not pedidos:
            print("No hay pedidos en el historial")
            return

        for _, pedido in pedidos:
            print(f"\n  {pedido}")
            print(f"    Fecha: {pedido.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    Total: ${pedido.total:,.0f}")

    def ver_historial_por_cliente(self, codigo_cliente: str) -> None:
        """Muestra el historial de pedidos de un cliente específico"""
        cliente = self.servicio_clientes.buscar_cliente_por_codigo(codigo_cliente)
        if cliente is None:
            print(f"✗ Cliente {codigo_cliente} no encontrado")
            return

        print(f"\n=== HISTORIAL DE {cliente.nombre_completo} ===")

        pedidos = self.historial_pedidos.filtrar_por_criterio(
            lambda p: p.cliente.codigo == codigo_cliente
        )

        if not pedidos:
            print("Este cliente no tiene pedidos")
            return

        for pedido in pedidos:
            print(f"\n  Pedido #{pedido.id}")
            print(f"    Estado: {pedido.estado.value}")
            print(f"    Fecha: {pedido.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    Total: ${pedido.total:,.0f}")
            if pedido.restaurante:
                print(f"    Restaurante: {pedido.restaurante.nombre}")

    def ver_historial_por_zona(self, zona: str) -> None:
        """Muestra pedidos de una zona específica"""
        if not self.servicio_mapa.zona_en_mapa(zona):
            print(f"✗ La zona '{zona}' no existe")
            return

        print(f"\n=== PEDIDOS EN ZONA: {zona} ===")

        pedidos = self.historial_pedidos.filtrar_por_criterio(
            lambda p: p.cliente.zona == zona
        )

        if len(pedidos) == 0:
            print(f"No hay pedidos en la zona {zona}")
            return

        for pedido in pedidos:
            print(
                f"  Pedido #{pedido.id} - {pedido.cliente.nombre_completo} - {pedido.estado.value}"
            )
