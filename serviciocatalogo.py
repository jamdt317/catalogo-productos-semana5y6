from modelo.producto import Producto

class CatalogoProductos:
    def __init__(self):
        # Manejo de Colecciones:
        # dict: Búsqueda rápida por ID (CRUD)
        # list: Mantenimiento del orden/listado
        # set: Control estricto de IDs únicos
        self._productos_dict: dict[str, Producto] = {}
        self._ids_unicos: set[str] = set()

    def agregar(self, producto: Producto) -> bool:
        if producto.id_producto in self._ids_unicos:
            return False  # Duplicado
        self._ids_unicos.add(producto.id_producto)
        self._productos_dict[producto.id_producto] = producto
        return True

    def buscar(self, id_producto: str) -> Producto | None:
        return self._productos_dict.get(id_producto)

    def listar(self) -> list[Producto]:
        return list(self._productos_dict.values())

    def actualizar(self, producto: Producto) -> bool:
        if producto.id_producto not in self._ids_unicos:
            return False
        self._productos_dict[producto.id_producto] = producto
        return True

    def eliminar(self, id_producto: str) -> bool:
        if id_producto in self._ids_unicos:
            self._ids_unicos.remove(id_producto)
            del self._productos_dict[id_producto]
            return True
        return False