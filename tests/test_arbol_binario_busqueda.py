from src.utils.structures.arbol_binario_busqueda import ArbolBinarioBusqueda


def test_arbol_binario_busqueda():
    print("\n--- Testing ArbolBinarioBusqueda ---")
    arbol = ArbolBinarioBusqueda()

    # Probar inserción
    arbol.insertar(10, "Diez")
    arbol.insertar(5, "Cinco")
    arbol.insertar(15, "Quince")
    arbol.insertar(3, "Tres")
    arbol.insertar(7, "Siete")
    arbol.insertar(12, "Doce")
    arbol.insertar(18, "Dieciocho")

    # Probar peso
    print("Testing len(arbol)")
    assert len(arbol) == 7

    # Probar búsqueda
    print("Testing arbol.buscar(10)")
    assert arbol.buscar(10) == "Diez"
    print("Testing arbol.buscar(7)")
    assert arbol.buscar(7) == "Siete"
    print("Testing arbol.buscar(18)")
    assert arbol.buscar(18) == "Dieciocho"
    print("Testing arbol.buscar(100)")
    assert arbol.buscar(100) is None

    # Probar recorrido inorden
    print("Testing recorrer_inorden")
    elementos_inorden = list(arbol.recorrer_inorden())
    claves_inorden = [clave for clave, _ in elementos_inorden]
    assert claves_inorden == [3, 5, 7, 10, 12, 15, 18]

    # Probar eliminación
    # Caso 1: nodo sin hijos
    print("Before deleting 3, len(arbol):", len(arbol))
    arbol.eliminar(3)
    print(
        "After deleting 3, arbol.buscar(3):", arbol.buscar(3), "len(arbol):", len(arbol)
    )
    assert arbol.buscar(3) is None
    assert len(arbol) == 6

    # Caso 2: nodo con un solo hijo
    print("Before deleting 15, len(arbol):", len(arbol))
    arbol.eliminar(15)
    print(
        "After deleting 15, arbol.buscar(15):",
        arbol.buscar(15),
        "len(arbol):",
        len(arbol),
    )
    assert arbol.buscar(15) is None
    assert len(arbol) == 5

    # Caso 3: nodo con dos hijos
    print("Before deleting 10, len(arbol):", len(arbol))
    arbol.eliminar(10)
    print(
        "After deleting 10, arbol.buscar(10):",
        arbol.buscar(10),
        "len(arbol):",
        len(arbol),
    )
    assert arbol.buscar(10) is None
    assert len(arbol) == 4

    print("Testing claves_despues_de_eliminar")
    claves_despues_de_eliminar = [clave for clave, _ in arbol.recorrer_inorden()]
    print("Claves after deletions:", claves_despues_de_eliminar)
    assert claves_despues_de_eliminar == [5, 7, 12, 18]

    print("Todos los tests para ArbolBinarioBusqueda pasaron.")

