# auth.py

from database import conectar


# =====================================================
# REGISTRAR USUARIO
# =====================================================

def registrar_usuario(
    nombre,
    email,
    password,
    direccion,
    telefono
):

    conn, cursor = conectar()

    try:

        cursor.execute("""

        INSERT INTO usuarios (
            nombre,
            email,
            password,
            direccion,
            telefono
        )

        VALUES (?, ?, ?, ?, ?)

        """, (

            nombre,
            email,
            password,
            direccion,
            telefono

        ))

        conn.commit()

        conn.close()

        return True

    except Exception as e:

        conn.close()

        return str(e)


# =====================================================
# LOGIN
# =====================================================

def iniciar_sesion(
    email,
    password
):

    conn, cursor = conectar()

    cursor.execute("""

    SELECT * FROM usuarios
    WHERE email = ?
    AND password = ?

    """, (

        email,
        password

    ))

    usuario = cursor.fetchone()

    conn.close()

    return usuario