class Producto:
    def __init__(self, id_producto: str, nombre: str, precio: float, Categoria: str):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = Categoria

    def __hash__(self):
        # Permite usar Producto en un set basado en id_producto
        return hash(self.id_producto)

    def __eq__(self, other):
        if isinstance(other, Producto):
            return self.id_producto == other.id_producto
        return False

    def __repr__(self):
        return f"Producto({self.id_producto}, {self.nombre}, ${self.precio:.2f}, {self.categoria})"