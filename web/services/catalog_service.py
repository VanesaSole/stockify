# app/services/catalog_service.py
# Servicio de importación de catálogo desde Excel.
# Desacoplado del modelo para facilitar testing.

import pandas as pd


def parsear_excel(ruta_archivo):
    """
    Lee un Excel de catálogo y retorna lista de productos normalizados.
    Compatible con el formato del sistema original (columnas flexibles).
    """

    df = pd.read_excel(ruta_archivo)

    # Limpiar nombres de columna
    df.columns = [
        str(col).replace("\n", "").replace("\r", "").strip()
        for col in df.columns
    ]

    # Detectar columna de producto
    col_producto = None
    for col in df.columns:
        if "producto" in col.lower() or "descripci" in col.lower():
            col_producto = col
            break

    if not col_producto:
        # Fallback: segunda columna (como el sistema original)
        if len(df.columns) > 1:
            col_producto = df.columns[1]
        else:
            col_producto = df.columns[0]

    productos = []

    for _, fila in df.iterrows():

        nombre = str(fila[col_producto]).strip()

        if nombre == "nan" or not nombre:
            continue

        p_costo  = _leer_precio(fila, df.columns, "costo")
        p_venta  = _leer_precio(fila, df.columns, "venta")
        p_mayoreo = _leer_precio(fila, df.columns, "mayoreo")

        productos.append({
            "nombre":    nombre,
            "p_costo":   p_costo,
            "p_venta":   p_venta,
            "p_mayoreo": p_mayoreo,
        })

    return productos


def _leer_precio(fila, columnas, tipo):
    """Detecta la columna del tipo de precio y retorna el valor limpio."""

    for col in columnas:
        col_lower = col.lower()

        if tipo == "costo" and "costo" in col_lower:
            return _a_float(fila[col])

        elif tipo == "venta" and "venta" in col_lower and "tipo" not in col_lower:
            return _a_float(fila[col])

        elif tipo == "mayoreo" and "mayoreo" in col_lower:
            return _a_float(fila[col])

    return 0.0


def _a_float(valor):
    """Convierte un valor a float de forma segura."""
    try:
        return float(str(valor).replace("$", "").replace(",", "").strip())
    except:
        return 0.0