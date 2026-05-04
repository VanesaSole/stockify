# utils.py


# ---------------- VALIDACIONES ----------------

def es_vacio(valor):
    """
    Verifica si un valor está vacío o es None.
    """
    return valor is None or str(valor).strip() == ""


def limpiar_texto(texto):
    """
    Limpia espacios innecesarios de un texto.
    """
    if texto is None:
        return ""
    return str(texto).strip()


def normalizar_texto(texto):
    """
    Convierte texto a minúsculas y sin espacios extra.
    """
    return limpiar_texto(texto).lower()


# ---------------- NÚMEROS ----------------

def es_numero(valor):
    """
    Verifica si un valor puede convertirse a número.
    """
    try:
        float(str(valor).replace(",", "."))
        return True
    except:
        return False


def convertir_float(valor, default=None):
    """
    Convierte a float de forma segura.
    """
    try:
        return float(str(valor).replace(",", "."))
    except:
        return default


# ---------------- LISTAS ----------------

def limitar_lista(lista, limite=30):
    """
    Limita la cantidad de elementos de una lista.
    """
    return lista[:limite]


def eliminar_duplicados(lista):
    """
    Elimina duplicados manteniendo el orden.
    """
    seen = set()
    resultado = []

    for item in lista:
        if item not in seen:
            seen.add(item)
            resultado.append(item)

    return resultado


# ---------------- STRINGS ----------------

def contiene_texto(texto_base, texto_busqueda):
    """
    Verifica si un texto está contenido en otro (case insensitive).
    """
    return normalizar_texto(texto_busqueda) in normalizar_texto(texto_base)


# ---------------- ARCHIVOS ----------------

def obtener_extension(ruta):
    """
    Devuelve la extensión de un archivo.
    """
    if not ruta or "." not in ruta:
        return ""
    return ruta.split(".")[-1].lower()


def cambiar_extension(ruta, nueva_extension):
    """
    Cambia la extensión de un archivo.
    """
    if "." not in ruta:
        return f"{ruta}.{nueva_extension}"

    base = ".".join(ruta.split(".")[:-1])
    return f"{base}.{nueva_extension}"


# ---------------- FORMATEO ----------------

def formatear_moneda(valor):
    """
    Formatea número como moneda.
    """
    try:
        return f"${float(valor):,.2f}"
    except:
        return valor


def formatear_numero(valor, decimales=2):
    """
    Formatea número con decimales.
    """
    try:
        return f"{float(valor):.{decimales}f}"
    except:
        return valor


# ---------------- DEBUG / LOG SIMPLE ----------------

def debug(mensaje):
    """
    Imprime mensajes de debug (se puede reemplazar por logging).
    """
    print(f"[DEBUG] {mensaje}")