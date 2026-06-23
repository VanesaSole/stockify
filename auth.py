# auth.py

from database import obtener_conexion
from datetime import datetime


# =====================================================
# LOGIN
# =====================================================

def validar_login(usuario, password):

    conn = obtener_conexion()

    cursor = conn.cursor()

    # ------------------------------------------
    # ADMIN
    # ------------------------------------------

    if usuario.strip().lower() == "admin":

        cursor.execute("""
        SELECT id, nombre, rol
        FROM usuarios
        WHERE rol = 'ADMIN'
        AND password = ?
        AND activo = 1
        """, (password,))

    else:

        cursor.execute("""
        SELECT id, nombre, rol
        FROM usuarios
        WHERE email = ?
        AND password = ?
        AND activo = 1
        """, (

            usuario,
            password

        ))

    resultado = cursor.fetchone()

    conn.close()

    return resultado


# =====================================================
# CREAR USUARIO
# =====================================================

def crear_usuario(

    nombre,
    email,
    password,
    rol,
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
            sucursal_id,
            activo,
            fecha_creacion

        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (

            nombre,
            email,
            password,
            rol,
            sucursal_id,
            1,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        ))

        conn.commit()

        return True

    except Exception as e:

        print(e)

        return False

    finally:

        conn.close()


# =====================================================
# LISTAR USUARIOS
# =====================================================

def obtener_usuarios():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        id,
        nombre,
        email,
        rol,
        activo

    FROM usuarios

    ORDER BY nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# DESACTIVAR USUARIO
# =====================================================

def desactivar_usuario(usuario_id):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET activo = 0
    WHERE id = ?
    """, (usuario_id,))

    conn.commit()

    conn.close()


# =====================================================
# ACTIVAR USUARIO
# =====================================================

def activar_usuario(usuario_id):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios
    SET activo = 1
    WHERE id = ?
    """, (usuario_id,))

    conn.commit()

    conn.close()