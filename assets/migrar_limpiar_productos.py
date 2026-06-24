# migrar_limpiar_productos.py
#
# Script de migración ÚNICA EJECUCIÓN para corregir el problema de
# productos duplicados causado por reimportaciones repetidas del
# catálogo Excel (cada arranque de main.py volvía a insertar todo
# el catálogo porque "codigo" se guardaba siempre como NULL).
#
# QUÉ HACE:
#   1. Hace un backup del .db actual (por seguridad).
#   2. Si detecta movimientos o pedidos ya registrados, AVISA y no
#      borra nada salvo que se confirme explícitamente con --forzar.
#   3. Si la base está “limpia” de pedidos reales (o se fuerza),
#      borra la tabla productos, resetea el autoincrement y
#      reimporta el catálogo Excel desde cero usando la función
#      ya corregida (importar_catalogo_excel), que ahora usa el
#      código real del Excel como clave única.
#
# USO:
#   python migrar_limpiar_productos.py "assets/catalogo.xlsx"
#   python migrar_limpiar_productos.py "assets/catalogo.xlsx" --forzar
#
# El flag --forzar borra los productos aunque ya existan pedidos o
# movimientos en la base (los pedidos/movimientos viejos quedarán
# con producto_id que ya no existe; sus nombres no se podrán mostrar
# en pantallas que dependan del JOIN con productos, pero no se borran
# los pedidos/movimientos en sí).

import sys
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

DB_NAME = "stockify.db"


def hacer_backup():

    origen = Path(DB_NAME)

    if not origen.exists():

        print(f"No se encontró '{DB_NAME}' en esta carpeta. Nada que migrar.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    destino = Path(f"stockify_backup_{timestamp}.db")

    shutil.copy2(origen, destino)

    print(f"Backup creado: {destino}")

    return destino


def contar_filas(cursor, tabla):

    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")

    return cursor.fetchone()[0]


def main():

    if len(sys.argv) < 2:

        print("Uso: python migrar_limpiar_productos.py <ruta_catalogo.xlsx> [--forzar]")
        sys.exit(1)

    ruta_excel = sys.argv[1]

    forzar = "--forzar" in sys.argv[2:]

    if not Path(ruta_excel).exists():

        print(f"ERROR: no se encontró el archivo Excel en '{ruta_excel}'")
        sys.exit(1)

    backup_path = hacer_backup()

    if backup_path is None:
        sys.exit(1)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    productos_antes = contar_filas(cursor, "productos")
    movimientos_count = contar_filas(cursor, "movimientos")
    detalle_pedido_count = contar_filas(cursor, "detalle_pedido")

    print()
    print("=" * 60)
    print(f"Productos actuales en la base : {productos_antes}")
    print(f"Movimientos registrados       : {movimientos_count}")
    print(f"Líneas de detalle_pedido       : {detalle_pedido_count}")
    print("=" * 60)
    print()

    if (movimientos_count > 0 or detalle_pedido_count > 0) and not forzar:

        print(
            "ATENCIÓN: ya existen movimientos o pedidos guardados que "
            "referencian productos actuales.\n"
            "Borrar la tabla 'productos' ahora dejaría esos registros "
            "históricos sin poder mostrar el nombre del producto "
            "(quedarían con producto_id huérfano).\n\n"
            "Si estás seguro de que querés continuar igual, volvé a "
            "correr el script agregando --forzar al final.\n\n"
            "No se modificó nada."
        )

        conn.close()
        sys.exit(0)

    # --- Borrado seguro de productos ---

    cursor.execute("DELETE FROM productos")

    cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name = 'productos'"
    )

    conn.commit()
    conn.close()

    print("Tabla 'productos' vaciada. Reimportando catálogo limpio...\n")

    # Reimportar usando la función ya corregida (codigo real + existencia)
    from inventario import importar_catalogo_excel

    procesados = importar_catalogo_excel(ruta_excel)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    productos_despues = contar_filas(cursor, "productos")

    conn.close()

    print()
    print("=" * 60)
    print("MIGRACIÓN COMPLETADA")
    print("=" * 60)
    print(f"Filas procesadas del Excel : {procesados}")
    print(f"Productos antes            : {productos_antes}")
    print(f"Productos después          : {productos_despues}")
    print(f"Backup disponible en       : {backup_path}")
    print("=" * 60)


if __name__ == "__main__":

    main()