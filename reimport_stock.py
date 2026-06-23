import sqlite3
import pandas as pd

print("=" * 60)
print("REIMPORTACIÓN DE CATÁLOGO CON STOCK")
print("=" * 60)

# Leer Excel
df = pd.read_excel('assets/catalogo.xlsx')

# Limpiar nombres
df.columns = [
    str(col).replace("\n", "").replace("\r", "").strip()
    for col in df.columns
]

print(f"Leyendo {len(df)} productos del Excel...")

# Conectar BD
conn = sqlite3.connect('stockify.db')
cursor = conn.cursor()

# Función para limpiar números
def limpiar_numero(valor):
    if valor is None or str(valor).strip() == "-":
        return 0
    valor = str(valor)
    valor = valor.replace("$", "").replace(",", "").strip()
    try:
        return float(valor)
    except:
        return 0

actualizado = 0
no_encontrado = 0

for _, fila in df.iterrows():
    producto = str(fila.get('Producto', '')).strip()
    
    if not producto or producto == "nan":
        continue
    
    # Leer stock
    stock = limpiar_numero(fila.get('Existencia', 0))
    
    # Actualizar en BD
    cursor.execute("""
    UPDATE productos 
    SET stock = ?
    WHERE nombre = ?
    """, (stock, producto))
    
    if cursor.rowcount > 0:
        actualizado += 1
    else:
        no_encontrado += 1

conn.commit()
conn.close()

print(f"✓ {actualizado} productos actualizados con stock")
print(f"⚠ {no_encontrado} productos no encontrados en BD")
print("\n✓ Reimportación completada")

# Verificar
conn = sqlite3.connect('stockify.db')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM productos WHERE stock > 0")
con_stock = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM productos WHERE stock = 0")
sin_stock = cursor.fetchone()[0]
conn.close()

print(f"\nEstadísticas:")
print(f"  Productos con stock: {con_stock}")
print(f"  Productos sin stock: {sin_stock}")
