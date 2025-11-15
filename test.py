import tests

if __name__ == "__main__":
    try:
        tests.test_pila()
        tests.test_cola_prioridad()
        tests.test_lista_doble()
        tests.test_grafo()
        tests.test_arbol_binario_busqueda()
        print("\nTests completados correctamente")
    except Exception as e:
        print(e)
