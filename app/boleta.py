# REEMPLAZÁ TODO boleta.py

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

from datetime import datetime


def dinero(valor):

    try:
        valor = float(valor)
    except:
        valor = 0

    texto = f"{valor:,.2f}"

    texto = texto.replace(",", "X")
    texto = texto.replace(".", ",")
    texto = texto.replace("X", ".")

    return f"$ {texto}"


def generar_boleta_pdf(
    ruta_pdf,
    datos_tabla,
    modo="PEDIDO",
    logo_path="logo.png",
    numero_pedido="0001",
    cliente="",
    direccion="",
    vendedor="Stockify"
):

    estilos = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25
    )

    elementos = []

    azul = colors.HexColor("#1E3A8A")
    gris = colors.HexColor("#F3F4F6")

    # =====================================================
    # HEADER
    # =====================================================

    try:

        logo = Image(
            logo_path,
            width=28 * mm,
            height=28 * mm
        )

    except:

        logo = Paragraph(
            "<b>Stockify</b>",
            estilos["Heading2"]
        )

    titulo = Paragraph(
        f"""
        <para align='center'>
        <font size='26' color='#1E3A8A'>
        <b>PEDIDO #{numero_pedido}</b>
        </font>
        </para>
        """,
        estilos["BodyText"]
    )

    fecha = datetime.now().strftime("%d/%m/%Y")

    fecha_paragraph = Paragraph(
        f"""
        <para align='right'>
        <b>Fecha:</b><br/>
        {fecha}
        </para>
        """,
        estilos["BodyText"]
    )

    encabezado = Table(
        [
            [logo, titulo, fecha_paragraph]
        ],
        colWidths=[40 * mm, 100 * mm, 40 * mm]
    )

    encabezado.setStyle(TableStyle([

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("ALIGN", (0, 0), (0, 0), "LEFT"),

        ("ALIGN", (1, 0), (1, 0), "CENTER"),

        ("ALIGN", (2, 0), (2, 0), "RIGHT"),

    ]))

    elementos.append(encabezado)

    elementos.append(Spacer(1, 20))

    # =====================================================
    # CLIENTE
    # =====================================================

    datos_cliente = Table(
        [
            ["Cliente", cliente],
            ["Dirección", direccion],
            ["Vendedor", vendedor]
        ],
        colWidths=[40 * mm, 130 * mm]
    )

    datos_cliente.setStyle(TableStyle([

        ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),

        ("BACKGROUND", (0, 0), (0, -1), gris),

        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

    ]))

    elementos.append(datos_cliente)

    elementos.append(Spacer(1, 18))

    # =====================================================
    # TABLA PRODUCTOS
    # =====================================================

    total_general = 0

    if modo == "PEDIDO":

        tabla_data = [
            ["Producto", "Cantidad"]
        ]

        for fila in datos_tabla:

            producto_paragraph = Paragraph(
                f"""
                <font size='9'>
                {fila[0]}
                </font>
                """,
                estilos["BodyText"]
            )

            tabla_data.append([
                producto_paragraph,
                str(fila[1])
            ])

        widths = [140 * mm, 30 * mm]

    else:

        tabla_data = [
            [
                "Producto",
                "Cantidad",
                "Costo",
                "Venta",
                "Mayoreo",
                "Total"
            ]
        ]

        for fila in datos_tabla:

            producto = fila[0]

            cantidad = float(fila[1])

            costo = float(fila[2])

            venta = float(fila[3])

            mayoreo = float(fila[4])

            total = costo * cantidad

            total_general += total

            producto_paragraph = Paragraph(
                f"""
                <font size='9'>
                {producto}
                </font>
                """,
                estilos["BodyText"]
            )

            tabla_data.append([

                producto_paragraph,

                str(int(cantidad)),

                dinero(costo),

                dinero(venta),

                dinero(mayoreo),

                dinero(total)

            ])

        tabla_data.append([

            "", "", "", "",

            "TOTAL",

            dinero(total_general)

        ])

        widths = [
            85 * mm,
            18 * mm,
            24 * mm,
            24 * mm,
            24 * mm,
            28 * mm
        ]

    tabla = Table(
        tabla_data,
        colWidths=widths
    )

    tabla.setStyle(TableStyle([

        ("BACKGROUND", (0, 0), (-1, 0), azul),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 1, colors.lightgrey),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ("TOPPADDING", (0, 0), (-1, 0), 10),

        ("FONTNAME", (-2, -1), (-1, -1), "Helvetica-Bold"),

    ]))

    elementos.append(tabla)

    elementos.append(Spacer(1, 35))

    # =====================================================
    # FOOTER
    # =====================================================

    footer = Paragraph(
        """
        <para align='center'>
        <font color='#1E3A8A'>
        <b>Gracias por utilizar Stockify</b>
        </font>
        </para>
        """,
        estilos["BodyText"]
    )

    elementos.append(footer)

    # =====================================================
    # GENERAR PDF
    # =====================================================

    doc.build(elementos)