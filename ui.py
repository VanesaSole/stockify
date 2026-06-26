# ui.py

import os

import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from tema import *

from logic import (
    buscar_productos,
    agregar_producto,
    cambiar_modo,
    preparar_datos_exportacion,
    validar_tabla_vacia
)

from data import (
    cargar_catalogo,
    exportar_excel,
    es_excel,
    es_pdf
)

from boleta import generar_boleta_pdf


class App:

    def __init__(self, root, usuario):

        self.root = root

        self.usuario = usuario

        self.root.title("Stockify")

        self.root.geometry("1200x700")

        self.root.configure(bg=COLOR_FONDO)

        # =================================================
        # DATOS USUARIO
        # =================================================

        self.nombre_usuario = usuario[1]

        self.email_usuario = usuario[2]

        self.direccion_usuario = usuario[3]

        # =================================================
        # ESTADO
        # =================================================

        self.productos = []

        self.productos_lower = []

        self.catalogo_dict = {}

        self.modo = "PEDIDO"

        # =================================================
        # UI
        # =================================================

        self.crear_widgets()

        # =================================================
        # CARGAR CATALOGO AUTOMATICO
        # =================================================

        self.cargar_catalogo_automatico()

    # =====================================================
    # CATALOGO AUTOMATICO
    # =====================================================

    def cargar_catalogo_automatico(self):

        posibles_archivos = [

            "catalogo.xlsx",

            "catalogo.xls",

            "productos.xlsx",

            "productos.xls"

        ]

        archivo_encontrado = None

        for archivo in posibles_archivos:

            if os.path.exists(archivo):

                archivo_encontrado = archivo

                break

        if not archivo_encontrado:
            return

        try:

            data = cargar_catalogo(
                archivo_encontrado
            )

            self.productos = data["productos"]

            self.productos_lower = data["productos_lower"]

            self.catalogo_dict = data["catalogo_dict"]

            messagebox.showinfo(
                "Stockify",
                f"Catálogo automático cargado:\n{archivo_encontrado}"
            )

            # =================================================
            # DEVOLVER FOCO AL BUSCADOR
            # =================================================

            self.buscador.focus_set()

            self.root.update()

        except Exception as e:

            messagebox.showerror(
                "Error catálogo automático",
                str(e)
            )

    # =====================================================
    # CREAR WIDGETS
    # =====================================================

    def crear_widgets(self):

        # =================================================
        # TOP FRAME
        # =================================================

        top_frame = tk.Frame(
            self.root,
            bg=COLOR_FONDO
        )

        top_frame.pack(pady=10)

        tk.Button(
            top_frame,
            text="Cargar Catálogo",
            command=self.cargar_catalogo_ui,
            bg=COLOR_AZUL,
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            top_frame,
            text="Cambiar Pedido / Envío",
            command=self.cambiar_modo_ui,
            bg=COLOR_VERDE,
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            height=2
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            top_frame,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            bg=COLOR_ROJO,
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            height=2
        ).grid(row=0, column=2, padx=5)

        # =================================================
        # LABEL MODO
        # =================================================

        self.label_modo = tk.Label(
            self.root,
            text="Modo: PEDIDO",
            fg=COLOR_AZUL,
            bg=COLOR_FONDO,
            font=("Arial", 12, "bold")
        )

        self.label_modo.pack(pady=5)

        # =================================================
        # USUARIO
        # =================================================

        self.label_usuario = tk.Label(
            self.root,
            text=f"Sesión iniciada: {self.nombre_usuario}",
            bg=COLOR_FONDO,
            fg=COLOR_GRIS,
            font=("Arial", 10)
        )

        self.label_usuario.pack()

        # =================================================
        # BUSCADOR
        # =================================================

        self.buscador = tk.Entry(
            self.root,
            width=80,
            font=("Arial", 12)
        )

        self.buscador.pack(pady=12)

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

        # =================================================
        # LISTA
        # =================================================

        self.lista = tk.Listbox(
            self.root,
            width=110,
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

        # =================================================
        # CANTIDAD
        # =================================================

        frame = tk.Frame(
            self.root,
            bg=COLOR_FONDO
        )

        frame.pack(pady=10)

        tk.Label(
            frame,
            text="Cantidad",
            bg=COLOR_FONDO
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
            command=self.agregar_producto_ui,
            bg=COLOR_AZUL,
            fg="white",
            width=15
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(
            frame,
            text="Eliminar",
            command=self.eliminar_producto_ui,
            bg=COLOR_ROJO,
            fg="white",
            width=15
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # =================================================
        # TIPO CARGA
        # =================================================

        self.tipo_carga = tk.StringVar()

        self.tipo_carga.set("UNIDAD")

        frame_tipo = tk.Frame(
            self.root,
            bg=COLOR_FONDO
        )

        frame_tipo.pack(pady=5)

        tk.Label(
            frame_tipo,
            text="Tipo:",
            bg=COLOR_FONDO,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5)

        tk.Radiobutton(
            frame_tipo,
            text="Unidad",
            variable=self.tipo_carga,
            value="UNIDAD",
            bg=COLOR_FONDO
        ).grid(row=0, column=1)

        tk.Radiobutton(
            frame_tipo,
            text="Bulto",
            variable=self.tipo_carga,
            value="BULTO",
            bg=COLOR_FONDO
        ).grid(row=0, column=2)

        # =================================================
        # TABLA
        # =================================================

        self.columnas_pedido = (

            "Producto",

            "Tipo",

            "Cantidad",

            "Unidades"

        )

        self.columnas_envio = (

            "Producto",

            "Tipo",

            "Cantidad",

            "Unidades",

            "Costo",

            "Venta",

            "Mayoreo",

            "Total"

        )

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

        # =================================================
        # FINALIZAR
        # =================================================

        tk.Button(
            self.root,
            text="Finalizar Pedido",
            command=self.finalizar_pedido_ui,
            bg=COLOR_AZUL,
            fg="white",
            font=("Arial", 11, "bold"),
            width=25,
            height=2
        ).pack(pady=12)

    # =====================================================
    # ACTUALIZAR COLUMNAS
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

            if col == "Producto":

                ancho = 420

            elif col == "Tipo":

                ancho = 90

            elif col == "Cantidad":

                ancho = 90

            elif col == "Unidades":

                ancho = 90

            else:

                ancho = 110

            self.tabla.column(
                col,
                width=ancho,
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

            self.buscador.focus_set()

            self.root.update()

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

        tipo = self.tipo_carga.get()

        resultado = agregar_producto(

            producto,

            cantidad,

            self.catalogo_dict,

            self.modo,

            tipo

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

    def eliminar_producto_ui(self):

        seleccion = self.tabla.selection()

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

        self.label_modo.config(
            text=f"Modo: {self.modo}"
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
    # FINALIZAR PEDIDO
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

            if es_excel(ruta):

                exportar_excel(
                    ruta,
                    columnas,
                    datos
                )

            elif es_pdf(ruta):

                generar_boleta_pdf(
                    ruta_pdf=ruta,
                    datos_tabla=datos,
                    modo=self.modo,
                    logo_path="logo.png",
                    numero_pedido="0001",
                    cliente=self.nombre_usuario,
                    direccion=self.direccion_usuario,
                    vendedor="Stockify"
                )

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

    # =====================================================
    # CERRAR SESION
    # =====================================================

    def cerrar_sesion(self):

        self.root.destroy()

        import tkinter as tk

        from auth import AuthWindow

        nuevo_root = tk.Tk()

        AuthWindow(
            nuevo_root,
            self.reabrir_sistema
        )

        nuevo_root.mainloop()

    # =====================================================
    # REABRIR SISTEMA
    # =====================================================

    def reabrir_sistema(self, usuario):

        import tkinter as tk

        nuevo_root = tk.Tk()

        App(
            nuevo_root,
            usuario
        )

        nuevo_root.mainloop()