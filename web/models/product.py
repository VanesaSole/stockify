# app/models/product.py

from ..database import get_db


# -------------------------------------------------------
# LISTAR
# -------------------------------------------------------

def listar_productos(usuario_id, busqueda=""):

    db = get_db()

    if busqueda:
        rows = db.execute("""
            SELECT * FROM productos
            WHERE usuario_id = ? AND activo = 1
            AND nombre LIKE ?
            ORDER BY nombre
        """, (usuario_id, f"%{busqueda}%")).fetchall()
    else:
        rows = db.execute("""
            SELECT * FROM productos
            WHERE usuario_id = ? AND activo = 1
            ORDER BY nombre
        """, (usuario_id,)).fetchall()

    return [dict(r) for r in rows]


# -------------------------------------------------------
# OBTENER UNO
# -------------------------------------------------------

def obtener_producto(producto_id, usuario_id):

    db = get_db()

    row = db.execute("""
        SELECT * FROM productos
        WHERE id = ? AND usuario_id = ?
    """, (producto_id, usuario_id)).fetchone()

    return dict(row) if row else None


# -------------------------------------------------------
# CREAR
# -------------------------------------------------------

def crear_producto(usuario_id, nombre, p_costo, p_venta, p_mayoreo, stock=0):

    db = get_db()

    try:
        cursor = db.execute("""
            INSERT INTO productos (usuario_id, nombre, p_costo, p_venta, p_mayoreo, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (usuario_id, nombre, p_costo, p_venta, p_mayoreo, stock))

        db.commit()
        return {"ok": True, "id": cursor.lastrowid}

    except Exception as e:
        return {"error": str(e)}


# -------------------------------------------------------
# ACTUALIZAR
# -------------------------------------------------------

def actualizar_producto(producto_id, usuario_id, nombre, p_costo, p_venta, p_mayoreo, stock):

    db = get_db()

    db.execute("""
        UPDATE productos
        SET nombre=?, p_costo=?, p_venta=?, p_mayoreo=?, stock=?
        WHERE id=? AND usuario_id=?
    """, (nombre, p_costo, p_venta, p_mayoreo, stock, producto_id, usuario_id))

    db.commit()
    return {"ok": True}


# -------------------------------------------------------
# ELIMINAR (soft delete)
# -------------------------------------------------------

def eliminar_producto(producto_id, usuario_id):

    db = get_db()

    db.execute("""
        UPDATE productos SET activo = 0
        WHERE id = ? AND usuario_id = ?
    """, (producto_id, usuario_id))

    db.commit()
    return {"ok": True}


# -------------------------------------------------------
# CONTAR
# -------------------------------------------------------

def contar_productos(usuario_id):

    db = get_db()

    row = db.execute("""
        SELECT COUNT(*) as total FROM productos
        WHERE usuario_id = ? AND activo = 1
    """, (usuario_id,)).fetchone()

    return row["total"] if row else 0


# -------------------------------------------------------
# IMPORTAR LOTE (desde Excel)
# -------------------------------------------------------

def importar_lote(usuario_id, productos_lista):
    """
    productos_lista: lista de dicts con nombre, p_costo, p_venta, p_mayoreo
    Hace upsert por nombre.
    """
    db = get_db()
    insertados = 0
    actualizados = 0

    for p in productos_lista:

        existing = db.execute("""
            SELECT id FROM productos
            WHERE usuario_id = ? AND nombre = ?
        """, (usuario_id, p["nombre"])).fetchone()

        if existing:
            db.execute("""
                UPDATE productos
                SET p_costo=?, p_venta=?, p_mayoreo=?, activo=1
                WHERE id=?
            """, (p["p_costo"], p["p_venta"], p["p_mayoreo"], existing["id"]))
            actualizados += 1
        else:
            db.execute("""
                INSERT INTO productos (usuario_id, nombre, p_costo, p_venta, p_mayoreo)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario_id, p["nombre"], p["p_costo"], p["p_venta"], p["p_mayoreo"]))
            insertados += 1

    db.commit()
    return {"insertados": insertados, "actualizados": actualizados}