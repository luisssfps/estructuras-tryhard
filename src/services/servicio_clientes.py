from src.domain import Cliente
from src.utils.structures import ArbolBinarioBusqueda
from src.services.servicio_mapa import ServicioDeMapa


class ServicioDeClientes:
    def __init__(self, servicio_mapa: ServicioDeMapa) -> None:
        self.clientes: ArbolBinarioBusqueda[str, Cliente] = ArbolBinarioBusqueda()
        self.servicio_mapa: ServicioDeMapa = servicio_mapa

    def registrar_cliente(self, nombre: str, zona: str) -> Cliente | None:
        """Registra un nuevo cliente"""
        if not self.servicio_mapa.zona_en_mapa(zona):
            print(f"✗ La zona '{zona}' no existe en el mapa")
            return

        cliente = Cliente(nombre, zona)
        self.clientes[cliente.codigo] = cliente
        print(f"✓ Cliente registrado: {cliente}")
        return cliente

    def buscar_cliente_por_codigo(self, codigo: str) -> Cliente | None:
        """Busca un cliente por su código"""
        return self.clientes[codigo]

    def listar_clientes(self) -> None:
        """Lista todos los clientes registrados"""
        print("\n=== CLIENTES REGISTRADOS ===")

        if len(self.clientes) == 0:
            print("No hay clientes registrados")
        else:
            for _, cliente in self.clientes:
                print(f"  {cliente}")
