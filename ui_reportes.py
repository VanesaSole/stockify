import tkinter as tk
from tkinter import ttk

from tema import *


class VentanaReportes(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Reportes")

        self.geometry("1400x850")

        self.configure(
            bg=COLOR_FONDO
        )

        self.crear_widgets()

        self.bind(

            "<Escape>",

            lambda e: self.destroy()

        )
        
# ======================================
# WIDGETS
# ======================================

    def crear_widgets(self):

        # LOGO

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo3.png"
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

            text="REPORTES",

            bg=COLOR_FONDO,

            fg=COLOR_CELESTE,

            font=FUENTE_TITULO

        ).pack(

            pady=(0,10)

        )


        notebook = ttk.Notebook(self)

        notebook.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )


        # STOCK BAJO

        frame_stock_bajo = ttk.Frame(notebook)

        notebook.add(

            frame_stock_bajo,

            text="Stock Bajo"

        )

        columnas_stock = (

            "ID",

            "Producto",

            "Stock"

        )

        self.tree_stock_bajo = ttk.Treeview(

            frame_stock_bajo,

            columns=columnas_stock,

            show="headings"

        )

        for col in columnas_stock:

            self.tree_stock_bajo.heading(

                col,

                text=col

            )

        self.tree_stock_bajo.pack(

            fill="both",

            expand=True

        )


        # SIN STOCK

        frame_sin_stock = ttk.Frame(notebook)

        notebook.add(

            frame_sin_stock,

            text="Sin Stock"

        )

        columnas_sin_stock = (

            "ID",

            "Producto"

        )

        self.tree_sin_stock = ttk.Treeview(

            frame_sin_stock,

            columns=columnas_sin_stock,

            show="headings"

        )

        for col in columnas_sin_stock:

            self.tree_sin_stock.heading(

                col,

                text=col

            )

        self.tree_sin_stock.pack(

            fill="both",

            expand=True

        )


        # MAS VENDIDOS

        frame_mas_vendidos = ttk.Frame(notebook)

        notebook.add(

            frame_mas_vendidos,

            text="Más Vendidos"

        )

        columnas_mas_vendidos = (

            "Producto",

            "Cantidad"

        )

        self.tree_mas_vendidos = ttk.Treeview(

            frame_mas_vendidos,

            columns=columnas_mas_vendidos,

            show="headings"

        )

        for col in columnas_mas_vendidos:

            self.tree_mas_vendidos.heading(

                col,

                text=col

            )

        self.tree_mas_vendidos.pack(

            fill="both",

            expand=True

        )


        # BOTONES

        frame_botones = tk.Frame(

            self,

            bg=COLOR_FONDO

        )

        frame_botones.pack(

            pady=10

        )


        tk.Button(

            frame_botones,

            text="Actualizar",

            bg=COLOR_CELESTE,

            fg="white",

            font=FUENTE_BOTON,

            command=self.actualizar

        ).pack(

            side="left",

            padx=10

        )


        tk.Button(

            frame_botones,

            text="Cerrar",

            bg=COLOR_ROJO,

            fg="white",

            font=FUENTE_BOTON,

            command=self.destroy

        ).pack(

            side="left",

            padx=10

        )


    # ======================================
    # ACTUALIZAR
    # ======================================

    def actualizar(self):

        print(

            "Actualizar reportes"

        )