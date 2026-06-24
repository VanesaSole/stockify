# inventario.py

from database import obtener_conexion

import pandas as pd


# =====================================================
# IMPORTAR CATÁLOGO EXCEL
# =====================================================

def importar_catalogo_excel(ruta_excel):

    try:

        df = pd.read_excel(ruta_excel)

        # limpiar nombres de columnas
        df.columns = [
            str(col)
            .replace("\n", "")
            .replace("\r", "")
            .strip()
            for col in df.columns
        ]

        conn = obtener_conexion()

        cursor = conn.cursor()

        productos_importados = 0
        productos_actualizados = 0

        for _, fila in df.iterrows():

            producto = ""

            codigo = None

            costo = 0
            venta = 0
            mayoreo = 0
            stock = 0

            # detectar columnas automáticamente
            for col in df.columns:

                nombre = col.lower()

                if "producto" in nombre or "descripci" in nombre:
                    producto = str(fila[col]).strip()

                elif "código" in nombre or "codigo" in nombre:
                    codigo = limpiar_codigo(
                        fila[col]
                    )

                elif "costo" in nombre:
                    costo = limpiar_numero(
                        fila[col]
                    )

                elif (
                    "venta" in nombre
                    and "tipo" not in nombre
                ):
                    venta = limpiar_numero(
                        fila[col]
                    )

                elif "mayoreo" in nombre:
                    mayoreo = limpiar_numero(
                        fila[col]
                    )

                elif (
                    "existencia" in nombre
                    or "stock" in nombre
                ):
                    stock = limpiar_numero(
                        fila[col]
                    )

            if not producto or producto == "nan":
                continue

            paq = obtener_paq(
                producto
            )

            # Clave de unicidad real: el código del Excel si existe.
            # Si la fila no trae código, usamos el nombre como fallback
            # para no duplicar el mismo producto en cada reimportación.
            clave_unica = codigo if codigo else f"NOMBRE::{producto.upper()}"

            cursor.execute("""
            INSERT INTO productos (

                codigo,
                nombre,
                stock,
                paq,
                costo,
                venta,
                mayoreo,
                fecha_alta

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))

            ON CONFLICT(codigo) DO UPDATE SET

                nombre = excluded.nombre,
                paq = excluded.paq,
                costo = excluded.costo,
                venta = excluded.venta,
                mayoreo = excluded.mayoreo

            """, (

                clave_unica,
                producto,
                stock,
                paq,
                costo,
                venta,
                mayoreo

            ))

            productos_importados += 1

        conn.commit()

        conn.close()

        return productos_importados

    except Exception as e:

        print(e)

        return 0


# =====================================================
# LIMPIAR CÓDIGO (clave única del Excel)
# =====================================================

def limpiar_codigo(valor):
    """Normaliza el código/SKU del Excel a texto.
    Devuelve None si la celda está vacía, es 'nan' o es un guion '-'."""

    if valor is None:
        return None

    texto = str(valor).strip()

    if texto in ("", "nan", "-", "None"):
        return None

    # Si pandas lo trajo como float (p.ej. 123.0), lo normalizamos a entero
    try:
        if texto.endswith(".0"):
            texto = texto[:-2]
    except Exception:
        pass

    return texto


# =====================================================
# EXTRAER PAQ
# =====================================================

def obtener_paq(nombre_producto):

    texto = str(
        nombre_producto
    ).upper()

    if "PAQ" not in texto:
        return 1

    numeros = ""

    i = texto.find("PAQ") - 1

    while i >= 0:

        if texto[i].isdigit():

            numeros = texto[i] + numeros

            i -= 1

        else:
            break

    try:

        return int(numeros)

    except:

        return 1


# =====================================================
# LIMPIAR NUMEROS
# =====================================================

def limpiar_numero(valor):

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
# OBTENER PRODUCTOS
# =====================================================

def obtener_productos():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        id,
        nombre,
        stock,
        paq,
        costo,
        venta,
        mayoreo

    FROM productos

    ORDER BY nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# BUSCAR PRODUCTOS
# =====================================================

def buscar_productos(texto):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        id,
        nombre,
        stock,
        paq,
        costo,
        venta,
        mayoreo

    FROM productos

    WHERE nombre LIKE ?

    ORDER BY nombre
    """, (

        f"%{texto}%",

    ))

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# AGREGAR STOCK
# =====================================================

def agregar_stock(
    producto_id,
    cantidad
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE productos

    SET stock = stock + ?

    WHERE id = ?
    """, (

        cantidad,
        producto_id

    ))

    conn.commit()

    conn.close()


# =====================================================
# QUITAR STOCK
# =====================================================

def quitar_stock(
    producto_id,
    cantidad
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE productos

    SET stock = stock - ?

    WHERE id = ?
    AND stock >= ?
    """, (

        cantidad,
        producto_id,
        cantidad

    ))

    conn.commit()

    conn.close()


# =====================================================
# OBTENER PRODUCTO
# =====================================================

def obtener_producto(
    producto_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *

    FROM productos

    WHERE id = ?
    """, (

        producto_id,

    ))

    producto = cursor.fetchone()

    conn.close()

    return producto