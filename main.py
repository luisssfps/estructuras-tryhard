from src.services import SistemaPedidosDomicilio
from src.views.cmd.menus import menu_principal


def inicializar_datos_prueba(sistema: SistemaPedidosDomicilio) -> None:
    """Inicializa el sistema con datos de prueba"""
    # Crear mapa de la ciudad (10 zonas)
    zonas = [
        "Norte",
        "Sur",
        "Este",
        "Oeste",
        "Centro",
        "NorEste",
        "NorOeste",
        "SurEste",
        "SurOeste",
        "Periferia",
    ]

    for zona in zonas:
        sistema.servicio_mapa.agregar_zona(zona)

    # Conexiones entre zonas (bidireccionales con distancias)
    conexiones = [
        ("Norte", "Centro", 5),
        ("Sur", "Centro", 5),
        ("Este", "Centro", 4),
        ("Oeste", "Centro", 4),
        ("Norte", "NorEste", 3),
        ("Norte", "NorOeste", 3),
        ("Sur", "SurEste", 3),
        ("Sur", "SurOeste", 3),
        ("Este", "NorEste", 4),
        ("Este", "SurEste", 4),
        ("Oeste", "NorOeste", 4),
        ("Oeste", "SurOeste", 4),
        ("NorEste", "Periferia", 6),
        ("SurEste", "Periferia", 7),
        ("Centro", "Periferia", 10),
    ]

    for origen, destino, peso in conexiones:
        sistema.servicio_mapa.agregar_conexion(origen, destino, peso)

    # Registrar clientes
    clientes_prueba = [
        ("Juan Pérez", "Norte"),
        ("María González", "Sur"),
        ("Carlos Rodríguez", "Este"),
        ("Ana Martínez", "Centro"),
        ("Luis López", "Oeste"),
    ]

    for nombre, zona in clientes_prueba:
        sistema.servicio_clientes.registrar_cliente(nombre, zona)

    # Registrar restaurantes con menús
    items = (
        ("Hamburguesa Clásica", "Plato Fuerte", 15000),
        ("Papas Fritas", "Entrada", 5000),
        ("Gaseosa", "Bebida", 3000),
        ("Pizza Pepperoni", "Plato Fuerte", 25000),
        ("Pan de Ajo", "Entrada", 6000),
        ("Coca Cola", "Bebida", 3000),
        ("Roll California", "Plato Fuerte", 28000),
        ("Edamame", "Entrada", 8000),
        ("Té Verde", "Bebida", 4000),
        ("Tacos al Pastor", "Plato Fuerte", 18000),
        ("Nachos", "Entrada", 7000),
        ("Agua de Horchata", "Bebida", 3500),
        ("Pasta Carbonara", "Plato Fuerte", 22000),
        ("Ensalada César", "Entrada", 9000),
        ("Vino Tinto", "Bebida", 15000),
    )

    restaurantes_data = (
        ("Burger King", "Centro"),
        ("Pizza Hut", "Norte"),
        ("Sushi Express", "Este"),
        ("Taco Bell", "Sur"),
        ("Pasta Bella", "Oeste"),
    )

    # Registrar restaurantes
    for nombre_restaurante, zona in restaurantes_data:
        sistema.servicio_restaurantes.registrar_restaurante(nombre_restaurante, zona)

    # Agregar items al menú
    for nombre_platillo, categoria, precio in items:
        sistema.registrar_item_menu(nombre_platillo, categoria, precio)

    # Registrar domiciliarios
    domiciliarios_data = [
        ("Pedro Sánchez", "Centro"),
        ("Laura Ramírez", "Norte"),
        ("Diego Torres", "Sur"),
        ("Sofia Vargas", "Este"),
        ("Miguel Ángel", "Oeste"),
    ]

    for nombre, zona in domiciliarios_data:
        sistema.servicio_domiciliarios.registrar_domiciliario(nombre, zona)


def main():
    sistema = SistemaPedidosDomicilio()
    inicializar_datos_prueba(sistema)
    input("\nPresione Enter para continuar...")

    menu_principal(sistema)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Gracias por usar el sistema!")
    except ValueError as e:
        print(f"✗ Error: {e}")
