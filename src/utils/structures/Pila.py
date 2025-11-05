class Pila:
    def __init__(self):
        self._items = []
        
    def push(self, elemento):
        self._items.append(elemento)

    def pop(self):
        if not self.empty():
            return self._items.pop()
        return None

    def print_stack(self):
        for item in reversed(self._items):
            print(item,  end=" ")
    
    def empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def top(self):
        return self._items[-1] if not self.empty() else None
