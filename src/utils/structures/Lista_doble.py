from typing import Callable, Self


class NodoDoble[T]:
    """Nodo para lista doblemente ligada"""

    def __init__(self, dato: T) -> None:
        self.dato: T = dato
        self.siguiente: Self | None = None
        self.anterior: Self | None = None


class ListaDoble[T]:
    """
    Lista doblemente enlazada
    Usada para: Domiciliarios (permite retroceder y avanzar)
    """

    def __init__(self) -> None:
        self.cabeza: NodoDoble[T] | None = None
        self.cola: NodoDoble[T] | None = None
        self.tamanio_lista: int = 0

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

    def eliminar(self, criterio: Callable[[T], bool]) -> bool:
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
                return True
            actual = actual.siguiente
        return False

    def buscar(self, criterio: Callable[[T], bool]) -> T | None:
        """Busca elemento que cumpla el criterio"""
        actual = self.cabeza
        while actual is not None:
            if criterio(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

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
