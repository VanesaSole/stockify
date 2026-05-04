# ui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# importar capas
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
    exportar_pdf,
    es_excel,
    es_pdf
)



class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Logístico")
        self.root.geometry("950x650")

        # estado
        self.productos = []
        self.productos_lower = []
        self.catalogo_dict = {}
        self.modo = "PEDIDO"

        self.crear_widgets()


    # ---------------- UI ----------------

    def crear_widgets(self):

        tk.Button(self.root, text="Cargar Catálogo", command=self.cargar_catalogo_ui).pack(pady=5)

        self.label_modo = tk.Label(self.root, text="Modo: PEDIDO", fg="blue", font=("Arial", 12))
        self.label_modo.pack()

        tk.Button(self.root, text="Cambiar a Pedido / Envío", command=self.cambiar_modo_ui).pack(pady=5)

        self.buscador = tk.Entry(self.root, width=60)
        self.buscador.pack(pady=10)

        self.buscador.bind("<KeyRelease>", self.on_key_release)
        self.buscador.bind("<Return>", self.on_enter_buscador)

        self.lista = tk.Listbox(self.root, width=90, height=8)
        self.lista.pack()
        self.lista.bind("<Double-Button-1>", self.agregar_producto_ui)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Cantidad").grid(row=0, column=0)

        self.entrada_cantidad = tk.Entry(frame, width=10)
        self.entrada_cantidad.grid(row=0, column=1)
        self.entrada_cantidad.bind("<Return>", self.agregar_producto_ui)

        tk.Button(frame, text="Agregar", command=self.agregar_producto_ui).grid(row=0, column=2, padx=5)
        tk.Button(frame, text="Eliminar", command=self.eliminar_producto_ui).grid(row=0, column=3, padx=5)

        # tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=("Descripción", "Cantidad", "Costo", "Venta", "Mayoreo"),
            show="headings"
        )

        for col in ("Descripción", "Cantidad", "Costo", "Venta", "Mayoreo"):
            self.tabla.heading(col, text=col)

        self.tabla.pack(expand=True, fill="both", pady=10)

        tk.Button(self.root, text="Finalizar Pedido", command=self.finalizar_pedido_ui, height=2).pack(pady=10)


    # ---------------- EVENTOS ----------------

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

            messagebox.showinfo("OK", f"{len(self.productos)} productos cargados")

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def on_key_release(self, event=None):
        texto = self.buscador.get()

        resultados = buscar_productos(texto, self.productos)

        self.lista.delete(0, tk.END)

        for r in resultados:
            self.lista.insert(tk.END, r)


    def on_enter_buscador(self, event=None):
        if self.lista.size() > 0:
            self.lista.selection_set(0)
            self.entrada_cantidad.focus()


    def agregar_producto_ui(self, event=None):

        try:
            producto = self.lista.get(self.lista.curselection())
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
            messagebox.showwarning("Error", resultado["error"])
            return

        self.tabla.insert("", tk.END, values=resultado["fila"])

        # limpiar
        self.entrada_cantidad.delete(0, tk.END)
        self.buscador.delete(0, tk.END)
        self.lista.delete(0, tk.END)

        self.buscador.focus()


    def eliminar_producto_ui(self):
        seleccion = self.tabla.selection()
        if seleccion:
            self.tabla.delete(seleccion)


    def cambiar_modo_ui(self):
        self.modo = cambiar_modo(self.modo)

        if self.modo == "PEDIDO":
            self.label_modo.config(text="Modo: PEDIDO", fg="blue")
        else:
            self.label_modo.config(text="Modo: ENVÍO", fg="green")



    def obtener_datos_tabla(self):
        """
        Extrae datos desde Treeview (movido de data.py).
        """
        datos = []
        for item in self.tabla.get_children():
            valores = self.tabla.item(item)["values"]
            datos.append(valores)
        return datos


    def finalizar_pedido_ui(self):

        datos_tabla = self.obtener_datos_tabla()


        if validar_tabla_vacia(datos_tabla):
            messagebox.showwarning("Aviso", "No hay productos")
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("PDF", "*.pdf")]
        )

        if not ruta:
            return

        try:
            columnas, datos = preparar_datos_exportacion(datos_tabla, self.modo)

            if es_excel(ruta):
                exportar_excel(ruta, columnas, datos)

            elif es_pdf(ruta):
                exportar_pdf(ruta, datos)


            messagebox.showinfo("OK", "Archivo generado")

        except Exception as e:
            messagebox.showerror("Error", str(e))



