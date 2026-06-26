# usuarios.py

from database import obtener_conexion

from datetime import datetime


# =====================================================
# CREAR USUARIO
# =====================================================

def crear_usuario(

    nombre,
    email,
    password,
    rol,
    direccion,
    telefono,
    sucursal_id

):

    conn = obtener_conexion()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO usuarios (

            nombre,
            email,
            password,
            rol,
            direccion,
            telefono,
            sucursal_id,
            activo,
            fecha_creacion

        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

        nombre.strip(),

        email.strip().lower(),

        password,

        rol,

        direccion.strip(),

        telefono.strip(),

        sucursal_id,

        1,

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    ))

        conn.commit()

        return True

    except Exception as e:

        print(
            "Error al crear usuario:",
            e
        )

        return False

    finally:

        conn.close()


# =====================================================
# OBTENER TODOS
# =====================================================

def obtener_usuarios():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        u.id,
        u.nombre,
        u.email,
        u.rol,
        s.nombre,
        u.activo

    FROM usuarios u

    LEFT JOIN sucursales s
    ON u.sucursal_id = s.id

    ORDER BY u.nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# BUSCAR POR ID
# =====================================================

def obtener_usuario_por_id(
    usuario_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *

    FROM usuarios

    WHERE id = ?
    """, (

        usuario_id,

    ))

    usuario = cursor.fetchone()

    conn.close()

    return usuario


# =====================================================
# ACTIVAR
# =====================================================

def activar_usuario(
    usuario_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios

    SET activo = 1

    WHERE id = ?
    """, (

        usuario_id,

    ))

    conn.commit()

    conn.close()


# =====================================================
# DESACTIVAR
# =====================================================

def desactivar_usuario(
    usuario_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios

    SET activo = 0

    WHERE id = ?
    """, (

        usuario_id,

    ))

    conn.commit()

    conn.close()


# =====================================================
# CAMBIAR ROL
# =====================================================

def cambiar_rol(

    usuario_id,
    nuevo_rol

):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios

    SET rol = ?

    WHERE id = ?
    """, (

        nuevo_rol,
        usuario_id

    ))

    conn.commit()

    conn.close()