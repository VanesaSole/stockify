# ui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# lógica
from logic import (
    buscar_productos,
    agregar_producto,
    cambiar_modo,
    preparar_datos_exportacion,
    validar_tabla_vacia
)

# data
from data import (
    cargar_catalogo,
    exportar_excel,
    es_excel,
    es_pdf
)

# pdf
from boleta import generar_boleta_pdf


class App:

    def __init__(self, root, usuario):

        self.root = root

        self.usuario = usuario

        self.root.title("Stockify")

        self.root.geometry("1100x700")

        # estado
        self.productos = []

        self.productos_lower = []

        self.catalogo_dict = {}

        self.modo = "PEDIDO"

        self.crear_widgets()

    # =====================================================
    # UI
    # =====================================================

    def crear_widgets(self):

        # -------------------------------------------------
        # TOP FRAME
        # -------------------------------------------------

        top_frame = tk.Frame(self.root)

        top_frame.pack(pady=10)

        # -------------------------------------------------
        # BOTON CARGAR
        # -------------------------------------------------

        tk.Button(
            top_frame,
            text="Cargar Catálogo",
            command=self.cargar_catalogo_ui,
            bg="#1976D2",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            height=2
        ).grid(row=0, column=0, padx=5)

        # -------------------------------------------------
        # BOTON CAMBIAR MODO
        # -------------------------------------------------

        tk.Button(
            top_frame,
            text="Cambiar Pedido / Envío",
            command=self.cambiar_modo_ui,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold"),
            width=20,
            height=2
        ).grid(row=0, column=1, padx=5)

        # -------------------------------------------------
        # LABEL MODO
        # -------------------------------------------------

        self.label_modo = tk.Label(
            self.root,
            text="Modo: PEDIDO",
            fg="blue",
            font=("Arial", 14, "bold")
        )

        self.label_modo.pack(pady=5)

        # -------------------------------------------------
        # BUSCADOR
        # -------------------------------------------------

        self.buscador = tk.Entry(
            self.root,
            width=70,
            font=("Arial", 12)
        )

        self.buscador.pack(pady=10)

        self.buscador.bind(
            "<KeyRelease>",
            self.on_key_release
        )

        self.buscador.bind(
            "<Return>",
            self.on_enter_buscador
        )

        self.buscador.bind(
            "<Down>",
            self.bajar_lista
        )

        # -------------------------------------------------
        # LISTA
        # -------------------------------------------------

        self.lista = tk.Listbox(
            self.root,
            width=100,
            height=8,
            font=("Arial", 10)
        )

        self.lista.pack()

        self.lista.bind(
            "<Double-Button-1>",
            self.confirmar_producto
        )

        self.lista.bind(
            "<Return>",
            self.confirmar_producto
        )

        self.lista.bind(
            "<Up>",
            self.subir_lista
        )

        self.lista.bind(
            "<Down>",
            self.bajar_lista
        )

        # -------------------------------------------------
        # FRAME CANTIDAD
        # -------------------------------------------------

        frame = tk.Frame(self.root)

        frame.pack(pady=10)

        tk.Label(
            frame,
            text="Cantidad"
        ).grid(row=0, column=0)

        self.entrada_cantidad = tk.Entry(
            frame,
            width=10,
            font=("Arial", 11)
        )

        self.entrada_cantidad.grid(
            row=0,
            column=1
        )

        self.entrada_cantidad.bind(
            "<Return>",
            self.agregar_producto_ui
        )

        tk.Button(
            frame,
            text="Agregar",
            command=self.agregar_producto_ui
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(
            frame,
            text="Eliminar",
            command=self.eliminar_producto_ui
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # -------------------------------------------------
        # COLUMNAS
        # -------------------------------------------------

        self.columnas_pedido = (
            "Producto",
            "Cantidad"
        )

        self.columnas_envio = (
            "Producto",
            "Cantidad",
            "Costo",
            "Venta",
            "Mayoreo",
            "Total"
        )

        # -------------------------------------------------
        # TABLA
        # -------------------------------------------------

        self.tabla = ttk.Treeview(
            self.root,
            columns=self.columnas_pedido,
            show="headings"
        )

        self.actualizar_columnas_tabla()

        self.tabla.pack(
            expand=True,
            fill="both",
            pady=10
        )

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        self.root.bind(
            "<Delete>",
            self.eliminar_producto_ui
        )

        # -------------------------------------------------
        # EXPORTAR
        # -------------------------------------------------

        tk.Button(
            self.root,
            text="Finalizar Pedido",
            command=self.finalizar_pedido_ui,
            bg="#1565C0",
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=2
        ).pack(pady=10)

    # =====================================================
    # TABLA
    # =====================================================

    def actualizar_columnas_tabla(self):

        if self.modo == "PEDIDO":
            columnas = self.columnas_pedido
        else:
            columnas = self.columnas_envio

        self.tabla["columns"] = columnas

        for col in columnas:

            self.tabla.heading(
                col,
                text=col
            )

            self.tabla.column(
                col,
                width=180,
                anchor="center"
            )

    # =====================================================
    # CARGAR CATALOGO
    # =====================================================

    def cargar_catalogo_ui(self):

        ruta = filedialog.askopenfilename(
            title="Seleccionar catálogo",
            filetypes=[("Excel", "*.xlsx *.xls")]
        )

        if not ruta:
            return

        try:

            data = cargar_catalogo(ruta)

            self.productos = data["productos"]

            self.productos_lower = data["productos_lower"]

            self.catalogo_dict = data["catalogo_dict"]

            messagebox.showinfo(
                "OK",
                f"{len(self.productos)} productos cargados"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================================
    # BUSCADOR
    # =====================================================

    def on_key_release(self, event=None):

        teclas_ignoradas = [
            "Up",
            "Down",
            "Return"
        ]

        if event and event.keysym in teclas_ignoradas:
            return

        texto = self.buscador.get()

        resultados = buscar_productos(
            texto,
            self.productos
        )

        self.lista.delete(0, tk.END)

        for r in resultados:

            self.lista.insert(
                tk.END,
                r
            )

    # =====================================================
    # ENTER BUSCADOR
    # =====================================================

    def on_enter_buscador(self, event=None):

        if self.lista.size() == 0:
            return "break"

        seleccion = self.lista.curselection()

        if not seleccion:

            self.lista.selection_clear(0, tk.END)

            self.lista.selection_set(0)

            self.lista.activate(0)

            self.lista.focus_set()

            return "break"

        self.entrada_cantidad.focus_set()

        return "break"

    # =====================================================
    # BAJAR LISTA
    # =====================================================

    def bajar_lista(self, event=None):

        if self.lista.size() == 0:
            return "break"

        seleccion = self.lista.curselection()

        if not seleccion:

            self.lista.selection_set(0)

            self.lista.activate(0)

            return "break"

        indice = seleccion[0]

        if indice < self.lista.size() - 1:

            self.lista.selection_clear(indice)

            self.lista.selection_set(indice + 1)

            self.lista.activate(indice + 1)

            self.lista.see(indice + 1)

        return "break"

    # =====================================================
    # SUBIR LISTA
    # =====================================================

    def subir_lista(self, event=None):

        if self.lista.size() == 0:
            return "break"

        seleccion = self.lista.curselection()

        if not seleccion:
            return "break"

        indice = seleccion[0]

        if indice > 0:

            self.lista.selection_clear(indice)

            self.lista.selection_set(indice - 1)

            self.lista.activate(indice - 1)

            self.lista.see(indice - 1)

        return "break"

    # =====================================================
    # CONFIRMAR PRODUCTO
    # =====================================================

    def confirmar_producto(self, event=None):

        if not self.lista.curselection():
            return "break"

        self.entrada_cantidad.focus_set()

        return "break"

    # =====================================================
    # AGREGAR PRODUCTO
    # =====================================================

    def agregar_producto_ui(self, event=None):

        try:

            producto = self.lista.get(
                self.lista.curselection()
            )

        except:
            return

        cantidad = self.entrada_cantidad.get()

        resultado = agregar_producto(
            producto,
            cantidad,
            self.catalogo_dict,
            self.modo
        )

        if "error" in resultado:

            messagebox.showwarning(
                "Error",
                resultado["error"]
            )

            return

        fila = resultado["fila"]

        self.tabla.insert(
            "",
            tk.END,
            values=fila
        )

        self.entrada_cantidad.delete(0, tk.END)

        self.buscador.delete(0, tk.END)

        self.lista.delete(0, tk.END)

        self.buscador.focus_set()

    # =====================================================
    # ELIMINAR
    # =====================================================

    def eliminar_producto_ui(self, event=None):

        seleccion = self.tabla.selection()

        if seleccion:

            for item in seleccion:

                self.tabla.delete(item)

    # =====================================================
    # CAMBIAR MODO
    # =====================================================

    def cambiar_modo_ui(self):

        self.modo = cambiar_modo(self.modo)

        for item in self.tabla.get_children():

            self.tabla.delete(item)

        self.actualizar_columnas_tabla()

        if self.modo == "PEDIDO":

            self.label_modo.config(
                text="Modo: PEDIDO",
                fg="blue"
            )

        else:

            self.label_modo.config(
                text="Modo: ENVÍO",
                fg="green"
            )

    # =====================================================
    # OBTENER DATOS TABLA
    # =====================================================

    def obtener_datos_tabla(self):

        datos = []

        for item in self.tabla.get_children():

            valores = self.tabla.item(item)["values"]

            datos.append(valores)

        return datos

    # =====================================================
    # EXPORTAR
    # =====================================================

    def finalizar_pedido_ui(self):

        datos_tabla = self.obtener_datos_tabla()

        if validar_tabla_vacia(datos_tabla):

            messagebox.showwarning(
                "Aviso",
                "No hay productos"
            )

            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Excel", "*.xlsx")
            ]
        )

        if not ruta:
            return

        try:

            columnas, datos = preparar_datos_exportacion(
                datos_tabla,
                self.modo
            )

            # =================================================
            # EXCEL
            # =================================================

            if es_excel(ruta):

                exportar_excel(
                    ruta,
                    columnas,
                    datos
                )

            # =================================================
            # PDF
            # =================================================

            elif es_pdf(ruta):

                cliente = ""
                direccion = ""
                vendedor = "Stockify"

                # usuario puede venir como dict o tuple
                if isinstance(self.usuario, dict):

                    cliente = self.usuario.get("nombre", "")
                    direccion = self.usuario.get("direccion", "")

                elif isinstance(self.usuario, tuple):

                    # AJUSTADO PARA SQLITE
                    # id, nombre, email, contraseña, direccion

                    if len(self.usuario) >= 5:

                        cliente = self.usuario[1]
                        direccion = self.usuario[4]

                generar_boleta_pdf(
                    ruta_pdf=ruta,
                    datos_tabla=datos,
                    modo=self.modo,
                    logo_path="logo.png",
                    numero_pedido="0001",
                    cliente=cliente,
                    direccion=direccion,
                    vendedor=vendedor
                )

            # =================================================
            # LIMPIAR
            # =================================================

            for item in self.tabla.get_children():

                self.tabla.delete(item)

            self.buscador.delete(0, tk.END)

            self.entrada_cantidad.delete(0, tk.END)

            self.lista.delete(0, tk.END)

            self.buscador.focus_set()

            self.root.update()

            messagebox.showinfo(
                "OK",
                "Archivo generado correctamente"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )