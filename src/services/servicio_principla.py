from src.domain import (
    Cliente,
    Restaurante,
    Domiciliario,
    Pedido,
    ItemMenu,
)
from src.services import (
    ServicioDeClientes,
    ServicioDeDomiciliarios,
    ServicioDeRestaurantes,
    ServicioDePedidos,
    ServicioDeMapa,
    ServicioDeMenu,
)


class SistemaPedidosDomicilio:
    """
    Sistema principal de gestión de pedidos a domicilio
    Integra todas las estructuras de datos
    """

    def __init__(self) -> None:
        self.servicio_mapa: ServicioDeMapa = ServicioDeMapa()
        self.servicio_menu: ServicioDeMenu = ServicioDeMenu()

        self.servicio_clientes: ServicioDeClientes = ServicioDeClientes(
            self.servicio_mapa
        )
        self.servicio_restaurantes: ServicioDeRestaurantes = ServicioDeRestaurantes(
            self.servicio_mapa
        )
        self.servicio_domiciliarios: ServicioDeDomiciliarios = ServicioDeDomiciliarios(
            self.servicio_mapa
        )

        self.servicio_pedidos: ServicioDePedidos = ServicioDePedidos(
            self.servicio_mapa,
            self.servicio_menu,
            self.servicio_clientes,
            self.servicio_restaurantes,
            self.servicio_domiciliarios,
        )

    # ==================== FUNCIONES DE REGISTRO ====================

    def registrar_cliente(self, nombre: str, zona: str) -> Cliente | None:
        return self.servicio_clientes.registrar_cliente(nombre, zona)

    def registrar_restaurante(self, nombre: str, zona: str) -> Restaurante | None:
        return self.servicio_restaurantes.registrar_restaurante(nombre, zona)

    def registrar_domiciliario(self, nombre: str, zona: str) -> Domiciliario | None:
        return self.servicio_domiciliarios.registrar_domiciliario(nombre, zona)

    def registrar_item_menu(self, nombre: str, categoria: str, precio: float) -> None:
        return self.servicio_menu.registrar_item_menu(nombre, categoria, precio)

    # ==================== FUNCIONES DE CONSULTA ====================

    def buscar_cliente_por_codigo(self, codigo: str) -> Cliente | None:
        return self.servicio_clientes.buscar_cliente_por_codigo(codigo)

    def buscar_restaurante_por_codigo(self, codigo: str) -> Restaurante | None:
        return self.servicio_restaurantes.buscar_restaurante_por_codigo(codigo)

    def buscar_domiciliario_por_codigo(self, codigo: str) -> Domiciliario | None:
        return self.servicio_domiciliarios.buscar_domiciliario_por_codigo(codigo)

    def buscar_item_menu_por_codigo(self, codigo: str) -> ItemMenu | None:
        return self.servicio_menu.buscar_item_menu_por_codigo(codigo)

    def listar_clientes(self) -> None:
        self.servicio_clientes.listar_clientes()

    def listar_restaurantes(self) -> None:
        self.servicio_restaurantes.listar_restaurantes()

    def listar_domiciliarios(self) -> None:
        self.servicio_domiciliarios.listar_domiciliarios()

    def listar_items_menu(self) -> None:
        self.servicio_menu.listar_items_menu()

    # ==================== FUNCIONES DE PEDIDOS ====================

    def crear_pedido(
        self, codigo_cliente: str, items: list[str], prioridad: int = 3
    ) -> Pedido | None:
        return self.servicio_pedidos.crear_pedido(codigo_cliente, items, prioridad)

    def asignar_pedido(self) -> Pedido | None:
        return self.servicio_pedidos.asignar_pedido()

    def entregar_pedido(self, pedido_id: int) -> bool:
        return self.servicio_pedidos.entregar_pedido(pedido_id)

    def cancelar_pedido(self, pedido_id: int) -> bool:
        return self.servicio_pedidos.cancelar_pedido(pedido_id)

    def deshacer_ultima_accion(self) -> bool:
        return self.servicio_pedidos.deshacer_ultima_accion()

    # ==================== FUNCIONES DE VISUALIZACIÓN ====================

    def ver_pedidos_activos(self) -> None:
        self.servicio_pedidos.ver_pedidos_activos()

    def ver_cola_pedidos(self) -> None:
        self.servicio_pedidos.ver_cola_pedidos()

    def ver_historial_acciones(self, ultimas_n: int = 10) -> None:
        self.servicio_pedidos.ver_historial_acciones(ultimas_n)

    def ver_historial_pedidos_completo(self) -> None:
        self.servicio_pedidos.ver_historial_pedidos_completo()

    def ver_historial_por_cliente(self, codigo_cliente: str) -> None:
        self.servicio_pedidos.ver_historial_por_cliente(codigo_cliente)

    def ver_historial_por_zona(self, zona: str) -> None:
        self.servicio_pedidos.ver_historial_por_zona(zona)

    def calcular_ruta(self, origen: str, destino: str) -> None:
        self.servicio_mapa.calcular_ruta(origen, destino)

    def ver_mapa_ciudad(self) -> None:
        self.servicio_mapa.ver_mapa_ciudad()

    def estadisticas_domiciliarios(self) -> None:
        self.servicio_domiciliarios.estadisticas_domiciliarios()
