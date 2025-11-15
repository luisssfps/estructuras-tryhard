from src.utils.structures.grafo import Grafo
from src.utils.structures.lista_doble import ListaDoble


def test_grafo():
    print("\n--- Testing Grafo ---")
    grafo = Grafo()

    # Probar agregar vértices y aristas
    grafo.agregar_vertice("A")
    grafo.agregar_vertice("B")
    grafo.agregar_vertice("C")
    grafo.agregar_vertice("D")
    grafo.agregar_vertice("E")

    grafo.agregar_arista("A", "B", 1)
    grafo.agregar_arista("A", "C", 4)
    grafo.agregar_arista("B", "C", 2)
    grafo.agregar_arista("B", "D", 5)
    grafo.agregar_arista("C", "D", 1)
    grafo.agregar_arista("D", "E", 3)

    # Probar __contains__
    print("Testing 'A' in grafo")
    assert ("A" in grafo) is True
    print("Testing 'F' in grafo")
    assert ("F" in grafo) is False

    # Probar Dijkstra
    print("Testing Dijkstra A to E")
    peso, camino = grafo.dijkstra("A", "E")
    print(f"  Dijkstra A to E: peso={peso}, camino={list(camino)}")
    assert peso == 7
    assert list(camino) == ["A", "B", "C", "D", "E"]

    print("Testing Dijkstra A to D")
    peso, camino = grafo.dijkstra("A", "D")
    print(f"  Dijkstra A to D: peso={peso}, camino={list(camino)}")
    assert peso == 4
    assert list(camino) == ["A", "B", "C", "D"]

    print("Testing Dijkstra E to A")
    peso, camino = grafo.dijkstra("E", "A")
    print(f"  Dijkstra E to A: peso={peso}, camino={list(camino)}")
    assert peso == 7
    assert list(camino) == ["E", "D", "C", "B", "A"]

    # Probar con un nodo sin conexión
    grafo.agregar_vertice("F")
    print("Testing Dijkstra A to F (no connection)")
    peso, camino = grafo.dijkstra("A", "F")
    print(f"  Dijkstra A to F: peso={peso}, camino={list(camino)}")
    assert peso == float("inf")
    assert list(camino) == []

    # Probar obtener_vertice_mas_cercana
    destinos = ListaDoble()
    destinos.agregar_final("D")
    destinos.agregar_final("E")
    destinos.agregar_final("F")

    print("Testing obtener_vertice_mas_cercana A to D, E, F")
    assert grafo.obtener_vertice_mas_cercana("A", destinos) == ("D", 4)

    print("Todos los tests para Grafo pasaron.")
