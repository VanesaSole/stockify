# historial.py

from database import obtener_conexion
from datetime import datetime


# =====================================================
# REGISTRAR MOVIMIENTO
# =====================================================

def registrar_movimiento(

    usuario_id,
    producto_id,
    tipo,
    cantidad,
    observacion=""

):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO movimientos (

        fecha,
        usuario_id,
        producto_id,
        tipo,
        cantidad,
        observacion

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        usuario_id,

        producto_id,

        tipo.upper(),

        cantidad,

        observacion

    ))

    conn.commit()

    conn.close()


# =====================================================
# OBTENER HISTORIAL COMPLETO
# =====================================================

def obtener_historial():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        m.id,

        m.fecha,

        u.nombre,

        p.nombre,

        m.tipo,

        m.cantidad,

        m.observacion

    FROM movimientos m

    LEFT JOIN usuarios u
    ON m.usuario_id = u.id

    LEFT JOIN productos p
    ON m.producto_id = p.id

    ORDER BY m.fecha DESC

    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# HISTORIAL DE PRODUCTO
# =====================================================

def obtener_historial_producto(
    producto_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        m.fecha,

        u.nombre,

        m.tipo,

        m.cantidad,

        m.observacion

    FROM movimientos m

    LEFT JOIN usuarios u
    ON m.usuario_id = u.id

    WHERE m.producto_id = ?

    ORDER BY m.fecha DESC

    """, (

        producto_id,

    ))

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# HISTORIAL DE USUARIO
# =====================================================

def obtener_historial_usuario(
    usuario_id
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        m.fecha,

        p.nombre,

        m.tipo,

        m.cantidad,

        m.observacion

    FROM movimientos m

    LEFT JOIN productos p
    ON m.producto_id = p.id

    WHERE m.usuario_id = ?

    ORDER BY m.fecha DESC

    """, (

        usuario_id,

    ))

    datos = cursor.fetchall()

    conn.close()

    return datos

# =====================================================
# HISTORIAL POR TIPO
# =====================================================

def obtener_historial_tipo(
    tipo
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        m.fecha,

        u.nombre,

        p.nombre,

        m.cantidad,

        m.observacion

    FROM movimientos m

    LEFT JOIN usuarios u
    ON m.usuario_id = u.id

    LEFT JOIN productos p
    ON m.producto_id = p.id

    WHERE m.tipo = ?

    ORDER BY m.fecha DESC

    """, (

        tipo.upper(),

    ))

    datos = cursor.fetchall()

    conn.close()

    return datos


# =====================================================
# ULTIMOS MOVIMIENTOS
# =====================================================

def obtener_ultimos_movimientos(
    limite=20
):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        m.fecha,

        u.nombre,

        p.nombre,

        m.tipo,

        m.cantidad,

        m.observacion

    FROM movimientos m

    LEFT JOIN usuarios u
    ON m.usuario_id = u.id

    LEFT JOIN productos p
    ON m.producto_id = p.id

    ORDER BY m.fecha DESC

    LIMIT ?

    """, (

        limite,

    ))

    datos = cursor.fetchall()

    conn.close()

    return datos
