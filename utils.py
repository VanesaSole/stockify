# utils.py

from datetime import datetime


# =====================================================
# FECHA ACTUAL
# =====================================================

def fecha_actual():

    return datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


# =====================================================
# DINERO
# =====================================================

def dinero(valor):

    try:

        return (
            f"${float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    except:

        return "$0,00"


# =====================================================
# LIMPIAR TEXTO
# =====================================================

def limpiar_texto(texto):

    return str(texto).strip()


# =====================================================
# CONVERTIR A ENTERO
# =====================================================

def entero(valor, defecto=0):

    try:

        return int(valor)

    except:

        return defecto


# =====================================================
# CONVERTIR A FLOAT
# =====================================================

def decimal(valor, defecto=0):

    try:

        return float(valor)

    except:

        return defecto


# =====================================================
# VALIDAR VACIO
# =====================================================

def vacio(texto):

    return str(texto).strip() == ""


# =====================================================
# COLOR STOCK
# =====================================================

def color_stock(stock):

    if stock <= 0:

        return "red"

    elif stock <= 10:

        return "orange"

    return "green"
