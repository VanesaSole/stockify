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
            bg=COLOR_TOPO
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

                bg=COLOR_TOPO

            ).pack(

                pady=(10,5)

            )

        except:

            pass


        # TITULO

        tk.Label(

            self,

            text="HISTORIAL",

            bg=COLOR_TOPO,

            fg=COLOR_BLANCO,

            font=FUENTE_TITULO

        ).pack(

            pady=(0,10)

        )


        # BOTONES

        frame_superior = tk.Frame(

            self,

            bg=COLOR_TOPO

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

        style = ttk.Style(self)
        try:
            style.theme_use('clam')
        except Exception:
            pass
        style.configure(
            'Top.Treeview',
            background=COLOR_TOPO,
            fieldbackground=COLOR_TOPO,
            foreground=COLOR_BLANCO,
            rowheight=28,
            bordercolor=COLOR_GRIS,
            lightcolor=COLOR_GRIS,
            darkcolor=COLOR_GRIS
        )
        style.configure(
            'Top.Treeview.Heading',
            background="#4D5258",
            foreground=COLOR_BLANCO,
            relief='flat'
        )
        style.map(
            'Top.Treeview',
            background=[('selected', COLOR_CELESTE)],
            foreground=[('selected', COLOR_BLANCO)]
        )

        columnas = (

            "ID",

            "Fecha",

            "Usuario",

            "Producto",

            "Tipo",

            "Cantidad",

            "Observación"

        )

        frame_tabla = tk.Frame(self, bg=COLOR_TOPO)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(

            frame_tabla,

            columns=columnas,

            show="headings",

            style='Top.Treeview'

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

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(

            side="left",

            fill="both",

            expand=True

        )
        scrollbar.pack(side="right", fill="y")


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