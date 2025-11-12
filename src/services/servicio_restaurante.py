from src.services.servicio_mapa import ServicioDeMapa
from src.domain import Restaurante
from src.utils.structures import ArbolBinarioBusqueda, ListaDoble


class ServicioDeRestaurantes:
    def __init__(self, servicio_mapa: ServicioDeMapa) -> None:
        self.servicio_mapa: ServicioDeMapa = servicio_mapa
        self.restaurantes: ArbolBinarioBusqueda[str, Restaurante] = (
            ArbolBinarioBusqueda()
        )

    def registrar_restaurante(self, nombre: str, zona: str) -> Restaurante | None:
        """Registra un nuevo restaurante"""
        if not self.servicio_mapa.zona_en_mapa(zona):
            print(f"✗ La zona '{zona}' no existe en el mapa")
            return

        restaurante = Restaurante(nombre, zona)
        self.restaurantes.insertar(restaurante.codigo, restaurante)
        print(f"✓ Restaurante registrado: {restaurante}")
        return restaurante

    def buscar_restaurante_por_codigo(self, codigo: str) -> Restaurante | None:
        """Busca un restaurante por su código"""
        return self.restaurantes.buscar(codigo)

    def listar_restaurantes(self) -> None:
        """Lista todos los restaurantes con sus menús"""
        print("\n=== RESTAURANTES REGISTRADOS ===")
        if len(self.restaurantes) == 0:
            print("No hay restaurantes registrados")
        else:
            for _, rest in self.restaurantes:
                print(f"\n  {rest}")

    def obtener_restaurante_mas_cercano(
        self, zona: str
    ) -> tuple[Restaurante | None, float]:
        """Obtiene el restaurante más cercano a una zona"""
        zonas_restaurantes = ListaDoble(r.zona for _, r in self.restaurantes)

        resultado = self.servicio_mapa.obtener_zona_mas_cercana(
            zona, zonas_restaurantes
        )

        if resultado is None:
            print("✗ No se encontró restaurante cercano")
            return None, 0

        zona_rest, distancia_rest = resultado

        # Seleccionar restaurante de esa zona
        restaurante = self.restaurantes.buscar(zona_rest)
        return restaurante, distancia_rest
