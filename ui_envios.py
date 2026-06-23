import tkinter as tk
from tkinter import ttk, messagebox

from pedidos import Pedido
from inventario import buscar_productos
from boleta import generar_remito_verde

from tema import *


class VentanaEnvios(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Nuevo Envío")

        self.geometry("1400x850")

        self.configure(
            bg=COLOR_FONDO
        )

        self.pedido = Pedido()

        # Variables

        self.var_busqueda = tk.StringVar()

        self.var_cantidad = tk.IntVar(
            value=1
        )

        self.var_tipo = tk.StringVar(
            value="UNIDAD"
        )

        self.producto_id_seleccionado = None

        self.crear_widgets()

        # Búsqueda automática

        self.var_busqueda.trace_add(

            "write",

            self.actualizar_resultados

        )

        # Atajos

        self.bind(

            "<Escape>",

            lambda e: self.destroy()

        )

        self.bind(

            "<Delete>",

            lambda e: self.eliminar_seleccionado()

        )

        self.bind(

            "<Control-s>",

            lambda e: self.guardar_envio()

        )

        self.bind(

            "<F5>",

            lambda e: self.generar_pdf()

        )

        self.tree_resultados.bind(

            "<Double-1>",

            lambda e: self.agregar_producto()

        )

        self.actualizar_resultados()
        
        
    # ==================================
    # WIDGETS
    # ==================================

    def crear_widgets(self):

        # ==========================
        # LOGO
        # ==========================

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo2.png"
            )

            self.logo = self.logo.subsample(5, 5)

            tk.Label(

                self,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(

                pady=(10, 5)

            )

        except:

            pass


        # ==========================
        # TITULO
        # ==========================

        tk.Label(

            self,

            text="NUEVO ENVÍO",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=FUENTE_TITULO

        ).pack(

            pady=(0, 10)

        )


        # ==========================
        # BUSQUEDA
        # ==========================

        frame_busqueda = tk.LabelFrame(

            self,

            text="Buscar producto",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=FUENTE_SUBTITULO

        )

        frame_busqueda.pack(

            fill="x",

            padx=10,

            pady=5

        )

        self.entry_busqueda = ttk.Entry(

            frame_busqueda,

            textvariable=self.var_busqueda,

            width=70

        )

        self.entry_busqueda.pack(

            padx=10,

            pady=10,

            ipady=4

        )


        # ==========================
        # PRODUCTOS
        # ==========================

        frame_resultados = tk.LabelFrame(

            self,

            text="Productos",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=FUENTE_SUBTITULO

        )

        frame_resultados.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=5

        )

        columnas = (

            "ID",

            "Producto",

            "Stock",

            "Paq",

            "Costo"

        )

        self.tree_resultados = ttk.Treeview(

            frame_resultados,

            columns=columnas,

            show="headings",

            height=10

        )

        for col in columnas:

            self.tree_resultados.heading(

                col,

                text=col

            )

        self.tree_resultados.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )


        # ==========================
        # AGREGAR
        # ==========================

        frame_agregar = tk.LabelFrame(

            self,

            text="Agregar producto",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=FUENTE_SUBTITULO

        )

        frame_agregar.pack(

            fill="x",

            padx=10,

            pady=5

        )


        tk.Label(

            frame_agregar,

            text="Cantidad",

            bg=COLOR_FONDO,

            font=FUENTE_NORMAL

        ).pack(

            side="left",

            padx=10

        )


        ttk.Entry(

            frame_agregar,

            textvariable=self.var_cantidad,

            width=8

        ).pack(

            side="left",

            padx=5

        )


        ttk.Combobox(

            frame_agregar,

            textvariable=self.var_tipo,

            values=[

                "UNIDAD",

                "BULTO"

            ],

            width=12

        ).pack(

            side="left",

            padx=10

        )


        tk.Button(

            frame_agregar,

            text="AGREGAR",

            bg=COLOR_VERDE,

            fg="white",

            font=FUENTE_BOTON,

            command=self.agregar_producto

        ).pack(

            side="left",

            padx=15

        )


        # ==========================
        # ENVIO ACTUAL
        # ==========================

        frame_envio = tk.LabelFrame(

            self,

            text="Envío actual",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=FUENTE_SUBTITULO

        )

        frame_envio.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=5

        )


        columnas2 = (

            "ID",

            "Producto",

            "Tipo",

            "Cantidad",

            "Unidades",

            "Precio",

            "Subtotal"

        )


        self.tree_envio = ttk.Treeview(

            frame_envio,

            columns=columnas2,

            show="headings",

            height=10

        )


        for col in columnas2:

            self.tree_envio.heading(

                col,

                text=col

            )


        self.tree_envio.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )


        # ==========================
        # TOTAL
        # ==========================

        self.lbl_total = tk.Label(

            self,

            text="TOTAL: $0,00",

            bg=COLOR_FONDO,

            fg=COLOR_VERDE,

            font=(

                "Segoe UI",

                22,

                "bold"

            )

        )

        self.lbl_total.pack(

            pady=10

        )


        # ==========================
        # BOTONES
        # ==========================

        frame_botones = tk.Frame(

            self,

            bg=COLOR_FONDO

        )

        frame_botones.pack(

            pady=15

        )


        tk.Button(

            frame_botones,

            text="GUARDAR",

            bg=COLOR_VERDE,

            fg="white",

            width=15,

            font=FUENTE_BOTON,

            command=self.guardar_envio

        ).pack(

            side="left",

            padx=10

        )


        tk.Button(

            frame_botones,

            text="GENERAR PDF",

            bg=COLOR_CELESTE,

            fg="white",

            width=15,

            font=FUENTE_BOTON,

            command=self.generar_pdf

        ).pack(

            side="left",

            padx=10

        )


        tk.Button(

            frame_botones,

            text="VACIAR",

            bg=COLOR_ROJO,

            fg="white",

            width=15,

            font=FUENTE_BOTON,

            command=self.vaciar_envio

        ).pack(

            side="left",

            padx=10

        )
    

    # ==================================
    # FUNCIONES
    # ==================================

