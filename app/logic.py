# logic.py

# ---------------- BUSCADOR ----------------

def buscar_productos(texto, productos, limite=30):
    """
    Filtra productos según texto ingresado.
    """
    if not texto:
        return []

    texto = texto.lower()

    resultados = [
        p for p in productos
        if texto in p.lower()
    ]

    return resultados[:limite]


# ---------------- VALIDACIÓN ----------------

def convertir_cantidad(valor):
    """
    Convierte string a float válido.
    """
    if not valor:
        return None

    valor = valor.replace(",", ".")

    try:
        return float(valor)
    except ValueError:
        return None


# ---------------- AGREGAR PRODUCTO ----------------

def obtener_datos_producto(producto, catalogo_dict):
    """
    Busca los datos de un producto en el catálogo.
    """
    if not catalogo_dict:
        return None

    fila = catalogo_dict.get(producto)

    if not fila:
        return None

    return {
        "costo": fila.get("precio_costo", ""),
        "venta": fila.get("precio_venta", ""),
        "mayoreo": fila.get("precio_mayoreo", "")
    }


def construir_fila_tabla(producto, cantidad, datos_producto, modo):
    """
    Construye la fila que se insertará en la tabla.
    """
    if modo == "PEDIDO":
        return (
            producto,
            cantidad,
            "", "", ""
        )

    elif modo == "ENVIO":
        return (
            producto,
            cantidad,
            datos_producto.get("costo", ""),
            datos_producto.get("venta", ""),
            datos_producto.get("mayoreo", "")
        )


def agregar_producto(producto, cantidad_str, catalogo_dict, modo):
    """
    Procesa la lógica completa de agregar producto.
    """

    cantidad = convertir_cantidad(cantidad_str)

    if cantidad is None:
        return {
            "error": "Cantidad inválida"
        }

    datos_producto = obtener_datos_producto(producto, catalogo_dict)

    if not datos_producto:
        return {
            "error": "Producto no encontrado"
        }

    fila = construir_fila_tabla(producto, cantidad, datos_producto, modo)

    return {
        "fila": fila
    }


# ---------------- ELIMINAR ----------------

def eliminar_indices(lista_datos, indices):
    """
    Elimina elementos de una lista según índices.
    """
    return [
        item for i, item in enumerate(lista_datos)
        if i not in indices
    ]


# ---------------- MODO ----------------

def cambiar_modo(modo_actual):
    """
    Alterna entre PEDIDO y ENVIO.
    """
    if modo_actual == "PEDIDO":
        return "ENVIO"
    return "PEDIDO"


# ---------------- EXPORTACIÓN ----------------

def preparar_datos_exportacion(datos_tabla, modo):
    """
    Prepara los datos según el modo para exportar.
    """
    if modo == "PEDIDO":
        columnas = ["Descripción", "Cantidad"]

        datos = [
            (fila[0], fila[1])
            for fila in datos_tabla
        ]

    else:
        columnas = [
            "Descripción",
            "Cantidad",
            "Costo",
            "Venta",
            "Mayoreo"
        ]

        datos = datos_tabla

    return columnas, datos


def validar_tabla_vacia(datos_tabla):
    """
    Verifica si hay productos en la tabla.
    """
    return len(datos_tabla) == 0


# ---------------- UTILIDAD GENERAL ----------------

def limpiar_texto(texto):
    """
    Limpia texto de espacios innecesarios.
    """
    return texto.strip() if texto else ""