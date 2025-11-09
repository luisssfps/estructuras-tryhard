class Grafo[T]:
    """
    Grafo no dirigido con pesos
    Usada para: Mapa de la ciudad (zonas y conexiones)
    """

    def __init__(self) -> None:
        self.vertices: dict[T, dict[T, float]] = {}

    def agregar_vertice(self, vertice: T) -> None:
        """Agrega un vértice al grafo"""
        if vertice not in self.vertices:
            self.vertices[vertice] = {}

    def agregar_arista(self, origen: T, destino: T, peso: float) -> None:
        """Agrega una arista bidireccional con peso"""
        if origen not in self.vertices:
            self.agregar_vertice(origen)
        if destino not in self.vertices:
            self.agregar_vertice(destino)

        self.vertices[origen][destino] = peso
        self.vertices[destino][origen] = peso

    def dijkstra(self, origen: T, destino: T) -> tuple[float, list[T]]:
        """
        Algoritmo de Dijkstra para encontrar la ruta más corta
        Retorna: (peso_total, lista_de_vertices)
        """
        if origen not in self.vertices or destino not in self.vertices:
            return (float("inf"), [])

        pesos: dict[T, float] = {v: float("inf") for v in self.vertices}
        pesos[origen] = 0
        anteriores: dict[T, T | None] = {v: None for v in self.vertices}
        sin_visitar = set(self.vertices.keys())

        while sin_visitar:
            actual = min(sin_visitar, key=lambda v: pesos[v])

            if pesos[actual] == float("inf"):
                break

            sin_visitar.remove(actual)

            if actual == destino:
                break

            for vecino, peso in self.vertices[actual].items():
                nuevo_peso = pesos[actual] + peso
                if nuevo_peso < pesos[vecino]:
                    pesos[vecino] = nuevo_peso
                    anteriores[vecino] = actual

        camino: list[T] = []
        actual = destino
        while actual is not None:
            camino.insert(0, actual)
            actual = anteriores[actual]

        if pesos[destino] == float("inf"):
            return (float("inf"), [])

        return (pesos[destino], camino)

    def obtener_vertice_mas_cercana(
        self, origen: T, destinos: list[T]
    ) -> tuple[T, float] | None:
        """
        Encuentra la zona más cercana de una lista de destinos
        Retorna: (vertice, peso) o None
        """
        mejor_vertice: T | None = None
        mejor_peso: float = float("inf")

        for destino in destinos:
            peso, _ = self.dijkstra(origen, destino)
            if peso < mejor_peso:
                mejor_peso = peso
                mejor_vertice = destino

        if mejor_vertice is not None:
            return (mejor_vertice, mejor_peso)
        return None