# ==================================
# FUNCIONES
# ==================================

    def actualizar_resultados(self, *args):

        for fila in self.tree_resultados.get_children():

            self.tree_resultados.delete(fila)

        texto = self.var_busqueda.get()

        productos = buscar_productos(texto)

        for producto in productos:

            self.tree_resultados.insert(

                "",

                "end",

                values=(

                    producto[0],

                    producto[1],

                    producto[2],

                    producto[3],

                    producto[4]

                )

            )


    # ==================================
    # SELECCIONAR PRODUCTO
    # ==================================

    def seleccionar_producto(self, event=None):

        seleccionado = self.tree_resultados.focus()

        if not seleccionado:

            return

        datos = self.tree_resultados.item(

            seleccionado,

            "values"

        )

        self.producto_id_seleccionado = int(

            datos[0]

        )


    # ==================================
    # AGREGAR PRODUCTO
    # ==================================

    def agregar_producto(self):

        seleccionado = self.tree_resultados.focus()

        if not seleccionado:

            messagebox.showwarning(

                "Stockify",

                "Seleccione un producto"

            )

            return

        datos = self.tree_resultados.item(

            seleccionado,

            "values"

        )

        producto_id = int(

            datos[0]

        )

        self.pedido.agregar_producto(

            producto_id,

            self.var_cantidad.get(),

            self.var_tipo.get()

        )

        self.actualizar_envio()

        self.var_cantidad.set(

            1

        )


    # ==================================
    # ACTUALIZAR ENVIO
    # ==================================

    def actualizar_envio(self):

        for fila in self.tree_envio.get_children():

            self.tree_envio.delete(

                fila

            )

        for item in self.pedido.obtener_items():

            self.tree_envio.insert(

                "",

                "end",

                values=(

                    item["producto_id"],

                    item["nombre"],

                    item["tipo"],

                    item["cantidad"],

                    item["unidades"],

                    item["precio"],

                    item["subtotal"]

                )

            )

        total = self.pedido.calcular_total()

        self.lbl_total.config(

            text=f"TOTAL: ${total:,.2f}"

        )


    # ==================================
    # ELIMINAR
    # ==================================

    def eliminar_seleccionado(self):

        seleccionado = self.tree_envio.focus()

        if not seleccionado:

            return

        indice = self.tree_envio.index(

            seleccionado

        )

        self.pedido.eliminar_producto(

            indice

        )

        self.actualizar_envio()


    # ==================================
    # VACIAR
    # ==================================

    def vaciar_envio(self):

        self.pedido.vaciar()

        self.actualizar_envio()

        self.var_cantidad.set(

            1

        )

        self.var_tipo.set(

            "UNIDAD"

        )


    # ==================================
    # GUARDAR
    # ==================================

    def guardar_envio(self):

        messagebox.showinfo(

            "Stockify",

            "Guardar envío pendiente"

        )


    # ==================================
    # PDF
    # ==================================

    def generar_pdf(self):

        try:

            generar_remito_verde(

                self.pedido.obtener_items()

            )

            messagebox.showinfo(

                "Stockify",

                "PDF generado"

            )

        except Exception as e:

            messagebox.showerror(

                "Error",

                str(e)

            )