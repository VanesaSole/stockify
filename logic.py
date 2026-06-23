# logic.py

# =====================================================
# BUSCADOR
# =====================================================

def buscar_productos(texto, productos, limite=30):

    if not texto:
        return []

    texto = texto.lower()

    resultados = [
        p for p in productos
        if texto in p.lower()
    ]

    return resultados[:limite]


# =====================================================
# VALIDAR CANTIDAD
# =====================================================

def convertir_cantidad(valor):

    if not valor:
        return None

    valor = str(valor).replace(",", ".")

    try:
        return float(valor)

    except:
        return None


# =====================================================
# LIMPIAR PRECIOS
# =====================================================

def limpiar_precio(valor):

    if valor is None:
        return 0

    valor = str(valor)

    valor = valor.replace("$", "")
    valor = valor.replace(",", "")
    valor = valor.strip()

    try:
        return float(valor)

    except:
        return 0


# =====================================================
# OBTENER DATOS PRODUCTO
# =====================================================

def obtener_datos_producto(producto, catalogo_dict):

    if producto not in catalogo_dict:
        return None

    fila = catalogo_dict[producto]

    costo = limpiar_precio(
        fila.get("P.Costo", 0)
    )

    venta = limpiar_precio(
        fila.get("P.Venta", 0)
    )

    mayoreo = limpiar_precio(
        fila.get("P.Mayoreo", 0)
    )

    paq = fila.get("P.Paq", 1)

    try:

        paq = int(paq)

    except:

        paq = 1

    return {

        "costo": costo,

        "venta": venta,

        "mayoreo": mayoreo,

        "paq": paq

    }


# =====================================================
# CONVERTIR UNIDADES
# =====================================================

def calcular_unidades_reales(
    cantidad,
    tipo_carga,
    paq
):

    if tipo_carga == "BULTO":

        return cantidad * paq

    return cantidad


# =====================================================
# CONSTRUIR FILA
# =====================================================

def construir_fila_tabla(
    producto,
    cantidad_original,
    unidades_reales,
    tipo_carga,
    datos_producto,
    modo
):

    # =================================================
    # MODO PEDIDO
    # =================================================

    if modo == "PEDIDO":

        return (

            producto,

            tipo_carga,

            cantidad_original,

            unidades_reales

        )

    # =================================================
    # MODO ENVIO
    # =================================================

    costo = datos_producto["costo"]

    venta = datos_producto["venta"]

    mayoreo = datos_producto["mayoreo"]

    total = unidades_reales * costo

    return (

        producto,

        tipo_carga,

        cantidad_original,

        unidades_reales,

        costo,

        venta,

        mayoreo,

        total

    )


# =====================================================
# AGREGAR PRODUCTO
# =====================================================

def agregar_producto(
    producto,
    cantidad_str,
    catalogo_dict,
    modo,
    tipo_carga="UNIDAD"
):

    cantidad = convertir_cantidad(
        cantidad_str
    )

    if cantidad is None:

        return {
            "error": "Cantidad inválida"
        }

    datos_producto = obtener_datos_producto(
        producto,
        catalogo_dict
    )

    if not datos_producto:

        return {
            "error": "Producto no encontrado"
        }

    paq = datos_producto["paq"]

    unidades_reales = calcular_unidades_reales(

        cantidad,

        tipo_carga,

        paq

    )

    fila = construir_fila_tabla(

        producto,

        cantidad,

        unidades_reales,

        tipo_carga,

        datos_producto,

        modo

    )

    return {
        "fila": fila
    }


# =====================================================
# CAMBIAR MODO
# =====================================================

def cambiar_modo(modo_actual):

    if modo_actual == "PEDIDO":
        return "ENVIO"

    return "PEDIDO"


# =====================================================
# EXPORTAR
# =====================================================

def preparar_datos_exportacion(
    datos_tabla,
    modo
):

    # =================================================
    # PEDIDO
    # =================================================

    if modo == "PEDIDO":

        columnas = [

            "Producto",

            "Tipo",

            "Cantidad",

            "Unidades"

        ]

    # =================================================
    # ENVIO
    # =================================================

    else:

        columnas = [

            "Producto",

            "Tipo",

            "Cantidad",

            "Unidades",

            "Costo",

            "Venta",

            "Mayoreo",

            "Total"

        ]

    return columnas, datos_tabla


# =====================================================
# VALIDAR TABLA
# =====================================================

def validar_tabla_vacia(datos_tabla):

    return len(datos_tabla) == 0