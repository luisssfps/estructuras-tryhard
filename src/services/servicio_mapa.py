from src.utils.structures import Grafo, ListaDoble


class ServicioDeMapa:
    def __init__(self) -> None:
        self.mapa_ciudad: Grafo[str] = Grafo()

    def agregar_zona(self, zona: str) -> None:
        self.mapa_ciudad.agregar_vertice(zona)

    def agregar_conexion(self, origen: str, destino: str, peso: float) -> None:
        self.mapa_ciudad.agregar_arista(origen, destino, peso)

    def zona_en_mapa(self, zona: str) -> bool:
        return zona in self.mapa_ciudad

    def obtener_zona_mas_cercana(
        self, origen: str, destinos: ListaDoble[str]
    ) -> tuple[str, float] | None:
        return self.mapa_ciudad.obtener_vertice_mas_cercana(origen, destinos)

    def calcular_ruta(self, origen: str, destino: str) -> None:
        """Calcula y muestra la ruta más corta entre dos zonas"""
        if not self.zona_en_mapa(origen):
            print(f"✗ Zona origen '{origen}' no existe")
            return
        if not self.zona_en_mapa(destino):
            print(f"✗ Zona destino '{destino}' no existe")
            return

        peso, camino = self.mapa_ciudad.dijkstra(origen, destino)
        if peso == float("inf"):
            print(f"✗ No se pudo encontrar una ruta desde '{origen}' hacia '{destino}'")
            return

        print(f"\n=== RUTA: {origen} → {destino} ===")
        print(f"  peso total: {peso} km")
        print(f"  Camino: {' → '.join(camino)}")

    def ver_mapa_ciudad(self) -> None:
        """Muestra todas las zonas y sus conexiones"""
        print("\n=== MAPA DE LA CIUDAD ===")
        for zona, destino, peso in self.mapa_ciudad:
            print(f"    {zona} → {destino}: {peso} km")
