# pedidos.py

from database import obtener_conexion
from inventario import obtener_producto, quitar_stock
from historial import registrar_movimiento
from datetime import datetime


class Pedido:

    def __init__(self):

        self.items = []


    # =====================================================
    # AGREGAR PRODUCTO
    # =====================================================

    def agregar_producto(

        self,

        producto_id,

        cantidad,

        tipo="UNIDAD"

    ):

        producto = obtener_producto(
            producto_id
        )

        if not producto:

            return False

        nombre = producto[2]

        stock = producto[3]

        paq = producto[4]

        costo = producto[5]
        
        venta = producto[6]  # PRECIO DE VENTA

        if tipo.upper() == "BULTO":

            unidades = cantidad * paq

        else:

            unidades = cantidad

        # Usar PRECIO DE VENTA para el cálculo del subtotal
        subtotal = unidades * venta

        item = {

            "producto_id": producto_id,

            "nombre": nombre,

            "tipo": tipo,

            "cantidad": cantidad,

            "unidades": unidades,

            "precio": venta,  # Mostrar precio de venta
            "precio_unitario": venta,  # Precio unitario (después de PAQ)
            "subtotal": subtotal,

            "stock": stock

        }

        self.items.append(item)

        return True


    # =====================================================
    # ELIMINAR PRODUCTO
    # =====================================================

    def eliminar_producto(
        self,
        indice
    ):

        if 0 <= indice < len(self.items):

            self.items.pop(indice)


    # =====================================================
    # OBTENER ITEMS
    # =====================================================

    def obtener_items(self):

        return self.items


    # =====================================================
    # VACIAR PEDIDO
    # =====================================================

    def vaciar(self):

        self.items = []


    # =====================================================
    # TOTAL
    # =====================================================

    def calcular_total(self):

        total = 0

        for item in self.items:

            total += item["subtotal"]

        return total


    # =====================================================
    # ESTADO STOCK
    # =====================================================

    def obtener_estado_stock(

        self,

        producto_id,

        cantidad,

        tipo="UNIDAD"

    ):

        producto = obtener_producto(
            producto_id
        )

        if not producto:

            return "ROJO"

        stock = producto[3]

        paq = producto[4]

        if tipo.upper() == "BULTO":

            unidades = cantidad * paq

        else:

            unidades = cantidad

        if stock == 0:

            return "ROJO"

        if unidades > stock:

            return "AMARILLO"

        return "VERDE"


    # =====================================================
    # GUARDAR PEDIDO
    # =====================================================

    def guardar_pedido(

        self,

        usuario_id,

        sucursal_id,

        estado="PENDIENTE"

    ):

        if len(self.items) == 0:

            return False

        conn = obtener_conexion()

        cursor = conn.cursor()

        total = self.calcular_total()

        cursor.execute("""

        INSERT INTO pedidos (

            fecha,
            usuario_id,
            sucursal_id,
            estado,
            total

        )

        VALUES (?, ?, ?, ?, ?)

        """, (

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            usuario_id,

            sucursal_id,

            estado,

            total

        ))

        pedido_id = cursor.lastrowid


        # ======================================
        # DETALLE PEDIDO
        # ======================================

        for item in self.items:

            cursor.execute("""

            INSERT INTO detalle_pedido (

                pedido_id,
                producto_id,
                cantidad,
                unidades,
                precio,
                subtotal

            )

            VALUES (?, ?, ?, ?, ?, ?)

            """, (

                pedido_id,

                item["producto_id"],

                item["cantidad"],

                item["unidades"],

                item["precio"],

                item["subtotal"]

            ))

        conn.commit()

        conn.close()

        return pedido_id


    # =====================================================
    # DESCONTAR STOCK
    # =====================================================

    def descontar_stock(self):

        for item in self.items:

            quitar_stock(

                item["producto_id"],

                item["unidades"]

            )


    # =====================================================
    # REGISTRAR MOVIMIENTOS
    # =====================================================

    def registrar_movimientos(

        self,

        usuario_id

    ):

        for item in self.items:

            registrar_movimiento(

                usuario_id=usuario_id,

                producto_id=item["producto_id"],

                tipo="PEDIDO",

                cantidad=item["unidades"],

                observacion="Pedido generado"

            )


    # =====================================================
    # PROCESAR PEDIDO COMPLETO
    # =====================================================

    def procesar_pedido(

        self,

        usuario_id,

        sucursal_id,

        estado="PENDIENTE"

    ):

        pedido_id = self.guardar_pedido(

            usuario_id,

            sucursal_id,

            estado

        )

        if not pedido_id:

            return False

        self.descontar_stock()

        self.registrar_movimientos(

            usuario_id

        )

        return pedido_id