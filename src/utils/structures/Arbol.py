from typing import Callable, Self


class NodoArbol[C, V]:
    """Nodo para árbol binario de búsqueda"""

    def __init__(self, clave: C, valor: V) -> None:
        self.clave: C = clave
        self.valor: V = valor
        self.izquierdo: Self | None = None
        self.derecho: Self | None = None


class ArbolBinarioBusqueda[C: int, V]:
    """
    Árbol binario de búsqueda
    Usada para: Historial de pedidos ordenados por ID
    """

    def __init__(self) -> None:
        self.raiz: NodoArbol[C, V] | None = None

    def insertar(self, clave: C, valor: V) -> None:
        """Inserta un nuevo nodo en el árbol"""
        if self.raiz is None:
            self.raiz = NodoArbol(clave, valor)
        else:
            self._insertar_recursivo(self.raiz, clave, valor)

    def _insertar_recursivo(self, nodo: NodoArbol[C, V], clave: C, valor: V) -> None:
        """Inserción recursiva en el árbol"""
        if clave < nodo.clave:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, clave, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.derecho, clave, valor)

    def buscar(self, clave: C) -> V | None:
        """Busca un valor por su clave"""
        return self._buscar_recursivo(self.raiz, clave)

    def _buscar_recursivo(self, nodo: NodoArbol[C, V] | None, clave: C) -> V | None:
        """Búsqueda recursiva en el árbol"""
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo.valor
        elif clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierdo, clave)
        else:
            return self._buscar_recursivo(nodo.derecho, clave)

    def recorrer_inorden(self) -> list[tuple[C, V]]:
        """Recorrido inorden (izquierda-raíz-derecha)"""
        resultado: list[tuple[C, V]] = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(
        self, nodo: NodoArbol[C, V] | None, resultado: list[tuple[C, V]]
    ) -> None:
        """Recorrido inorden recursivo"""
        if nodo is not None:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.clave, nodo.valor))
            self._inorden_recursivo(nodo.derecho, resultado)

    def filtrar_por_criterio(self, criterio: Callable[[V], bool]) -> list[V]:
        """Filtra elementos del árbol según criterio"""
        resultado: list[V] = []
        self._filtrar_recursivo(self.raiz, criterio, resultado)
        return resultado

    def _filtrar_recursivo(
        self,
        nodo: NodoArbol[C, V] | None,
        criterio: Callable[[V], bool],
        resultado: list[V],
    ) -> None:
        """Filtrado recursivo"""
        if nodo is not None:
            self._filtrar_recursivo(nodo.izquierdo, criterio, resultado)
            if criterio(nodo.valor):
                resultado.append(nodo.valor)
            self._filtrar_recursivo(nodo.derecho, criterio, resultado)
