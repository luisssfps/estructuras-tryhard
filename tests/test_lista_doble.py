from src.utils.structures.lista_doble import ListaDoble


def test_lista_doble():
    print("\n--- Testing ListaDoble ---")
    lista = ListaDoble()

    # Probar que la lista está vacía inicialmente
    print("Testing ListaDoble.esta_vacia()")
    assert lista.esta_vacia() is True
    assert len(lista) == 0
    assert list(lista) == []

    # Probar agregar al principio
    print("Testing ListaDoble.agregar_principio()")
    lista.agregar_principio(1)
    lista.agregar_principio(2)
    lista.agregar_principio(3)

    assert len(lista) == 3
    assert list(lista) == [3, 2, 1]

    # Probar agregar al final
    print("Testing ListaDoble.agregar_final()")
    lista.agregar_final(4)
    assert len(lista) == 4
    assert list(lista) == [3, 2, 1, 4]

    # Probar buscar
    print("Testing ListaDoble.buscar()")
    assert lista.buscar(lambda x: x == 2) == 2
    assert lista.buscar(lambda x: x == 5) is None

    # Probar __contains__
    print("Testing ListaDoble.__contains__()")
    assert (2 in lista) is True
    assert (5 in lista) is False

    # Probar eliminar
    print("Testing ListaDoble.eliminar()")
    assert lista.eliminar(lambda x: x == 2) == 2
    assert len(lista) == 3
    assert list(lista) == [3, 1, 4]
    assert lista.eliminar(lambda x: x == 5) is None

    assert lista.eliminar(lambda x: x == 3) == 3
    assert len(lista) == 2
    assert list(lista) == [1, 4]

    assert lista.eliminar(lambda x: x == 4) == 4
    assert len(lista) == 1
    assert list(lista) == [1]

    assert lista.eliminar(lambda x: x == 1) == 1
    assert len(lista) == 0
    assert list(lista) == []

    print("Todos los tests para ListaDoble pasaron.")
