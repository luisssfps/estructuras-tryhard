from typing import Callable, Iterator, Protocol, Self

from src.utils.structures import ListaDoble


class Comparable(Protocol):
    def __lt__(self, _: Self, /) -> bool: ...
    def __le__(self, _: Self, /) -> bool: ...
    def __gt__(self, _: Self, /) -> bool: ...
    def __ge__(self, _: Self, /) -> bool: ...


class NodoArbol[C, V]:
    def __init__(self, clave: C, valor: V) -> None:
        self.clave: C = clave
        self.valor: V = valor
        self.izquierdo: Self | None = None
        self.derecho: Self | None = None


class ArbolBinarioBusqueda[C: Comparable, V]:
    def __init__(self, iter: Iterator[tuple[C, V]] | None = None) -> None:
        self.raiz: NodoArbol[C, V] | None = None
        self.peso = 0

        if iter is None:
            return

        for clave, valor in iter:
            self.insertar(clave, valor)

    def insertar(self, clave: C, valor: V) -> None:
        """Inserta un nuevo nodo en el árbol"""
        if self.raiz is None:
            self.raiz = NodoArbol(clave, valor)
        else:
            self._insertar_recursivo(self.raiz, clave, valor)
        self.peso += 1

    def _insertar_recursivo(self, nodo: NodoArbol[C, V], clave: C, valor: V) -> None:
        """Inserción recursiva en el árbol"""
        if clave < nodo.clave:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, clave, valor)
        elif clave > nodo.clave:
            if nodo.derecho is None:
                nodo.derecho = NodoArbol(clave, valor)
            else:
                self._insertar_recursivo(nodo.derecho, clave, valor)
        else:
            nodo.valor = valor

    def buscar[T](self, clave: C, valor_por_defecto: T = None) -> V | T:
        """Busca un valor por su clave"""
        res = self._buscar_recursivo(self.raiz, clave)
        return res if res is not None else valor_por_defecto

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

    def recorrer_inorden(self) -> Iterator[tuple[C, V]]:
        """Recorrido inorden (izquierda-raíz-derecha)"""
        yield from self._inorden_recursivo(self.raiz)

    def _inorden_recursivo(self, nodo: NodoArbol[C, V] | None) -> Iterator[tuple[C, V]]:
        """Recorrido inorden recursivo"""
        if nodo is not None:
            yield from self._inorden_recursivo(nodo.izquierdo)
            yield nodo.clave, nodo.valor
            yield from self._inorden_recursivo(nodo.derecho)

    def filtrar_por_criterio(self, criterio: Callable[[V], bool]) -> ListaDoble[V]:
        """Filtra elementos del árbol según criterio"""
        resultado: ListaDoble[V] = ListaDoble()
        self._filtrar_recursivo(self.raiz, criterio, ListaDoble())
        return resultado

    def _filtrar_recursivo(
        self,
        nodo: NodoArbol[C, V] | None,
        criterio: Callable[[V], bool],
        resultado: ListaDoble[V],
    ) -> None:
        """Filtrado recursivo"""
        if nodo is not None:
            self._filtrar_recursivo(nodo.izquierdo, criterio, resultado)
            if criterio(nodo.valor):
                resultado.agregar_final(nodo.valor)
            self._filtrar_recursivo(nodo.derecho, criterio, resultado)

    def buscar_por_criterio(self, criterio: Callable[[V], bool]) -> V | None:
        """Buscar elementos del árbol según criterio"""
        return self._buscar_por_criterio_recursivo(self.raiz, criterio)

    def _buscar_por_criterio_recursivo(
        self,
        nodo: NodoArbol[C, V] | None,
        criterio: Callable[[V], bool],
    ) -> V | None:
        """Busqueda recursiva por criterio"""
        if nodo is not None:
            if criterio(nodo.valor):
                return nodo.valor
            return self._buscar_por_criterio_recursivo(
                nodo.izquierdo, criterio
            ) or self._buscar_por_criterio_recursivo(nodo.derecho, criterio)
        return None

    def eliminar(self, clave: C) -> None:
        """Elimina un nodo del árbol por su clave"""
        self.raiz = self._eliminar_recursivo(self.raiz, clave)

    def _eliminar_recursivo(
        self, nodo: NodoArbol[C, V] | None, clave: C
    ) -> NodoArbol[C, V] | None:
        """Eliminación recursiva de un nodo"""
        if nodo is None:
            return None

        # Buscar el nodo a eliminar
        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, clave)
        else:
            self.peso -= 1
            # Caso 1: nodo sin hijos
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: nodo con un solo hijo
            elif nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: nodo con dos hijos
            else:
                sucesor = self._encontrar_minimo(nodo.derecho)
                nodo.clave, nodo.valor = sucesor.clave, sucesor.valor
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.clave)

        return nodo

    def claves(self) -> ListaDoble[C]:
        return ListaDoble(clave for clave, _ in self.recorrer_inorden())

    def valores(self) -> ListaDoble[V]:
        return ListaDoble(valor for _, valor in self.recorrer_inorden())

    def _encontrar_minimo(self, nodo: NodoArbol[C, V]) -> NodoArbol[C, V]:
        """Encuentra el nodo con la clave mínima en un subárbol"""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def __iter__(self) -> Iterator[tuple[C, V]]:
        """Retorna todos los elementos como un iterador"""
        return self.recorrer_inorden()

    def __len__(self) -> int:
        return self.peso

    def __getitem__(self, key: C):
        res = self.buscar(key)
        if res is None:
            raise KeyError(f"No se encuentra la clave:{key}")

        return res

    def __setitem__(self, key: C, value: V):
        self.insertar(key, value)

    def __delitem__(self, key: C):
        self.eliminar(key)

    def __contains__(self, item: C) -> bool:
        return self.buscar(item) is not None
