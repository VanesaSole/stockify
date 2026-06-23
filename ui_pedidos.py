# ui_pedidos.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from pedidos import Pedido
from inventario import buscar_productos, obtener_producto
from boleta import generar_pedido_azul
import os

from tema import *


class VentanaPedidos(tk.Toplevel):

    def __init__(self, master=None, usuario=None):

        super().__init__(master)

        self.title("Nuevo Pedido")

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = min(1200, int(screen_width * 0.95))
        window_height = min(820, int(screen_height * 0.85))
        self.geometry(f"{window_width}x{window_height}")
        self.minsize(900, 620)
        self.maxsize(window_width, window_height)
        # ancho efectivo para contener los frames centrados
        self._main_width = window_width

        self.configure(
            bg=COLOR_FONDO
        )

        # usuario = (id, nombre, rol) según auth.validar_login
        self.usuario = usuario

        self.pedido = Pedido()

        # Variables

        self.var_busqueda = tk.StringVar()

        self.var_cantidad = tk.IntVar(value=1)

        self.var_tipo = tk.StringVar(value="UNIDAD")

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

            lambda e: self.guardar_pedido()

        )

        self.bind(

            "<F5>",

            lambda e: self.guardar_pedido()

        )

        self.tree_resultados.bind(

            "<Double-1>",

            lambda e: self.agregar_producto()

        )

        self.tree_resultados.bind(

            "<Return>",

            lambda e: self.ir_a_cantidad()

        )

        self.entry_cantidad.bind(

            "<Return>",

            lambda e: self.confirmar_cantidad()

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
                file="assets/logo.png"
            )
            self.logo = self.logo.subsample(8, 8)

            tk.Label(

                self,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(
                pady=(10,5)
            )

        except:

            pass


        # ==========================
        # TITULO
        # ==========================

        tk.Label(

            self,

            text="NUEVO PEDIDO",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_TITULO

        ).pack(
            pady=(0,10)
        )

        # Contenedor centrado (ancho fijo relativo, pero con expansión vertical)
        main_frame_width = int(self._main_width * 0.95)
        self.main_frame = tk.Frame(self, bg=COLOR_FONDO, width=main_frame_width)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



        # ==========================
        # BUSQUEDA
        # ==========================

        frame_busqueda = tk.LabelFrame(

            self.main_frame,

            text="Buscar producto",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

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

            self.main_frame,

            text="Productos",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_SUBTITULO

        )

        frame_resultados.pack(

            fill="x",

            expand=False,

            padx=10,

            pady=3

        )

        columnas = (

            "ID",

            "Producto",

            "Stock",

            "Paq",

            "Costo"

        )

        # Contenedor para Treeview + scrollbar
        frame_tree_results = tk.Frame(frame_resultados, bg=COLOR_FONDO)
        frame_tree_results.pack(fill="both", expand=True, padx=6, pady=6)

        self.tree_resultados = ttk.Treeview(

            frame_tree_results,

            columns=columnas,

            show="headings",

            height=7

        )

        scrollbar_res = ttk.Scrollbar(frame_tree_results, orient="vertical", command=self.tree_resultados.yview)
        self.tree_resultados.configure(yscrollcommand=scrollbar_res.set)

        for col in columnas:

            self.tree_resultados.heading(

                col,

                text=col

            )

        self.tree_resultados.pack(side="left", fill="both", expand=True)
        scrollbar_res.pack(side="right", fill="y")
        


    # ==========================
    # AGREGAR
    # ==========================

        frame_agregar = tk.LabelFrame(

            self.main_frame,

            text="Agregar producto",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_SUBTITULO

        )

        frame_agregar.pack(

            fill="x",

            padx=10,

            pady=3

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


        self.entry_cantidad = ttk.Entry(

            frame_agregar,

            textvariable=self.var_cantidad,

            width=8

        )

        self.entry_cantidad.pack(

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

        self.lbl_ultimo_agregado = tk.Label(

            frame_agregar,

            text="",

            bg=COLOR_FONDO,

            fg=COLOR_GRIS,

            font=FUENTE_NORMAL

        )

        self.lbl_ultimo_agregado.pack(

            side="left",

            padx=15

        )


        # ==========================
        # PEDIDO ACTUAL (FRAME CONTENEDOR)
        # ==========================

        frame_pedido_contenedor = tk.LabelFrame(

            self.main_frame,

            text="Pedido actual",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_SUBTITULO

        )

        frame_pedido_contenedor.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5,
            ipady=5
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


        # Frame para el treeview con scrollbar
        frame_tree_scroll = tk.Frame(frame_pedido_contenedor, bg=COLOR_FONDO)
        frame_tree_scroll.pack(fill="both", expand=True, padx=10, pady=8)


        # Scrollbar
        scrollbar_pedido = ttk.Scrollbar(frame_tree_scroll)
        scrollbar_pedido.pack(side="right", fill="y")

        self.tree_pedido = ttk.Treeview(

            frame_tree_scroll,

            columns=columnas2,

            show="headings",

            height=8,

            yscrollcommand=scrollbar_pedido.set

        )

        
        scrollbar_pedido.config(command=self.tree_pedido.yview)


        # Configurar columnas con widths
        anchos = {
            "ID": 40,
            "Producto": 300,
            "Tipo": 60,
            "Cantidad": 70,
            "Unidades": 80,
            "Precio": 80,
            "Subtotal": 100
        }

        for col in columnas2:

            self.tree_pedido.heading(

                col,

                text=col

            )
            
            self.tree_pedido.column(
                col,
                width=anchos.get(col, 80),
                anchor="center"
            )


        self.tree_pedido.pack(

            fill="both",

            expand=True

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

                16,

                "bold"

            )

        )

        self.lbl_total.pack(

            pady=10,

            fill="x"

        )


        # ==========================
        # BOTONES
        # ==========================

        frame_botones = tk.Frame(

            self.main_frame,

            bg=COLOR_FONDO

        )

        frame_botones.pack(

            pady=15,

            fill="x"

        )


        tk.Button(

            frame_botones,

            text="finalizar pedido",

            bg=COLOR_AZUL,

            fg="white",

            width=25,

            font=FUENTE_BOTON,

            command=self.guardar_pedido

        ).pack(

            side="left",

            padx=15

        )


        tk.Button(

            frame_botones,


            text="🗑 VACIAR",

            bg=COLOR_ROJO,

            fg="white",

            width=15,

            font=FUENTE_BOTON,

            command=self.vaciar_pedido

        ).pack(

            side="left",

            padx=15,

            expand=True

        )
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
    # OBTENER PRODUCTO SELECCIONADO (helper)
    # ==================================

    def _obtener_producto_id_seleccionado(self):

        seleccionado = self.tree_resultados.selection()

        if not seleccionado:

            seleccionado_focus = self.tree_resultados.focus()

            if seleccionado_focus:

                seleccionado = (seleccionado_focus,)

        if not seleccionado:

            return None

        datos = self.tree_resultados.item(

            seleccionado[0],

            "values"

        )

        if not datos:

            return None

        try:

            return int(datos[0])

        except (ValueError, TypeError):

            return None


    # ==================================
    # ENTER EN LA LISTA -> IR A CANTIDAD
    # ==================================

    def ir_a_cantidad(self):

        producto_id = self._obtener_producto_id_seleccionado()

        if producto_id is None:

            messagebox.showwarning(

                "Stockify",

                "Seleccione un producto"

            )

            return "break"

        self.entry_cantidad.focus_set()

        self.entry_cantidad.selection_range(0, tk.END)

        return "break"


    # ==================================
    # ENTER EN CANTIDAD -> CONFIRMAR LINEA
    # ==================================

    def confirmar_cantidad(self):

        self.agregar_producto()

        # vuelve el foco al buscador para cargar el próximo producto
        self.entry_busqueda.focus_set()

        return "break"


    # ==================================
    # AGREGAR PRODUCTO
    # ==================================

    def agregar_producto(self):

        producto_id = self._obtener_producto_id_seleccionado()

        if producto_id is None:

            messagebox.showwarning(

                "Stockify",

                "Seleccione un producto"

            )

            return

        try:

            cantidad = float(

                str(self.var_cantidad.get()).replace(",", ".")

            )

        except (ValueError, tk.TclError):

            messagebox.showwarning(

                "Stockify",

                "Cantidad inválida"

            )

            return

        if cantidad <= 0:

            messagebox.showwarning(

                "Stockify",

                "La cantidad debe ser mayor a cero"

            )

            return

        # ======================================
        # VALIDAR STOCK ANTES DE AGREGAR
        # ======================================

        producto = obtener_producto(producto_id)

        if not producto:

            messagebox.showerror(

                "Stockify",

                "Producto no encontrado"

            )

            return

        nombre_producto = producto[2]

        stock_actual = producto[3]

        paq = producto[4]

        if stock_actual is None or stock_actual <= 0:

            messagebox.showwarning(

                "Stockify",

                f"No se puede agregar:\n\n"
                f"\"{nombre_producto}\" (ID {producto_id})\n\n"
                f"No tiene stock disponible (stock: {stock_actual})."

            )

            return

        tipo = self.var_tipo.get()

        try:

            paq = int(paq)

        except (ValueError, TypeError):

            paq = 1

        unidades_pedidas = cantidad * paq if tipo.upper() == "BULTO" else cantidad

        # Si el mismo producto ya está en el carrito (pedido actual, aún
        # no descontado de la BD), sumamos sus unidades para no permitir
        # que dos líneas independientes superen el stock real entre ambas.
        unidades_ya_en_carrito = sum(

            item["unidades"]

            for item in self.pedido.obtener_items()

            if item["producto_id"] == producto_id

        )

        unidades_disponibles = stock_actual - unidades_ya_en_carrito

        if unidades_pedidas > unidades_disponibles:

            messagebox.showwarning(

                "Stockify",

                f"No hay suficiente stock:\n\n"
                f"\"{nombre_producto}\" (ID {producto_id})\n\n"
                f"Stock disponible: {unidades_disponibles:g} unidades\n"
                f"Cantidad solicitada: {unidades_pedidas:g} unidades"

            )

            return

        agregado = self.pedido.agregar_producto(

            producto_id,

            cantidad,

            tipo

        )

        if not agregado:

            messagebox.showerror(

                "Stockify",

                "No se pudo agregar el producto (no encontrado)"

            )

            return

        self.actualizar_pedido()

        # Confirmación visual: clave cuando hay productos con el mismo
        # nombre pero distinto ID (catálogos con duplicados).
        self.lbl_ultimo_agregado.config(

            text=(

                f"Agregado: {nombre_producto} (ID {producto_id}) "
                f"— {cantidad:g} {tipo}"

            )

        )

        self.var_cantidad.set(1)


    # ==================================
    # ACTUALIZAR PEDIDO
    # ==================================

    def actualizar_pedido(self):

        for fila in self.tree_pedido.get_children():

            self.tree_pedido.delete(

                fila

            )

        for item in self.pedido.obtener_items():

            # Formatear valores para visualización
            precio_formateado = f"${item['precio']:,.0f}"
            subtotal_formateado = f"${item['subtotal']:,.0f}"
            cantidad_formateada = f"{item['cantidad']:g}"
            unidades_formateadas = f"{item['unidades']:g}"

            self.tree_pedido.insert(

                "",

                "end",

                values=(

                    item["producto_id"],

                    item["nombre"],

                    item["tipo"],

                    cantidad_formateada,

                    unidades_formateadas,

                    precio_formateado,

                    subtotal_formateado

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

        seleccionado = self.tree_pedido.focus()

        if not seleccionado:

            return

        indice = self.tree_pedido.index(

            seleccionado

        )

        self.pedido.eliminar_producto(

            indice

        )

        self.actualizar_pedido()


    # ==================================
    # VACIAR
    # ==================================

    def vaciar_pedido(self):

        self.pedido.vaciar()

        self.actualizar_pedido()

        self.var_cantidad.set(

            1

        )

        self.var_tipo.set(

            "UNIDAD"

        )

        self.lbl_ultimo_agregado.config(text="")


    # ==================================
    # GUARDAR Y GENERAR PEDIDO (BD + STOCK + HISTORIAL + PDF)
    # ==================================

    def guardar_pedido(self):

        items = self.pedido.obtener_items()

        if not items:

            messagebox.showwarning(

                "Stockify",

                "No hay productos en el pedido"

            )

            return

        if not self.usuario:

            messagebox.showerror(

                "Stockify",

                "No se pudo identificar al usuario de la sesión"

            )

            return

        usuario_id = self.usuario[0]

        nombre_usuario = self.usuario[1]

        # La sesión actual (auth.validar_login) no devuelve sucursal_id;
        # se guarda como None hasta que el login provea ese dato.
        sucursal_id = None

        confirmar = messagebox.askyesno(

            "Confirmar",

            "¿Finalizar el pedido? Esto va a:\n\n"
            "• Guardar el pedido en el sistema\n"
            "• Descontar el stock de los productos\n"
            "• Registrar el movimiento en el historial\n"
            "• Generar el PDF de la orden de pedido"

        )

        if not confirmar:

            return

        try:

            pedido_id = self.pedido.procesar_pedido(

                usuario_id,

                sucursal_id

            )

        except Exception as e:

            messagebox.showerror(

                "Error al guardar el pedido",

                str(e)

            )

            return

        if not pedido_id:

            messagebox.showerror(

                "Stockify",

                "No se pudo guardar el pedido"

            )

            return

        # ======================================
        # GENERAR PDF (no revierte el guardado si falla)
        # ======================================

        try:

            # Preguntar dónde guardar el PDF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"pedido_{pedido_id}_{timestamp}.pdf"
            save_path = filedialog.asksaveasfilename(
                parent=self,
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=default_name,
                title="Guardar pedido como"
            )

            if save_path:
                filepath = generar_pedido_guardar(
                    save_path,
                    items,
                    cliente="",
                    vendedor=nombre_usuario,
                    numero=str(pedido_id)
                )
            else:
                # Si el usuario cancela, guardamos en proyecto con nombre por defecto
                filepath = generar_pedido_guardar(
                    default_name,
                    items,
                    cliente="",
                    vendedor=nombre_usuario,
                    numero=str(pedido_id)
                )

            pdf_ok = True

            # Intentar abrir el PDF generado (Windows)
            try:
                abs_path = os.path.abspath(filepath)
                if os.name == 'nt':
                    os.startfile(abs_path)
            except Exception:
                # No crítico si no se puede abrir automáticamente
                pass

        except Exception as e:

            pdf_ok = False

            messagebox.showerror(

                "Pedido guardado, pero falló el PDF",

                f"El pedido #{pedido_id} se guardó y el stock fue actualizado, "
                f"pero no se pudo generar el PDF:\n{e}"

            )

        self.pedido.vaciar()

        self.actualizar_pedido()

        self.var_cantidad.set(1)

        self.var_tipo.set("UNIDAD")

        self.lbl_ultimo_agregado.config(text="")

        self.entry_busqueda.focus_set()

        if pdf_ok:

            messagebox.showinfo(

                "Stockify",

                f"Pedido #{pedido_id} finalizado correctamente.\n\n"
                f"Stock actualizado, movimiento registrado en el historial "
                f"y PDF generado."

            )