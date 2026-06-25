# ui_principal.py

import tkinter as tk
from tkinter import ttk
from datetime import datetime

from ui_pedidos import VentanaPedidos
from ui_envios import VentanaEnvios
from ui_historial import VentanaHistorial
from ui_reportes import VentanaReportes
from ui_usuarios import VentanaUsuarios
from ui_admin import VentanaAdmin
from tema import *

class VentanaPrincipal:

    def __init__(self, usuario=None, master=None):

        # VentanaPrincipal siempre administra su propia ventana raíz
        # (tk.Tk()), incluso si se le pasa un "master": Tkinter no
        # admite múltiples instancias de Tk() en el mismo proceso,
        # así que cualquier ventana anterior (por ejemplo, el login)
        # debe destruirse antes de llegar a este punto.
        self._master_externo = master

        self.root = tk.Tk()

        self.usuario = usuario

        self.root.title("Stockify V2")

        self.root.geometry("900x650")

        self.root.resizable(True, True)

        self.crear_widgets()

        # Atajos teclado

        self.root.bind("<F1>", lambda e: self.abrir_pedidos())

        self.root.bind("<F2>", lambda e: self.abrir_envios())

        self.root.bind("<F3>", lambda e: self.abrir_historial())

        self.root.bind("<F4>", lambda e: self.abrir_reportes())

        self.root.mainloop()


    # ===================================
    # WIDGETS
    # ===================================

    def crear_widgets(self):

        self.root.configure(
            bg=COLOR_FONDO
        )

        # ==========================
        # LOGO
        # ==========================

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo.png"
            )
            self.logo = self.logo.subsample(4, 4)

            tk.Label(

                self.root,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(

                pady=(20,10)

            )

        except:

            pass


        # ==========================
        # TITULO
        # ==========================

        tk.Label(

            self.root,

            text="STOCKIFY V2",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_TITULO

        ).pack()


        tk.Label(

            self.root,

            text=datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),

            bg=COLOR_FONDO,

            fg=COLOR_GRIS,

            font=FUENTE_NORMAL

        ).pack(

            pady=(0,20)

        )


        # ==========================
        # BOTONES
        # ==========================

        frame_botones = tk.Frame(

            self.root,

            bg=COLOR_FONDO

        )

        frame_botones.pack()


        # FILA 1

        tk.Button(

            frame_botones,

            text="Nuevo Pedido",

            bg=COLOR_AZUL,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_pedidos

        ).grid(

            row=0,

            column=0,

            padx=15,

            pady=10

        )


        tk.Button(

            frame_botones,

            text="Nuevo Envío",

            bg=COLOR_VERDE,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_envios

        ).grid(

            row=0,

            column=1,

            padx=15,

            pady=10

        )


        # FILA 2

        tk.Button(

            frame_botones,

            text="Historial",

            bg=COLOR_TOPO,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_historial

        ).grid(

            row=1,

            column=0,

            padx=15,

            pady=10

        )


        tk.Button(

            frame_botones,

            text="Reportes",

            bg=COLOR_CELESTE,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_reportes

        ).grid(

            row=1,

            column=1,

            padx=15,

            pady=10

        )


        # FILA 3

        tk.Button(

            frame_botones,

            text="Usuarios",

            bg=COLOR_VIOLETA,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_usuarios

        ).grid(

            row=2,

            column=0,

            padx=15,

            pady=10

        )


        tk.Button(

            frame_botones,

            text="Administración",

            bg=COLOR_ROJO,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            height=2,

            command=self.abrir_admin

        ).grid(

            row=2,

            column=1,

            padx=15,

            pady=10

        )


        # ==========================
        # SALIR
        # ==========================

        tk.Button(

            self.root,

            text="Salir",

            width=20,

            height=2,

            font=FUENTE_BOTON,

            command=self.root.destroy

        ).pack(

            pady=25

        )
    
    
    # ===================================
    # VENTANAS
    # ===================================

    def abrir_pedidos(self):

        VentanaPedidos(self.root, self.usuario)


    def abrir_envios(self):

        VentanaEnvios(self.root)


    def abrir_historial(self):

        VentanaHistorial(self.root)


    def abrir_reportes(self):

        VentanaReportes(self.root)


    def abrir_usuarios(self):

        if not self.usuario or self.usuario[2] != "ADMIN":

            from tkinter import messagebox

            messagebox.showerror("Acceso Denegado", "Solo el administrador puede acceder a la gestión de usuarios.")

            return

        VentanaUsuarios(self.root)


    def abrir_admin(self):

        if not self.usuario or self.usuario[2] != "ADMIN":

            from tkinter import messagebox

            messagebox.showerror("Acceso Denegado", "Solo el administrador puede acceder al panel de administración.")

            return

        VentanaAdmin(self.root)


if __name__ == "__main__":

    VentanaPrincipal()