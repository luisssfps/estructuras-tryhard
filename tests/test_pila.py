from src.utils.structures.pila import Pila


def test_pila():
    print("\n--- Testing Pila ---")
    pila = Pila()

    # Probar que la pila está vacía inicialmente
    print("Testing Pila.empty()")
    assert pila.empty() is True
    assert pila.size() == 0
    assert pila.pop() is None
    assert pila.top() is None

    # Probar push
    print("Testing Pila.push()")
    pila.push(1)
    pila.push(2)
    pila.push(3)

    assert pila.empty() is False
    assert pila.size() == 3
    assert pila.top() == 3

    # Probar pop
    print("Testing Pila.pop()")
    assert pila.pop() == 3
    assert pila.size() == 2
    assert pila.top() == 2

    assert pila.pop() == 2
    assert pila.pop() == 1
    assert pila.size() == 0
    assert pila.empty() is True
    assert pila.pop() is None

    print("Todos los tests para Pila pasaron.")
