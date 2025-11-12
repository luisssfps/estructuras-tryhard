from typing import Iterator
from src.utils.structures import ListaDoble, ArbolBinarioBusqueda, Comparable


class Grafo[T: Comparable]:
    """
    Grafo no dirigido con pesos
    """

    def __init__(self) -> None:
        self.vertices: ArbolBinarioBusqueda[T, ArbolBinarioBusqueda[T, float]] = (
            ArbolBinarioBusqueda()
        )

    def agregar_vertice(self, vertice: T) -> None:
        """Agrega un vértice al grafo"""
        if vertice not in self.vertices:
            self.vertices[vertice] = ArbolBinarioBusqueda()

    def agregar_arista(self, origen: T, destino: T, peso: float) -> None:
        """Agrega una arista bidireccional con peso"""
        conexiones_origen = self.vertices.buscar(origen)
        if conexiones_origen is None:
            self.agregar_vertice(origen)
            conexiones_origen = self.vertices[origen]

        conexiones_destino = self.vertices.buscar(destino)
        if conexiones_destino is None:
            self.agregar_vertice(destino)
            conexiones_destino = self.vertices[destino]

        conexiones_origen[destino] = peso
        conexiones_destino[origen] = peso

    def dijkstra(self, origen: T, destino: T) -> tuple[float, ListaDoble[T]]:
        """
        Algoritmo de Dijkstra para encontrar la ruta más corta
        Retorna: (peso_total, lista_de_vertices)
        """
        if origen not in self.vertices or destino not in self.vertices:
            return (float("inf"), ListaDoble())

        pesos: ArbolBinarioBusqueda[T, float] = ArbolBinarioBusqueda(
            (v, float("inf")) for v in self.vertices.claves()
        )
        pesos[origen] = 0
        anteriores: ArbolBinarioBusqueda[T, T | None] = ArbolBinarioBusqueda(
            (v, None) for v in self.vertices.claves()
        )
        sin_visitar = set(self.vertices.claves())

        while sin_visitar:
            actual = min(sin_visitar, key=lambda v: pesos[v])

            if pesos[actual] == float("inf"):
                break

            sin_visitar.remove(actual)

            if actual == destino:
                break

            vertices_tmp = self.vertices[actual]

            for vecino, peso in vertices_tmp:
                peso_actual = pesos[actual]

                nuevo_peso = peso_actual + peso

                peso_vecino = pesos[vecino]

                if nuevo_peso < peso_vecino:
                    pesos[vecino] = nuevo_peso
                    anteriores[vecino] = actual

                vertices_tmp = self.vertices[actual]

        camino: ListaDoble[T] = ListaDoble()
        actual = destino
        while actual is not None:
            camino.agregar_principio(actual)
            actual = anteriores.buscar(actual)

        peso_destino = pesos[destino]
        if peso_destino == float("inf"):
            return (float("inf"), ListaDoble())

        return (peso_destino, camino)

    def obtener_vertice_mas_cercana(
        self, origen: T, destinos: ListaDoble[T]
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

    def __contains__(self, vertice: T) -> bool:
        "Devuelve si una vertice pertenece al grafo"
        return vertice in self.vertices

    def __iter__(self) -> Iterator[tuple[T, T, float]]:
        for vertice, conexiones in self.vertices:
            for destino, peso in conexiones:
                yield vertice, destino, peso
