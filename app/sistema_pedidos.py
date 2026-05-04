import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

productos = []
productos_lower = []
catalogo = None
modo = "PEDIDO"  # PEDIDO o ENVIO


# ---------------- CARGAR CATALOGO ----------------

def cargar_catalogo():
    global productos, productos_lower, catalogo

    archivo = filedialog.askopenfilename(
        title="Seleccionar catálogo",
        filetypes=[("Excel","*.xlsx *.xls")]
    )

    if archivo == "":
        return

    catalogo = pd.read_excel(archivo)

    productos = catalogo.iloc[:,1].dropna().tolist()
    productos_lower = [p.lower() for p in productos]

    messagebox.showinfo("OK", f"{len(productos)} productos cargados")


# ---------------- BUSCADOR ----------------

def autocompletar(event=None):

    texto = buscador.get().lower()

    lista.delete(0, tk.END)

    if texto == "":
        return

    resultados = []

    for i, p in enumerate(productos_lower):
        if texto in p:
            resultados.append(productos[i])

        if len(resultados) >= 30:
            break

    for r in resultados:
        lista.insert(tk.END, r)


# ---------------- ENTER EN BUSCADOR ----------------

def enter_buscador(event=None):

    if lista.size() > 0:
        lista.selection_set(0)
        entrada_cantidad.focus()


# ---------------- AGREGAR PRODUCTO ----------------

def agregar_producto(event=None):

    try:
        producto = lista.get(lista.curselection())
    except:
        return

    cantidad = entrada_cantidad.get().replace(",", ".")

    try:
        cantidad = float(cantidad)
    except:
        messagebox.showwarning("Error","Cantidad inválida")
        return

    fila = catalogo[catalogo.iloc[:,1] == producto].iloc[0]

    try:
        costo = fila["precio_costo"]
        venta = fila["precio_venta"]
        mayoreo = fila["precio_mayoreo"]
    except:
        costo = ""
        venta = ""
        mayoreo = ""

    tabla.insert("",tk.END,values=(producto,cantidad,costo,venta,mayoreo))

    # limpiar
    entrada_cantidad.delete(0,tk.END)
    buscador.delete(0,tk.END)
    lista.delete(0,tk.END)

    buscador.focus()


# ---------------- ELIMINAR ----------------

def eliminar_producto():
    sel = tabla.selection()
    if sel:
        tabla.delete(sel)


# ---------------- CAMBIAR MODO ----------------

def cambiar_modo():
    global modo

    if modo == "PEDIDO":
        modo = "ENVIO"
        label_modo.config(text="Modo: ENVÍO", fg="green")
    else:
        modo = "PEDIDO"
        label_modo.config(text="Modo: PEDIDO", fg="blue")


# ---------------- EXPORTAR PDF ----------------

def exportar_pdf(datos, archivo):

    c = canvas.Canvas(archivo, pagesize=letter)
    y = 750

    for fila in datos:

        if modo == "PEDIDO":
            texto = f"{fila[0]} - Cantidad: {fila[1]}"
        else:
            texto = f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]}"

        c.drawString(50,y,texto)
        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()


# ---------------- FINALIZAR ----------------

def finalizar_pedido():

    if len(tabla.get_children()) == 0:
        messagebox.showwarning("Aviso","No hay productos")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel","*.xlsx"),("PDF","*.pdf")]
    )

    if archivo == "":
        return

    datos = []

    for item in tabla.get_children():
        datos.append(tabla.item(item)["values"])

    try:

        if archivo.endswith(".xlsx"):

            if modo == "PEDIDO":
                df = pd.DataFrame(datos,columns=["Descripción","Cantidad"])
                df = df[["Descripción","Cantidad"]]

            else:
                df = pd.DataFrame(datos,columns=[
                    "Descripción","Cantidad","Costo","Venta","Mayoreo"
                ])

            df.to_excel(archivo,index=False)

        else:
            exportar_pdf(datos,archivo)

        messagebox.showinfo("OK","Archivo generado")

    except Exception as e:
        messagebox.showerror("Error",str(e))


# ---------------- INTERFAZ ----------------

root = tk.Tk()
root.title("Stockify - Sistema Logístico")
root.geometry("950x650")

tk.Button(root,text="Cargar Catálogo",command=cargar_catalogo).pack(pady=5)

label_modo = tk.Label(root,text="Modo: PEDIDO",fg="blue",font=("Arial",12))
label_modo.pack()

tk.Button(root,text="Cambiar a Pedido / Envío",command=cambiar_modo).pack(pady=5)

buscador = tk.Entry(root,width=60)
buscador.pack(pady=10)

buscador.bind("<KeyRelease>",autocompletar)
buscador.bind("<Return>",enter_buscador)

lista = tk.Listbox(root,width=90,height=8)
lista.pack()

lista.bind("<Double-Button-1>",agregar_producto)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame,text="Cantidad").grid(row=0,column=0)

entrada_cantidad = tk.Entry(frame,width=10)
entrada_cantidad.grid(row=0,column=1)

entrada_cantidad.bind("<Return>",agregar_producto)

tk.Button(frame,text="Agregar",command=agregar_producto).grid(row=0,column=2,padx=5)
tk.Button(frame,text="Eliminar",command=eliminar_producto).grid(row=0,column=3,padx=5)

tabla = ttk.Treeview(
    root,
    columns=("Descripción","Cantidad","Costo","Venta","Mayoreo"),
    show="headings"
)

for col in ("Descripción","Cantidad","Costo","Venta","Mayoreo"):
    tabla.heading(col,text=col)

tabla.pack(expand=True, fill="both", pady=10)

tk.Button(root,text="Finalizar Pedido",command=finalizar_pedido,height=2).pack(pady=10)

root.mainloop()