# ==========================
# STOCKIFY V2 - boleta.py
# ==========================

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4

from reportlab.graphics.barcode import qr

from datetime import datetime
import os


# ==========================
# ESTILOS
# ==========================

styles = getSampleStyleSheet()

estilo_normal = styles["Normal"]

estilo_titulo = ParagraphStyle(
    "titulo",
    parent=styles["Heading1"],
    alignment=TA_CENTER,
    textColor=colors.white,
    fontSize=16
)

estilo_descripcion = ParagraphStyle(
    "descripcion",
    parent=styles["Normal"],
    fontSize=9,
    leading=12
)


# ==========================
# FORMATO DINERO
# ==========================

def dinero(numero):
    try:
        return f"${float(numero):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "$0,00"


# ==========================
# LOGO
# ==========================

def crear_logo():

    rutas = [

        "assets/logo.png",

        "logo.png",

        "imagenes/logo.png"

    ]

    for ruta in rutas:

        if os.path.exists(ruta):

            logo = Image(ruta)

            logo.drawWidth = 3 * cm

            logo.drawHeight = 3 * cm

            return logo

    return Spacer(1, 1*cm)



from reportlab.graphics.shapes import Drawing

# ==========================
# QR
# ==========================

def crear_qr():

    codigo = qr.QrCodeWidget(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    bounds = codigo.getBounds()

    ancho = bounds[2] - bounds[0]
    alto = bounds[3] - bounds[1]

    dibujo = Drawing(
        3*cm,
        3*cm,
        transform=[
            3*cm/ancho,
            0,
            0,
            3*cm/alto,
            0,
            0
        ]
    )

    dibujo.add(codigo)

    return dibujo


# ==========================
# ENCABEZADO
# ==========================

def crear_encabezado(
        elementos,
        titulo,
        color
):

    logo = crear_logo()

    titulo_parrafo = Paragraph(

        f"<font color='white'><b>{titulo}</b></font>",

        ParagraphStyle(

            "encabezado",

            parent=estilo_titulo,

            backColor=color,

            alignment=TA_CENTER

        )

    )

    tabla = Table(

        [

            [

                logo,

                titulo_parrafo

            ]

        ],

        colWidths=[4*cm, 13*cm]

    )

    tabla.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),color),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

        ("BOX",(0,0),(-1,-1),1,colors.black)

    ]))

    elementos.append(tabla)

    elementos.append(
        Spacer(
            1,
            0.4*cm
        )
    )


def crear_separador(elementos):

    elementos.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=colors.grey

        )

    )

    elementos.append(

        Spacer(

            1,

            0.3*cm

        )

    )

# ==========================
# DATOS GENERALES
# ==========================

def crear_datos_generales(
        elementos,
        cliente="",
        vendedor="",
        numero=""
):

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    datos = [
        ["Cliente", cliente],
        ["Vendedor", vendedor],
        ["Número", numero],
        ["Fecha", fecha]
    ]

    tabla = Table(datos, colWidths=[3*cm, 10*cm])

    tabla.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),
        ("BOX",(0,0),(-1,-1),1,colors.black),
        ("GRID",(0,0),(-1,-1),0.5,colors.black),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1,0.4*cm))


# ==========================
# TABLA PRODUCTOS
# ==========================

def crear_tabla(elementos, productos,color):

    datos = [["Código", "Descripción", "Cant.", "Precio", "Subtotal"]]

    total = 0

    for p in productos:

        codigo = str(
            p["producto_id"]
        )

        descripcion = Paragraph(
            p["nombre"],
            estilo_descripcion
        )

        cantidad = p["cantidad"]

        precio = p["precio"]

        subtotal = p["subtotal"]

        total += subtotal

        datos.append([

            codigo,

            descripcion,

            f'{cantidad} {p["tipo"]}',

            dinero(precio),

            dinero(subtotal)

        ])

    tabla = Table(
        datos,
        repeatRows=1,
        colWidths=[
            2 * cm,
            8 * cm,
            2 * cm,
            3 * cm,
            3 * cm
        ]
    )

    tabla.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),color),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("BOX", (0, 0), (-1, -1), 1, colors.black),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")

    ]))

    elementos.append(
        tabla
    )

    return total


