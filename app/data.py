import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# ---------------- CARGA DE CATÁLOGO ----------------

def cargar_catalogo(ruta_archivo):
    """
    Carga el catálogo desde un archivo Excel.

    Retorna:
    - productos (lista)
    - productos_lower (lista)
    - catalogo_dict (dict optimizado)
    """

    if not ruta_archivo:
        raise ValueError("Ruta de archivo inválida")

    try:
        df = pd.read_excel(ruta_archivo)
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {str(e)}")

    if df.empty:
        raise ValueError("El archivo está vacío")

    # Tomamos la segunda columna como nombre de producto (como en tu sistema original)
    columna_producto = df.columns[1]

    # Remover duplicados para índice único (igual sistema_pedidos.py)
    df_unique = df.drop_duplicates(subset=[columna_producto], keep='first')
    
    productos = df_unique[columna_producto].dropna().astype(str).tolist()
    productos_lower = [p.lower() for p in productos]

    # Diccionario optimizado para búsquedas rápidas
    catalogo_dict = df_unique.set_index(columna_producto).to_dict("index")

    return {
        "productos": productos,
        "productos_lower": productos_lower,
        "catalogo_dict": catalogo_dict,
        "dataframe": df  # opcional, útil si lo necesitás después
    }


# ---------------- EXPORTAR A EXCEL ----------------

def exportar_excel(ruta_archivo, columnas, datos):
    """
    Exporta datos a Excel.
    """

    if not ruta_archivo:
        raise ValueError("Ruta de archivo inválida")

    try:
        df = pd.DataFrame(datos, columns=columnas)
        df.to_excel(ruta_archivo, index=False)
    except Exception as e:
        raise Exception(f"Error al exportar Excel: {str(e)}")


# ---------------- EXPORTAR PDF ----------------

def exportar_pdf(ruta_archivo, datos):
    """
    Exporta datos a PDF (igual que sistema_pedidos.py).
    """
    c = canvas.Canvas(ruta_archivo, pagesize=letter)
    y = 750

    for fila in datos:
        texto = " | ".join(map(str, fila))
        c.drawString(50, y, texto)
        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()


# ---------------- PREPARAR DATOS DESDE UI ----------------




# ---------------- VALIDACIONES DE ARCHIVO ----------------

def es_excel(ruta):
    """
    Verifica si el archivo es Excel.
    """
    return ruta.lower().endswith((".xlsx", ".xls"))


def es_pdf(ruta):
    """
    Verifica si el archivo es PDF.
    """
    return ruta.lower().endswith(".pdf")

