# main.py

from database import inicializar_bd
from ui_login import VentanaLogin


def main():

    try:

        # Crear tablas y admin por defecto
        inicializar_bd()
        
        from inventario import importar_catalogo_excel

        importar_catalogo_excel(
            "assets/catalogo.xlsx"
        ) 
        # Abrir aplicación
        VentanaLogin()

    except Exception as e:

        print("\n==============================")
        print("ERROR EN STOCKIFY V2")
        print("==============================\n")

        print(type(e).__name__)
        print(e)

        input("\nPresione ENTER para salir...")


if __name__ == "__main__":

    main()