# ==========================
# TOTALES
# ==========================

def crear_totales(elementos, total):

    elementos.append(Spacer(1, 0.5*cm))

    tabla = Table(
        [
            ["TOTAL", dinero(total)]
        ],
        colWidths=[4*cm, 4*cm]
    )

    tabla.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.lightgrey),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

        ("BOX",(0,0),(-1,-1),1,colors.black),

        ("ALIGN",(0,0),(-1,-1),"CENTER")

    ]))

    elementos.append(tabla)
    
# ==========================
# RESUMEN
# ==========================

def crear_resumen(
        elementos,
        productos,
        total
):

    cantidad_productos = len(
        productos
    )
    
    cantidad_unidades = sum(
    p.get("unidades", 0)
    for p in productos
    )
    
    datos = [

        [

            "Productos",

            cantidad_productos

        ],

        [

            "Unidades",

            cantidad_unidades

        ],

        [

            "Total",

            dinero(total)

        ]

    ]

    tabla = Table(

        datos,

        colWidths=[5*cm,5*cm]

    )

    tabla.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

        ("BOX",(0,0),(-1,-1),1,colors.black),

        ("GRID",(0,0),(-1,-1),0.5,colors.black),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold")

    ]))

    elementos.append(
        Spacer(
            1,
            0.4*cm
        )
    )

    elementos.append(
        tabla
    )


    
def crear_footer(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    fecha = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    canvas.drawString(
        2*cm,
        1*cm,
        f"Stockify V2 | {fecha}"
    )

    canvas.drawRightString(
        19*cm,
        1*cm,
        f"Página {doc.page}"
    )

    canvas.restoreState()
    
def generar_documento(

        nombre_archivo,
        titulo,
        color,
        productos,
        cliente="",
        vendedor="",
        numero=""

):

    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=A4
    )

    elementos = []

    crear_encabezado(
        elementos,
        titulo,
        color
    )

    crear_datos_generales(
        elementos,
        cliente,
        vendedor,
        numero
    )

    total = crear_tabla(
        elementos,
        productos,
        color
    )

    crear_totales(
        elementos,
        total
    )

    crear_observaciones(
        elementos
    )

    elementos.append(
        Spacer(
            1,
            0.5*cm
        )
    )

    elementos.append(
        crear_qr()
        )


    doc.build(
        elementos,
        onFirstPage=crear_footer,
        onLaterPages=crear_footer
    )

    return nombre_archivo

def generar_pedido_azul(

        productos,
        cliente="",
        vendedor="",
        numero="",
        nombre_archivo="pedido.pdf"

):

    return generar_documento(

        nombre_archivo,

        "PEDIDO",

        colors.HexColor("#2E86C1"),

        productos,

        cliente,

        vendedor,

        numero

    )
    
# =====================================
# REMITO VERDE
# =====================================

def generar_remito_verde(

        productos,
        cliente="",
        vendedor="",
        numero=""

):

    return generar_documento(

        "remito.pdf",

        "REMITO",

        colors.HexColor("#27AE60"),

        productos,

        cliente,

        vendedor,

        numero

    )


# =====================================
# REPORTE CELESTE
# =====================================

def generar_reporte_celeste(

        productos,
        cliente="",
        vendedor="",
        numero=""

):

    return generar_documento(

        "reporte.pdf",

        "REPORTE",

        colors.HexColor("#5DADE2"),

        productos,

        cliente,

        vendedor,

        numero

    )


def crear_observaciones(

        elementos,

        texto="Gracias por confiar en Stockify"

):

    elementos.append(

        Spacer(

            1,

            0.5*cm

        )

    )

    elementos.append(

        Paragraph(

            "<b>Observaciones:</b><br/>"+texto,

            estilo_normal

        )

    )

