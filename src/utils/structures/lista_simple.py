from typing import Callable, Self


class NodoSimple[T]:
    """Nodo para lista simple"""

    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.siguiente: Self | None = None


class ListaSimple[T]:
    """
    Lista enlazada simple
    Usada para: Registro de clientes
    """

    def __init__(self) -> None:
        self.cabeza: NodoSimple[T] | None = None
        self.tamanio_lista: int = 0

    def agregar_inicio(self, dato: T) -> None:
        """Agrega elemento al inicio"""
        nuevo_nodo = NodoSimple(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamanio_lista += 1

    def agregar_final(self, dato: T) -> None:
        """Agrega elemento al final"""
        nuevo_nodo = NodoSimple(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamanio_lista += 1

    def buscar(self, criterio: Callable[[T], bool]) -> T | None:
        """Busca elemento que cumpla el criterio"""
        actual = self.cabeza
        while actual is not None:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar(self, criterio: Callable[[T], bool]) -> bool:
        """Elimina elemento que cumpla el criterio"""
        if self.cabeza is None:
            return False

        if criterio(self.cabeza.dato):
            self.cabeza = self.cabeza.siguiente
            self.tamanio_lista -= 1
            return True

        actual = self.cabeza
        while actual.siguiente is not None:
            if criterio(actual.siguiente.dato):
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio_lista -= 1
                return True
            actual = actual.siguiente
        return False

    def listar_todos(self) -> list[T]:
        """Retorna todos los elementos como lista"""
        resultado: list[T] = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def tamanio(self) -> int:
        return self.tamanio_lista