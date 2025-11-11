class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return None

    def imprimir(self):
        if not self.esta_vacia():            
            print(self.items)

    def esta_vacia(self):
        return len(self.items) == 0

    def ver_frente(self):
        return self.items[0] if not self.esta_vacia() else None

    def tamano(self):
        return len(self.items)
