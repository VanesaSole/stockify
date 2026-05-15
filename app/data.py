# data.py

import pandas as pd


# =====================================================
# CARGAR CATÁLOGO
# =====================================================

def cargar_catalogo(ruta):

    df = pd.read_excel(ruta)

    # limpiar nombres columnas
    df.columns = [
        str(col)
        .replace("\n", "")
        .replace("\r", "")
        .strip()
        for col in df.columns
    ]

    print("\nCOLUMNAS DETECTADAS EN EXCEL:")
    print(df.columns.tolist())

    # verificar producto
    columna_producto = None

    for col in df.columns:

        nombre = col.lower()

        if "producto" in nombre:
            columna_producto = col
            break

    if not columna_producto:
        raise Exception(
            "No se encontró columna Producto"
        )

    productos = []

    catalogo_dict = {}

    for _, fila in df.iterrows():

        producto = str(
            fila[columna_producto]
        ).strip()

        if producto == "nan":
            continue

        productos.append(producto)

        costo = 0
        venta = 0
        mayoreo = 0

        # detectar columnas automáticamente
        for col in df.columns:

            nombre = col.lower()

            # COSTO
            if "costo" in nombre:
                costo = fila[col]

            # VENTA
            elif (
                "venta" in nombre
                and "tipo" not in nombre
            ):
                venta = fila[col]

            # MAYOREO
            elif "mayoreo" in nombre:
                mayoreo = fila[col]

        catalogo_dict[producto] = {

            "P.Costo": costo,

            "P.Venta": venta,

            "P.Mayoreo": mayoreo

        }

    return {

        "productos": productos,

        "productos_lower": [
            p.lower()
            for p in productos
        ],

        "catalogo_dict": catalogo_dict

    }


# =====================================================
# EXPORTAR EXCEL
# =====================================================

def exportar_excel(
    ruta,
    columnas,
    datos
):

    df = pd.DataFrame(
        datos,
        columns=columnas
    )

    df.to_excel(
        ruta,
        index=False
    )


# =====================================================
# VALIDAR EXTENSIONES
# =====================================================

def es_excel(ruta):

    return ruta.lower().endswith(
        (".xlsx", ".xls")
    )


def es_pdf(ruta):

    return ruta.lower().endswith(
        ".pdf"
    )