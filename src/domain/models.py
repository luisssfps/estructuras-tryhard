from datetime import datetime
from enum import Enum

from src.utils.structures import ListaDoble


class EstadoPedido(Enum):
    """Estados posibles de un pedido"""

    PENDIENTE = "Pendiente"
    ASIGNADO = "Asignado"
    EN_CAMINO = "En Camino"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"


class TipoAccion(Enum):
    """Tipos de acciones para el historial (pila)"""

    CREAR_PEDIDO = "Crear Pedido"
    CANCELAR_PEDIDO = "Cancelar Pedido"
    ASIGNAR_DOMICILIARIO = "Asignar Domiciliario"
    ENTREGAR_PEDIDO = "Entregar Pedido"


class Cliente:
    """Entidad Cliente"""

    contador_id: int = 1

    def __init__(self, nombre_completo: str, zona: str) -> None:
        self.codigo: str = f"CLI{Cliente.contador_id:04d}"
        Cliente.contador_id += 1
        self.nombre_completo: str = nombre_completo
        self.zona: str = zona

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre_completo} ({self.zona})"


class ItemMenu:
    """Elemento del menú de un restaurante"""

    contador_id: int = 1

    def __init__(self, nombre: str, categoria: str, precio: float) -> None:
        self.codigo: str = f"ITEM{ItemMenu.contador_id:04d}"
        ItemMenu.contador_id += 1
        self.nombre: str = nombre
        self.categoria: str = categoria
        self.precio: float = precio

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.categoria}) - ${self.precio:.2f}"


class Restaurante:
    """Entidad Restaurante"""

    contador_id: int = 1

    def __init__(self, nombre: str, zona: str) -> None:
        self.codigo: str = f"REST{Restaurante.contador_id:04d}"
        Restaurante.contador_id += 1
        self.nombre: str = nombre
        self.zona: str = zona

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.zona})"


class Domiciliario:
    """Entidad Domiciliario"""

    contador_id: int = 1

    def __init__(self, nombre: str, zona_actual: str) -> None:
        self.codigo: str = f"DOM{Domiciliario.contador_id:04d}"
        Domiciliario.contador_id += 1
        self.nombre: str = nombre
        self.zona_actual: str = zona_actual
        self.disponible: bool = True
        self.pedidos_entregados: int = 0

    def __str__(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"{self.codigo} - {self.nombre} ({self.zona_actual}) [{estado}]"


class Accion:
    """Registro de acción para el historial (pila)"""

    def __init__(self, tipo: TipoAccion, descripcion: str, pedido_id: int) -> None:
        self.tipo: TipoAccion = tipo
        self.descripcion: str = descripcion
        self.pedido_id: int = pedido_id
        self.fecha_hora: datetime = datetime.now()

    def __str__(self) -> str:
        return f"[{self.fecha_hora.strftime('%H:%M:%S')}] {self.tipo.value}: {self.descripcion}"


class Pedido:
    """Entidad Pedido"""

    contador_id: int = 1

    def __init__(self, cliente: Cliente) -> None:
        self.id: int = Pedido.contador_id
        Pedido.contador_id += 1
        self.cliente: Cliente = cliente
        self.items_pedido: ListaDoble[ItemMenu] = ListaDoble()
        self.restaurante: Restaurante | None = None
        self.domiciliario: Domiciliario | None = None
        self.estado: EstadoPedido = EstadoPedido.PENDIENTE
        self.fecha_hora: datetime = datetime.now()

    def agregar_item(self, item: ItemMenu) -> None:
        self.items_pedido.agregar_final(item)

    @property
    def total(self) -> float:
        return sum(item.precio for item in self.items_pedido)

    def __str__(self) -> str:
        rest_info = self.restaurante.nombre if self.restaurante else "Sin asignar"
        dom_info = self.domiciliario.nombre if self.domiciliario else "Sin asignar"
        return (
            f"Pedido #{self.id} - Cliente: {self.cliente.nombre_completo} | "
            f"Estado: {self.estado.value} | Rest: {rest_info} | Dom: {dom_info}"
        )
