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

    # =================================================
    # DETECTAR COLUMNAS
    # =================================================

    columna_producto = None

    columna_paq = None

    for col in df.columns:

        nombre = col.lower()

        # PRODUCTO
        if "producto" in nombre:
            columna_producto = col

        # PAQ
        elif "paq" in nombre:
            columna_paq = col

    if not columna_producto:

        raise Exception(
            "No se encontró columna Producto"
        )

    productos = []

    catalogo_dict = {}

    # =================================================
    # RECORRER PRODUCTOS
    # =================================================

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

        paq = 1

        # =============================================
        # DETECTAR COLUMNAS AUTOMATICAMENTE
        # =============================================

        for col in df.columns:

            nombre = col.lower()

            valor = fila[col]

            # COSTO
            if "costo" in nombre:

                costo = valor

            # VENTA
            elif (
                "venta" in nombre
                and "tipo" not in nombre
            ):

                venta = valor

            # MAYOREO
            elif "mayoreo" in nombre:

                mayoreo = valor

        # =============================================
        # LEER PAQ
        # =============================================

        if columna_paq:

            try:

                paq = int(
                    float(
                        fila[columna_paq]
                    )
                )

            except:

                paq = 1

        # =============================================
        # GUARDAR PRODUCTO
        # =============================================

        catalogo_dict[producto] = {

            "P.Costo": costo,

            "P.Venta": venta,

            "P.Mayoreo": mayoreo,

            "P.Paq": paq

        }

    # =================================================
    # RETORNO
    # =================================================

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