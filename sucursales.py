# sucursales.py

from database import obtener_conexion


# =====================================================
# CREAR SUCURSAL
# =====================================================

def crear_sucursal(
    nombre,
    direccion="",
    telefono=""
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO sucursales (

            nombre,
            direccion,
            telefono

        )
        VALUES (?, ?, ?)
        """, (

            nombre.strip(),
            direccion.strip(),
            telefono.strip()

        ))

        conn.commit()

        return True

    except Exception as e:

        print(
            "Error al crear sucursal:",
            e
        )

        return False

    finally:

        conn.close()


# =====================================================
# OBTENER SUCURSALES
# =====================================================

def obtener_sucursales():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        id,
        nombre,
        direccion,
        telefono

    FROM sucursales

    ORDER BY nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# BUSCAR SUCURSAL POR ID
# =====================================================

def obtener_sucursal_por_id(
    sucursal_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        id,
        nombre,
        direccion,
        telefono

    FROM sucursales

    WHERE id = ?
    """, (

        sucursal_id,

    ))

    resultado = cursor.fetchone()

    conn.close()

    return resultado


# =====================================================
# EDITAR SUCURSAL
# =====================================================

def editar_sucursal(

    sucursal_id,
    nombre,
    direccion,
    telefono

):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE sucursales

    SET

        nombre = ?,
        direccion = ?,
        telefono = ?

    WHERE id = ?
    """, (

        nombre.strip(),
        direccion.strip(),
        telefono.strip(),
        sucursal_id

    ))

    conn.commit()

    conn.close()


# =====================================================
# ELIMINAR SUCURSAL
# =====================================================

def eliminar_sucursal(
    sucursal_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM sucursales

    WHERE id = ?
    """, (

        sucursal_id,

    ))

    conn.commit()

    conn.close()