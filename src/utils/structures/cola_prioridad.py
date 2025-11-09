class ColaPrioridad[T]:
    """
    Cola con prioridades para pedidos
    Prioridad: 1 (alta) a 5 (baja)
    """

    def __init__(self) -> None:
        self.items: list[tuple[int, T]] = []

    def encolar(self, item: T, prioridad: int = 3) -> None:
        """Agrega elemento con prioridad (1=alta, 5=baja)"""
        self.items.append((prioridad, item))
        self.items.sort(key=lambda x: x[0])

    def desencolar(self) -> T | None:
        """Remueve el elemento de mayor prioridad"""
        if not self.esta_vacia():
            return self.items.pop(0)[1]
        return None

    def esta_vacia(self) -> bool:
        return len(self.items) == 0

    def tamanio(self) -> int:
        return len(self.items)
