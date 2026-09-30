import flet as ft
from modelo.producto import Producto
from servicio.catalogo import CatalogoProductos

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
                    ],
                    on_select_changed=lambda e, p=prod: cargar_datos_seleccionados(p)
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

    def mostrar_alerta(mensaje: str, es_error: bool = False):
        color = ft.Colors.RED_400 if es_error else ft.Colors.GREEN_400
        snack = ft.SnackBar(ft.Text(mensaje), bg_color=color)
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

    # Manejo de Eventos CRUD
    def btn_agregar_click(e):
        valido, msg = validar_entradas()
        if not valido:
            mostrar_alerta(msg, es_error=True)
            return

        prod = Producto(txt_id.value.strip(), txt_nombre.value.strip(), float(txt_precio.value), txt_categoria.value.strip())
        if catalogo.agregar(prod):
            mostrar_alerta("Producto agregado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: El ID ya existe.", es_error=True)

    def btn_actualizar_click(e):
        valido, msg = validar_entradas()
        if not valido:
            mostrar_alerta(msg, es_error=True)
            return

        prod = Producto(txt_id.value.strip(), txt_nombre.value.strip(), float(txt_precio.value), txt_categoria.value.strip())
        if catalogo.actualizar(prod):
            mostrar_alerta("Producto actualizado correctamente.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: El producto no existe.", es_error=True)

    def btn_eliminar_click(e):
        id_prod = txt_id.value.strip()
        if not id_prod:
            mostrar_alerta("Ingrese el ID del producto a eliminar.", es_error=True)
            return

        if catalogo.eliminar(id_prod):
            mostrar_alerta("Producto eliminado.")
            limpiar_campos()
            refrescar_tabla()
        else:
            mostrar_alerta("Error: ID no encontrado.", es_error=True)

    # Controles de la Interfaz
    page.add(
        ft.Text("Catálogo de Productos", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Row([txt_id, txt_nombre]),
        ft.Row([txt_precio, txt_categoria]),
        ft.Row([
            ft.ElevatedButton("Agregar", on_click=btn_agregar_click, icon=ft.Icons.ADD),
            ft.ElevatedButton("Actualizar", on_click=btn_actualizar_click, icon=ft.Icons.UPDATE),
            ft.ElevatedButton("Eliminar", on_click=btn_eliminar_click, icon=ft.Icons.DELETE),
            ft.OutlinedButton("Limpiar Formulario", on_click=lambda _: (limpiar_campos(), page.update())),
        ]),
        ft.Divider(),
        ft.Text("Listado de Productos (Haz clic en una fila para editar):"),
        tabla
    )

ft.app(target=main)