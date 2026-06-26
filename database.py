# database.py

import sqlite3
from datetime import datetime


DB_NAME = "stockify.db"


# =====================================================
# CONEXIÓN
# =====================================================

def obtener_conexion():

    return sqlite3.connect(DB_NAME)


# =====================================================
# CREAR TABLAS
# =====================================================

def crear_tablas():

    conn = obtener_conexion()

    cursor = conn.cursor()

    # ==========================================
    # SUCURSALES
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sucursales (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        direccion TEXT,

        telefono TEXT

    )
    """)

    # ==========================================
    # USUARIOS
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        nombre TEXT NOT NULL,

        email TEXT UNIQUE,

        password TEXT NOT NULL,

        rol TEXT NOT NULL,
        
        direccion TEXT,

        telefono TEXT,

        sucursal_id INTEGER,

        activo INTEGER DEFAULT 1,

        fecha_creacion TEXT,

        FOREIGN KEY (sucursal_id)
        REFERENCES sucursales(id)

    )
    """)

    # ==========================================
    # PRODUCTOS
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        codigo TEXT UNIQUE,

        nombre TEXT NOT NULL,

        stock REAL DEFAULT 0,

        paq INTEGER DEFAULT 1,

        costo REAL DEFAULT 0,

        venta REAL DEFAULT 0,

        mayoreo REAL DEFAULT 0,

        fecha_alta TEXT

    )
    """)

    # ==========================================
    # MOVIMIENTOS
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT NOT NULL,

        usuario_id INTEGER,

        producto_id INTEGER,

        tipo TEXT NOT NULL,

        cantidad REAL NOT NULL,

        observacion TEXT,

        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id),

        FOREIGN KEY (producto_id)
        REFERENCES productos(id)

    )
    """)

    # ==========================================
    # PEDIDOS
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fecha TEXT NOT NULL,

        usuario_id INTEGER,

        sucursal_id INTEGER,

        estado TEXT DEFAULT 'PENDIENTE',

        total REAL DEFAULT 0,

        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id),

        FOREIGN KEY (sucursal_id)
        REFERENCES sucursales(id)

    )
    """)

    # ==========================================
    # DETALLE PEDIDOS
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detalle_pedido (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        pedido_id INTEGER,

        producto_id INTEGER,

        cantidad REAL,

        unidades REAL,

        precio REAL,

        subtotal REAL,

        FOREIGN KEY (pedido_id)
        REFERENCES pedidos(id),

        FOREIGN KEY (producto_id)
        REFERENCES productos(id)

    )
    """)

    conn.commit()

    conn.close()


# =====================================================
# ADMIN POR DEFECTO
# =====================================================

def crear_admin():

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM usuarios
    WHERE rol = 'ADMIN'
    """)

    admin = cursor.fetchone()

    if not admin:

        cursor.execute("""
        INSERT INTO usuarios (

            nombre,
            email,
            password,
            rol,
            activo,
            fecha_creacion

        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (

            "Administrador",
            None,
            "12345",
            "ADMIN",
            1,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        ))

    conn.commit()

    conn.close()

# =====================================================
# SUCURSALES POR DEFECTO
# =====================================================

def crear_sucursales():

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM sucursales")

        cantidad = cursor.fetchone()[0]

        if cantidad == 0:

            sucursales = [

                ("Sucursal Central", "Av. Hipólito Yrigoyen 1994", "11-4000-1000"),

                ("Sucursal Lanús Este", "Av. 9 de Julio 350", "11-4000-1001"),

                ("Sucursal Avellaneda", "Mitre 250", "11-4000-1002"),

                ("Sucursal Lomas de Zamora", "Laprida 120", "11-4000-1003")

            ]

            cursor.executemany("""

            INSERT INTO sucursales(

                nombre,
                direccion,
                telefono

            )

            VALUES (?, ?, ?)

            """, sucursales)

        conn.commit()

        conn.close()
        
# =====================================================
# INICIALIZAR BD
# =====================================================

def inicializar_bd():

    crear_tablas()
    
    crear_sucursales()

    crear_admin()