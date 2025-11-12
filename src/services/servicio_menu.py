from src.domain import ItemMenu
from src.utils.structures import ArbolBinarioBusqueda


class ServicioDeMenu:
    def __init__(self) -> None:
        self.items_menu: ArbolBinarioBusqueda[str, ItemMenu] = ArbolBinarioBusqueda()

    def registrar_item_menu(self, nombre: str, categoria: str, precio: float) -> None:
        """Registra un nuevo item de menu"""
        item = ItemMenu(nombre, categoria, precio)
        self.items_menu.insertar(item.codigo, item)
        print(f"✓ Item de menu registrado: {item}")

    def buscar_item_menu_por_codigo(self, codigo: str) -> ItemMenu | None:
        """Busca un item de menu por su código"""
        return self.items_menu[codigo]

    def listar_items_menu(self) -> None:
        """Lista todos los items de menu registrados"""

        print("\n=== ITEMS DEL MENÚ ===")
        if len(self.items_menu) == 0:
            print("No hay items de menu registrados")
        else:
            for _, item in self.items_menu:
                print(f"    {item}")
