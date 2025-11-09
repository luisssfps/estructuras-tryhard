class Nodo_Arbol:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo: Nodo_Arbol = None
        self.derecho: Nodo_Arbol = None

class Arbol:
    def __init__(self):
        self.raiz : Nodo_Arbol = None
    
    def pre_orden(self):
        self.__pre_orden(self.raiz)

    def __pre_orden(self, nodo):
        if nodo is None:
            return 
        print(nodo.dato, end=" ")
        self.__pre_orden(nodo.izquierdo)
        self.__pre_orden(nodo.derecho)

    def in_orden(self):
        self.__in_orden(self.raiz)

    def __in_orden(self, nodo):
        if nodo is None:
            return 
        self.__in_orden(nodo.izquierdo)
        print(nodo.dato, end=" ")
        self.__in_orden(nodo.derecho)
    
    def post_orden(self):
        self.__post_orden(self.raiz)

    def __post_orden(self, nodo):
        if nodo is None:
            return 
        self.__post_orden(nodo.izquierdo)
        self.__post_orden(nodo.derecho)
        print(nodo.dato, end=" ")

    def buscar(self, dato):
        return self.__buscar(self.raiz, dato)

    def __buscar(self, nodo: Nodo_Arbol, dato):
        if nodo is None:
            return False
        
        if dato == nodo.dato:
            return True
        
        if dato < nodo.dato:
            return self.__buscar(nodo.izquierdo, dato)
        else:
            return self.__buscar(nodo.derecho, dato) 

    def buscar_iterativo(self, dato):
        nodo = self.raiz
        while nodo is not None:
            if nodo.dato == dato:
                return True
            elif dato < nodo.dato:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho
        return False
    
    def insertar(self, dato):
        if self.raiz is None:
            self.raiz = Nodo_Arbol(dato)
        else:
            self.__insertar(self.raiz, dato)

    def __insertar(self, nodo, dato):
        if dato < nodo.dato:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo_Arbol(dato)
            else:
                self.__insertar(nodo.izquierdo, dato)
        elif dato > nodo.dato:
            if nodo.derecho is None:
                nodo.derecho = Nodo_Arbol(dato)
            else:
                self.__insertar(nodo.derecho, dato)

    def eliminarPredecesor(self, dato):
        self.raiz = self.__eliminarPredecesor(dato, self.raiz)
    
    def __eliminarPredecesor(self, dato, nodo):
        if nodo is None:
            return nodo
        
        if dato < nodo.dato:
            nodo.izquierdo = self.__eliminarPredecesor(dato, nodo.izquierdo)
        elif dato > nodo.dato:
            nodo.derecho = self.__eliminarPredecesor(dato, nodo.derecho)
        else:
            if nodo.izquiero is None and nodo.derecho is None:
                return None
            
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            
            predecesor = self.__encontrarMaximo(nodo.izquierdo)
            nodo.dato = predecesor.dato
            nodo.izquierdo = self.__eliminarPredecesor(predecesor.dato, nodo.izquierdo)

        return nodo

    def __encontrarMaximo(self, nodo):
        if nodo.derecho is None:
            return nodo
        return self.__encontrarMaximo(nodo.derecho)
