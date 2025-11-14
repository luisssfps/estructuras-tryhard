from src.services.servicio_principla import SistemaPedidosDomicilio


def menu_principal(sistema: SistemaPedidosDomicilio) -> None:
    """Menú interactivo del sistema"""

    while True:
        print("\n" + "=" * 60)
        print("  SISTEMA DE GESTIÓN DE PEDIDOS A DOMICILIO")
        print("=" * 60)
        print("\n[1] Menú")
        print("[2] Gestión de Clientes")
        print("[3] Gestión de Restaurantes")
        print("[4] Gestión de Domiciliarios")
        print("[5] Gestión de Pedidos")
        print("[6] Visualización y Consultas")
        print("[7] Mapa y Rutas")
        print("[8] Historial y Estadísticas")
        print("[0] Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            submenu_menu(sistema)
        elif opcion == "2":
            submenu_clientes(sistema)
        elif opcion == "3":
            submenu_restaurantes(sistema)
        elif opcion == "4":
            submenu_domiciliarios(sistema)
        elif opcion == "5":
            submenu_pedidos(sistema)
        elif opcion == "6":
            submenu_visualizacion(sistema)
        elif opcion == "7":
            submenu_mapa(sistema)
        elif opcion == "8":
            submenu_historial(sistema)
        elif opcion == "0":
            print("\n¡Gracias por usar el sistema!")
            break
        else:
            print("✗ Opción inválida")


def submenu_menu(sistema: SistemaPedidosDomicilio):
    """Submenú de menú"""
    print("\n--- MENÚ ---")
    print("[1] Registrar item del menú")
    print("[2] Listar items del menú")
    print("[3] Buscar item del menú")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre: ").strip()
        try:
            precio = float(input("Precio: ").strip())
        except Exception:
            print("✗ Valor inválido, por favor ingrese un número")
            return
        categoria = input("Categoria: ").strip()

        sistema.registrar_item_menu(nombre, categoria, precio)
    elif opcion == "2":
        sistema.listar_items_menu()
    elif opcion == "3":
        codigo = input("Codigo: ").strip()
        item = sistema.buscar_item_menu_por_codigo(codigo)
        if item:
            print(f"✓ Encontrado: {item}")
        else:
            print("✗ Item no encontrado")
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_clientes(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de gestión de clientes"""
    print("\n--- GESTIÓN DE CLIENTES ---")
    print("[1] Registrar cliente")
    print("[2] Listar clientes")
    print("[3] Buscar cliente")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre completo: ").strip()
        zona = input("Zona: ").strip()
        try:
            sistema.registrar_cliente(nombre, zona)
        except ValueError as e:
            print(f"✗ Error: {e}")
    elif opcion == "2":
        sistema.listar_clientes()
    elif opcion == "3":
        codigo = input("Código del cliente: ").strip()
        cliente = sistema.buscar_cliente_por_codigo(codigo)
        if cliente:
            print(f"✓ Encontrado: {cliente}")
        else:
            print("✗ Cliente no encontrado")
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_restaurantes(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de gestión de restaurantes"""
    print("\n--- GESTIÓN DE RESTAURANTES ---")
    print("[1] Registrar restaurante")
    print("[2] Listar restaurantes")
    print("[3] Buscar restaurante")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre: ").strip()
        zona = input("Zona: ").strip()
        try:
            sistema.registrar_restaurante(nombre, zona)
        except ValueError as e:
            print(f"✗ Error: {e}")
    elif opcion == "2":
        sistema.listar_restaurantes()
    elif opcion == "3":
        codigo = input("Código del restaurante: ").strip()
        restaurante = sistema.buscar_restaurante_por_codigo(codigo)
        if restaurante:
            print(f"✓ Encontrado: {restaurante}")
        else:
            print("✗ Restaurante no encontrado")
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_domiciliarios(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de gestión de domiciliarios"""
    print("\n--- GESTIÓN DE DOMICILIARIOS ---")
    print("[1] Registrar domiciliario")
    print("[2] Listar domiciliarios")
    print("[3] Ver estadísticas")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        nombre = input("Nombre: ").strip()
        zona = input("Zona actual: ").strip()
        try:
            sistema.registrar_domiciliario(nombre, zona)
        except ValueError as e:
            print(f"✗ Error: {e}")
    elif opcion == "2":
        sistema.listar_domiciliarios()
    elif opcion == "3":
        sistema.estadisticas_domiciliarios()
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_pedidos(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de gestión de pedidos"""
    print("\n--- GESTIÓN DE PEDIDOS ---")
    print("[1] Crear pedido")
    print("[2] Asignar siguiente pedido")
    print("[3] Entregar pedido")
    print("[4] Cancelar pedido")
    print("[5] Deshacer última acción")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        codigo_cliente = input("Código del cliente: ").strip()
        items = input("Items del pedido (separados por coma): ").strip().split(",")
        items = [item.strip() for item in items]
        prioridad = int(input("Prioridad (1-5, default 3): ").strip() or "3")
        sistema.crear_pedido(codigo_cliente, items, prioridad)
    elif opcion == "2":
        sistema.asignar_pedido()
    elif opcion == "3":
        pedido_id = int(input("ID del pedido: ").strip())
        sistema.entregar_pedido(pedido_id)
    elif opcion == "4":
        pedido_id = int(input("ID del pedido: ").strip())
        sistema.cancelar_pedido(pedido_id)
    elif opcion == "5":
        sistema.deshacer_ultima_accion()
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_visualizacion(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de visualización"""
    print("\n--- VISUALIZACIÓN ---")
    print("[1] Ver pedidos activos")
    print("[2] Ver cola de pedidos")
    print("[3] Ver historial de acciones")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        sistema.ver_pedidos_activos()
    elif opcion == "2":
        sistema.ver_cola_pedidos()
    elif opcion == "3":
        n = int(input("¿Cuántas acciones mostrar? (default 10): ").strip() or "10")
        sistema.ver_historial_acciones(n)
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_mapa(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de mapa y rutas"""
    print("\n--- MAPA Y RUTAS ---")
    print("[1] Ver mapa completo")
    print("[2] Calcular ruta entre zonas")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        sistema.ver_mapa_ciudad()
    elif opcion == "2":
        origen = input("Zona origen: ").strip()
        destino = input("Zona destino: ").strip()
        sistema.calcular_ruta(origen, destino)
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")


def submenu_historial(sistema: SistemaPedidosDomicilio) -> None:
    """Submenú de historial y estadísticas"""
    print("\n--- HISTORIAL Y ESTADÍSTICAS ---")
    print("[1] Ver historial completo de pedidos")
    print("[2] Ver historial por cliente")
    print("[3] Ver pedidos por zona")
    print("[4] Estadísticas de domiciliarios")
    print("[0] Cancelar")

    opcion = input("Opción: ").strip()

    if opcion == "1":
        sistema.ver_historial_pedidos_completo()
    elif opcion == "2":
        codigo = input("Código del cliente: ").strip()
        sistema.ver_historial_por_cliente(codigo)
    elif opcion == "3":
        zona = input("Zona: ").strip()
        sistema.ver_historial_por_zona(zona)
    elif opcion == "4":
        sistema.estadisticas_domiciliarios()
    elif opcion == "0":
        pass
    else:
        print("✗ Opción inválida")
