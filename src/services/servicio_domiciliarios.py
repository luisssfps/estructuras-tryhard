from src.services.servicio_mapa import ServicioDeMapa
from src.domain import Domiciliario
from src.utils.structures import ArbolBinarioBusqueda, ListaDoble


class ServicioDeDomiciliarios:
    def __init__(self, servicio_mapa: ServicioDeMapa) -> None:
        self.domiciliarios: ArbolBinarioBusqueda[str, Domiciliario] = (
            ArbolBinarioBusqueda()
        )
        self.servicio_mapa: ServicioDeMapa = servicio_mapa

    def registrar_domiciliario(self, nombre: str, zona: str) -> Domiciliario | None:
        """Registra un nuevo domiciliario"""
        if not self.servicio_mapa.zona_en_mapa(zona):
            print(f"✗ La zona '{zona}' no existe en el mapa")
            return

        domiciliario = Domiciliario(nombre, zona)
        self.domiciliarios.insertar(domiciliario.codigo, domiciliario)
        print(f"✓ Domiciliario registrado: {domiciliario}")
        return domiciliario

    def buscar_domiciliario_por_codigo(self, codigo: str) -> Domiciliario | None:
        """Busca un domiciliario por su código"""
        return self.domiciliarios[codigo]

    def listar_domiciliarios(self) -> None:
        """Lista todos los domiciliarios"""
        print("\n=== DOMICILIARIOS REGISTRADOS ===")
        if len(self.domiciliarios) == 0:
            print("No hay domiciliarios registrados")
        else:
            for _, dom in self.domiciliarios:
                print(f"  {dom}")

    def estadisticas_domiciliarios(self) -> None:
        """Muestra estadísticas de los domiciliarios"""
        print("\n=== ESTADÍSTICAS DE DOMICILIARIOS ===")
        domiciliarios = self.domiciliarios.recorrer_inorden()

        for _, dom in domiciliarios:
            estado = "✓ Disponible" if dom.disponible else "✗ Ocupado"
            print(f"\n  {dom.nombre} ({dom.codigo})")
            print(f"    Estado: {estado}")
            print(f"    Ubicación actual: {dom.zona_actual}")
            print(f"    Pedidos entregados: {dom.pedidos_entregados}")

    def obtener_domiciliario_mas_cercano(
        self, zona: str
    ) -> tuple[Domiciliario | None, float]:
        domiciliarios_disponibles = ListaDoble(
            d for _, d in self.domiciliarios if d.disponible
        )

        if domiciliarios_disponibles.esta_vacia():
            print("✗ No hay domiciliarios disponibles")
            return None, 0

        zonas_domiciliarios = ListaDoble(
            d.zona_actual for d in domiciliarios_disponibles
        )
        resultado_dom = self.servicio_mapa.obtener_zona_mas_cercana(
            zona, zonas_domiciliarios
        )

        if resultado_dom is None:
            print("✗ No se encontró domiciliario cercano")
            return None, 0

        zona_dom, distancia_dom = resultado_dom
        domiciliario = self.domiciliarios.buscar_por_criterio(
            lambda d: d.zona_actual == zona_dom and d.disponible
        )

        return domiciliario, distancia_dom
