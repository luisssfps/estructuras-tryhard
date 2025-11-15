from src.utils.structures.cola_prioridad import ColaPrioridad


def test_cola_prioridad():
    print("\n--- Testing ColaPrioridad ---")
    cola_p = ColaPrioridad()

    # Probar que la cola de prioridad está vacía inicialmente
    print("Testing cola_p.esta_vacia()")
    assert cola_p.esta_vacia() is True
    assert cola_p.tamanio() == 0
    assert cola_p.desencolar() is None

    # Probar encolar con diferentes prioridades
    print("Testing cola_p.encolar()")
    cola_p.encolar("Tarea 1", 2)
    cola_p.encolar("Tarea 2", 1)
    cola_p.encolar("Tarea 3", 3)
    cola_p.encolar("Tarea 4", 1)

    assert cola_p.esta_vacia() is False
    assert cola_p.tamanio() == 4

    # Probar desencolar según la prioridad
    # Los elementos con prioridad 1 deben salir primero
    print("Testing cola_p.desencolar()")
    item1 = cola_p.desencolar()
    item2 = cola_p.desencolar()

    # El orden entre "Tarea 2" y "Tarea 4" no está garantizado,
    # así que los verificamos en un conjunto
    assert {item1, item2} == {"Tarea 2", "Tarea 4"}

    assert cola_p.tamanio() == 2

    assert cola_p.desencolar() == "Tarea 1"
    assert cola_p.tamanio() == 1

    assert cola_p.desencolar() == "Tarea 3"
    assert cola_p.tamanio() == 0
    assert cola_p.esta_vacia() is True
    assert cola_p.desencolar() is None

    print("Todos los tests para ColaPrioridad pasaron.")
