import flet as ft

# ==========================================
# 1. MODELO (Clase Producto)
# ==========================================
class Producto:
    def __init__(self, id_producto: str, nombre: str, precio: float, categoria: str):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def __hash__(self):
        return hash(self.id_producto)

    def __eq__(self, other):
        if isinstance(other, Producto):
            return self.id_producto == other.id_producto
        return False


# ==========================================
# 2. SERVICIO (Colecciones y Operaciones CRUD)
# ==========================================
class CatalogoProductos:
    def __init__(self):
        self._productos_dict: dict[str, Producto] = {}
        self._ids_unicos: set[str] = set()

    def agregar(self, producto: Producto) -> bool:
        if producto.id_producto in self._ids_unicos:
            return False
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


# ==========================================
# 3. INTERFAZ GRÁFICA Y MANEJO DE EVENTOS
# ==========================================
def main(page: ft.Page):
    page.title = "Gestión de Catálogo de Productos"
    page.padding = 20
    page.scroll = "adaptive"

    catalogo = CatalogoProductos()

    # Campos de Entrada
    txt_id = ft.TextField(label="ID Producto", width=200)
    txt_nombre = ft.TextField(label="Nombre", width=300)
    txt_precio = ft.TextField(label="Precio ($)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    txt_categoria = ft.TextField(label="Categoría", width=200)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Acción")),
        ],
        rows=[]
    )

    def refrescar_tabla():
        tabla.rows.clear()
        for prod in catalogo.listar():
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(prod.id_producto)),
                        ft.DataCell(ft.Text(prod.nombre)),
                        ft.DataCell(ft.Text(f"${prod.precio:.2f}")),
                        ft.DataCell(ft.Text(prod.categoria)),
                        ft.DataCell(
                            ft.Button(
                                "Seleccionar", 
                                on_click=lambda e, p=prod: cargar_datos_seleccionados(p)
                            )
                        ),
                    ]
                )
            )
        page.update()

    def cargar_datos_seleccionados(prod: Producto):
        txt_id.value = prod.id_producto
        txt_nombre.value = prod.nombre
        txt_precio.value = str(prod.precio)
        txt_categoria.value = prod.categoria
        page.update()

    def limpiar_campos():
        txt_id.value = ""
        txt_nombre.value = ""
        txt_precio.value = ""
        txt_categoria.value = ""

    def mostrar_alerta(mensaje: str):
        snack = ft.SnackBar(ft.Text(mensaje))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def validar_entradas() -> tuple[bool, str]:
        if not txt_id.value.strip():
            return False, "El ID es obligatorio."
        if not txt_nombre.value.strip():
            return False, "El nombre es obligatorio."
        try:
            val = float(txt_precio.value)
            if val < 0:
                return False, "El precio no puede ser negativo."
        except ValueError:
            return False, "El precio debe ser un número válido."
        return True, ""

    # Controladores de Eventos (Botones)
    def btn_agregar_click(e):
        valido, msg = validar_entradas()
        if not valido:
            mostrar_alerta(msg)
            return

        prod = Producto(txt_id.value.strip(), txt_nombre.value.strip(), float(txt_precio.value), txt_categoria.value.strip())
        if catalogo.agregar(prod):
            mostrar_alerta("Producto agregado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: El ID ya existe.")

    def btn_actualizar_click(e):
        valido, msg = validar_entradas()
        if not valido:
            mostrar_alerta(msg)
            return

        prod = Producto(txt_id.value.strip(), txt_nombre.value.strip(), float(txt_precio.value), txt_categoria.value.strip())
        if catalogo.actualizar(prod):
            mostrar_alerta("Producto actualizado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: El producto no existe.")

    def btn_eliminar_click(e):
        id_prod = txt_id.value.strip()
        if not id_prod:
            mostrar_alerta("Ingrese el ID del producto a eliminar.")
            return

        if catalogo.eliminar(id_prod):
            mostrar_alerta("Producto eliminado.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: ID no encontrado.")

    # Organización de componentes visuales
    page.add(
        ft.Text("Catálogo de Productos", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([txt_id, txt_nombre]),
        ft.Row([txt_precio, txt_categoria]),
        ft.Row([
            ft.Button("Agregar", on_click=btn_agregar_click),
            ft.Button("Actualizar", on_click=btn_actualizar_click),
            ft.Button("Eliminar", on_click=btn_eliminar_click),
            ft.Button("Limpiar Formulario", on_click=lambda _: (limpiar_campos(), page.update())),
        ]),
        ft.Divider(),
        ft.Text("Listado de Productos:"),
        tabla
    )

if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)