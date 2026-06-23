import tkinter as tk
from tkinter import ttk

from historial import obtener_historial

from tema import *


class VentanaHistorial(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Historial")

        self.geometry("1400x850")

        self.configure(
            bg=COLOR_FONDO
        )

        self.crear_widgets()

        self.cargar_datos()

        self.bind(

            "<Escape>",

            lambda e: self.destroy()

        )
        
# ====================================
# WIDGETS
# ====================================

    def crear_widgets(self):

        # LOGO

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo.png"
            )

            self.logo = self.logo.subsample(5, 5)

            tk.Label(

                self,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(

                pady=(10,5)

            )

        except:

            pass


        # TITULO

        tk.Label(

            self,

            text="HISTORIAL",

            bg=COLOR_FONDO,

            fg=COLOR_GRIS,

            font=FUENTE_TITULO

        ).pack(

            pady=(0,10)

        )


        # BOTONES

        frame_superior = tk.Frame(

            self,

            bg=COLOR_FONDO

        )

        frame_superior.pack(

            fill="x",

            padx=10,

            pady=10

        )


        tk.Button(

            frame_superior,

            text="Actualizar",

            bg=COLOR_AZUL,

            fg="white",

            font=FUENTE_BOTON,

            command=self.cargar_datos

        ).pack(

            side="left",

            padx=5

        )


        tk.Button(

            frame_superior,

            text="Cerrar",

            bg=COLOR_ROJO,

            fg="white",

            font=FUENTE_BOTON,

            command=self.destroy

        ).pack(

            side="left",

            padx=5

        )


        # TABLA

        columnas = (

            "ID",

            "Fecha",

            "Usuario",

            "Producto",

            "Tipo",

            "Cantidad",

            "Observación"

        )

        self.tree = ttk.Treeview(

            self,

            columns=columnas,

            show="headings"

        )

        for col in columnas:

            self.tree.heading(

                col,

                text=col

            )

            self.tree.column(

                col,

                width=150

            )

        self.tree.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )


    # ====================================
    # CARGAR DATOS
    # ====================================

    def cargar_datos(self):

        for fila in self.tree.get_children():

            self.tree.delete(

                fila

            )

        datos = obtener_historial()

        for fila in datos:

            self.tree.insert(

                "",

                "end",

                values=fila

            )