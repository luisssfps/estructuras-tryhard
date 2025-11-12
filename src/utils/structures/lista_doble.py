from typing import Callable, Iterator, Self


class NodoDoble[T]:
    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.siguiente: Self | None = None
        self.anterior: Self | None = None


class ListaDoble[T]:
    def __init__(self, iter: Iterator[T] | None = None) -> None:
        self.cabeza: NodoDoble[T] | None = None
        self.cola: NodoDoble[T] | None = None
        self.tamanio_lista: int = 0
        if iter is not None:
            for dato in iter:
                self.agregar_final(dato)

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def agregar_principio(self, dato: T) -> None:
        """Agrega elemento al final"""
        nuevo_nodo = NodoDoble(dato)
        if self.cola is None:
            self.cola = nuevo_nodo
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            assert self.cabeza is not None
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamanio_lista += 1

    def agregar_final(self, dato: T) -> None:
        """Agrega elemento al final"""
        nuevo_nodo = NodoDoble(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            assert self.cola is not None
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamanio_lista += 1

    def eliminar(self, criterio: Callable[[T], bool]) -> T | None:
        """Elimina elemento que cumpla el criterio"""
        actual = self.cabeza
        while actual is not None:
            if criterio(actual.dato):
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente

                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior

                self.tamanio_lista -= 1
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar(self, criterio: Callable[[T], bool]) -> T | None:
        """Busca elemento que cumpla el criterio"""
        actual = self.cabeza
        while actual is not None:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def __iter__(self) -> Iterator[T]:
        """Retorna todos los elementos como un iterador"""
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __len__(self) -> int:
        return self.tamanio_lista

    def __contains__(self, item):
        return self.buscar(lambda x: x == item) is not None
