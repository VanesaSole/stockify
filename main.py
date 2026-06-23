# main.py

from database import inicializar_bd, obtener_conexion
from ui_login import VentanaLogin


def main():
    try:

        # Crear tablas y admin por defecto
        inicializar_bd()
        
        # ===================================
        # IMPORTAR CATÁLOGO (SOLO SI VACÍO)
        # ===================================
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]
        conn.close()
        
        # Si no hay productos, importar del Excel
        if total_productos == 0:
            from inventario import importar_catalogo_excel
            print("Importando catálogo desde Excel...")
            importar_catalogo_excel("assets/catalogo.xlsx")
            print("Catálogo importado correctamente.")
        
        # Abrir aplicación
        VentanaLogin()

    except KeyboardInterrupt:
        # Manejo limpio de interrupción por teclado (Ctrl+C)
        print("\nInterrupción por teclado. Saliendo...")
    except Exception as e:

        print("\n==============================")
        print("ERROR EN STOCKIFY V2")
        print("==============================\n")

        print(type(e).__name__)
        print(e)

        input("\nPresione ENTER para salir...")


if __name__ == "__main__":

    main()