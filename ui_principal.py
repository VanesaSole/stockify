# ==========================================
# ui_principal.py
# Stockify V3
# ==========================================

import tkinter as tk
from datetime import datetime

from tema import *

from ui_pedidos import VentanaPedidos
from ui_envios import VentanaEnvios
from ui_historial import VentanaHistorial
from ui_reportes import VentanaReportes
from ui_usuarios import VentanaUsuarios
from ui_admin import VentanaAdmin


class VentanaPrincipal:

    def __init__(self, usuario=None, master=None):

        self.usuario = usuario

        self.master = master

        self.root = tk.Tk()

        self.root.title("Stockify V3")

        self.root.geometry("1600x900")

        self.root.minsize(1400, 800)

        self.root.configure(
            bg=COLOR_FONDO
        )

        try:
            self.root.state("zoomed")
        except:
            pass

# =====================================
# NAVEGACIÓN DEL MENÚ
# =====================================

        self.menu_actual = 0

        self.crear_widgets()
        
        self.aplicar_permisos()
        
        self.configurar_atajos()
        
        self.actualizar_menu()

        self.root.bind("<Up>", self.menu_arriba)
        self.root.bind("<Down>", self.menu_abajo)
        self.root.bind("<Return>", self.menu_enter)

        self.actualizar_reloj()

        self.root.mainloop()

    # =====================================
    # INICIO
    # =====================================

    def inicio(self):
        pass
    
    # =====================================
# INTERFAZ PRINCIPAL
# =====================================

    def crear_widgets(self):

        # ==========================
        # CONTENEDOR GENERAL
        # ==========================

        self.frame_principal = tk.Frame(
            self.root,
            bg=COLOR_FONDO
        )

        self.frame_principal.pack(
            fill="both",
            expand=True
        )

        # ==========================
        # MENU LATERAL
        # ==========================

        self.frame_menu = tk.Frame(
            self.frame_principal,
            bg=COLOR_PANEL,
            width=260
        )

        self.frame_menu.pack(
            side="left",
            fill="y"
        )

        self.frame_menu.pack_propagate(False)

        # ==========================
        # CONTENIDO
        # ==========================

        self.frame_contenido = tk.Frame(
            self.frame_principal,
            bg=COLOR_FONDO
        )

        self.frame_contenido.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==========================
        # LOGO
        # ==========================

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo.png"
            )

            self.logo = self.logo.subsample(6,6)

            tk.Label(

                self.frame_menu,

                image=self.logo,

                bg=COLOR_PANEL

            ).pack(
                pady=(20,5)
            )

        except:

            pass

        tk.Label(

            self.frame_menu,

            text="Stockify",

            bg=COLOR_PANEL,

            fg=COLOR_BLANCO,

            font=("Segoe UI",20,"bold")

        ).pack()

        tk.Label(

            self.frame_menu,

            text="Sistema de Gestión",

            bg=COLOR_PANEL,

            fg=COLOR_GRIS,

            font=("Segoe UI",10)

        ).pack(
            pady=(0,25)
        )

        # ==========================
        # MENU
        # ==========================

        self.frame_botones = tk.Frame(
            self.frame_menu,
            bg=COLOR_PANEL
        )

        self.frame_botones.pack(
            fill="x",
            padx=12
        )

        self.menu_botones = []

        self.crear_boton(
            "🏠  Inicio",
            "F1",
            COLOR_AZUL,
            self.inicio
        )

        self.crear_boton(
            "📦  Pedidos",
            "F2",
            COLOR_AZUL,
            self.abrir_pedidos
        )

        self.crear_boton(
            "🚚  Envíos",
            "F3",
            COLOR_VERDE,
            self.abrir_envios
        )

        self.crear_boton(
            "📊  Reportes",
            "F4",
            COLOR_CELESTE,
            self.abrir_reportes
        )

        self.crear_boton(
            "🕓  Historial",
            "F5",
            COLOR_TOPO,
            self.abrir_historial
        )

        self.crear_boton(
            "👤  Usuarios",
            "F6",
            COLOR_VIOLETA,
            self.abrir_usuarios
        )

        self.crear_boton(
            "⚙  Administración",
            "F7",
            COLOR_ROJO,
            self.abrir_admin
        )

        tk.Frame(
            self.frame_menu,
            bg=COLOR_PANEL
        ).pack(
            fill="both",
            expand=True
        )

        self.crear_boton(
            "🚪  Salir",
            "F8",
            "#555555",
            self.root.destroy
        )

        # ==========================
        # ENCABEZADO
        # ==========================

        self.frame_superior = tk.Frame(
            self.frame_contenido,
            bg=COLOR_FONDO,
            height=80
        )

        self.frame_superior.pack(
            fill="x",
            padx=30,
            pady=(25,10)
        )

        self.frame_superior.pack_propagate(False)

        tk.Label(

            self.frame_superior,

            text="Dashboard",

            bg=COLOR_FONDO,

            fg=COLOR_BLANCO,

            font=("Segoe UI",24,"bold")

        ).pack(
            anchor="w"
        )

        self.lbl_fecha = tk.Label(

            self.frame_superior,

            bg=COLOR_FONDO,

            fg=COLOR_GRIS,

            font=("Segoe UI",11)

        )

        self.lbl_fecha.pack(
            anchor="w"
        )
        
        nombre = "Invitado"

        if self.usuario:
            nombre = self.usuario[1]

        tk.Label(

            self.frame_superior,

            text=f"Usuario: {nombre}",

            bg=COLOR_FONDO,

            fg=COLOR_BLANCO,

            font=("Segoe UI",11,"bold")

        ).pack(
            anchor="w",
            pady=(5,0)
        )
        
        
# =====================================
# DASHBOARD
# =====================================

        self.dashboard = tk.Frame(

            self.frame_contenido,

            bg=COLOR_FONDO

        )

        self.dashboard.pack(

            fill="both",

            expand=True,

            padx=30,

            pady=10

        )

        # ==============================
        # FILA SUPERIOR
        # ==============================

        fila1 = tk.Frame(

            self.dashboard,

            bg=COLOR_FONDO

        )

        fila1.pack(

            fill="x",

            pady=10

        )

        self.crear_panel(

            fila1,

            "📦 Pedidos del día",

            COLOR_AZUL

        )

        self.crear_panel(

            fila1,

            "🚚 Envíos del día",

            COLOR_VERDE

        )

        # ==============================
        # FILA CENTRAL
        # ==============================

        fila2 = tk.Frame(

            self.dashboard,

            bg=COLOR_FONDO

        )

        fila2.pack(

            fill="x",

            pady=10

        )

        self.crear_panel(

            fila2,

            "📊 Reportes",

            COLOR_CELESTE

        )

        self.crear_panel(

            fila2,

            "📈 Estadísticas",

            COLOR_VIOLETA

        )

        # ==============================
        # FILA INFERIOR
        # ==============================

        fila3 = tk.Frame(

            self.dashboard,

            bg=COLOR_FONDO

        )

        fila3.pack(

            fill="both",

            expand=True,

            pady=10

        )

        self.crear_panel(

            fila3,

            "📝 Actividad reciente",

            COLOR_TOPO,

            expandir=True

        )

        self.crear_panel(

            fila3,

            "⚠ Alertas",

            COLOR_ROJO,

            expandir=True

        )

# =====================================
# CREAR BOTON DEL MENÚ
# =====================================

    def crear_boton(self, texto, tecla, color, comando):

        boton = tk.Button(

            self.frame_botones,

            text=f"{texto:<20} {tecla}",

            bg=color,

            fg="white",

            activebackground=color,

            activeforeground="white",

            relief="flat",

            bd=0,

            padx=15,

            pady=12,

            anchor="w",

            font=("Segoe UI",11,"bold"),

            command=comando

        )

        boton.pack(

            fill="x",

            pady=5

        )

        self.menu_botones.append(boton)
        
# =====================================
# PANEL DASHBOARD
# =====================================

    def crear_panel(self, parent, titulo, color, expandir=False):

        panel = tk.Frame(

            parent,

            bg=COLOR_PANEL,

            highlightbackground=color,

            highlightthickness=2

        )

        panel.pack(

            side="left",

            fill="both",

            expand=True,

            padx=8,

            pady=5

        )

        if expandir:

            panel.configure(height=250)

        else:

            panel.configure(height=150)

        panel.pack_propagate(False)

        tk.Label(

            panel,

            text=titulo,

            bg=COLOR_PANEL,

            fg="white",

            font=("Segoe UI",13,"bold")

        ).pack(

            anchor="w",

            padx=15,

            pady=(15,10)

        )

        tk.Label(

            panel,

            text="Sin información",

            bg=COLOR_PANEL,

            fg=COLOR_GRIS,

            font=("Segoe UI",11)

        ).pack(

            expand=True
        )
        
    # =====================================
    # RELOJ
    # =====================================

    def actualizar_reloj(self):

        self.lbl_fecha.config(
            text=datetime.now().strftime("%d/%m/%Y   %H:%M:%S")
        )

        self.root.after(1000, self.actualizar_reloj)


    # =====================================
    # NAVEGACIÓN DEL MENÚ
    # =====================================

    def actualizar_menu(self):

        for i, boton in enumerate(self.menu_botones):

            if i == self.menu_actual:

                boton.configure(
                    relief="solid",
                    bd=3,
                    highlightbackground="white",
                    highlightthickness=2
                )

                boton.focus_set()

            else:

                boton.configure(
                    relief="flat",
                    bd=0,
                    highlightthickness=0
                )
    
    # =====================================
# PERMISOS POR ROL
# =====================================

    def aplicar_permisos(self):

        if not self.usuario:
            return

        rol = self.usuario[3]

        # ADMIN -> ve todo
        if rol == "ADMIN":
            return

        # VENDEDOR
        if rol == "VENDEDOR":

            self.menu_botones[3].pack_forget()   # Reportes
            self.menu_botones[4].pack_forget()   # Historial
            self.menu_botones[5].pack_forget()   # Usuarios
            self.menu_botones[6].pack_forget()   # Administración

        # ENCARGADO
        elif rol == "ENCARGADO":

            self.menu_botones[2].pack_forget()   # Envíos
            self.menu_botones[3].pack_forget()   # Reportes
            self.menu_botones[4].pack_forget()   # Historial
            self.menu_botones[5].pack_forget()   # Usuarios
            self.menu_botones[6].pack_forget()   # Administración


    def menu_arriba(self, event=None):

        self.menu_actual -= 1

        if self.menu_actual < 0:
            self.menu_actual = len(self.menu_botones) - 1

        self.actualizar_menu()


    def menu_abajo(self, event=None):

        self.menu_actual += 1

        if self.menu_actual >= len(self.menu_botones):
            self.menu_actual = 0

        self.actualizar_menu()


    def menu_enter(self, event=None):

        self.menu_botones[self.menu_actual].invoke()
        
# =====================================
# ATAJOS SEGÚN EL ROL
# =====================================

    def configurar_atajos(self):

        self.root.bind("<F1>", lambda e: self.inicio())
        self.root.bind("<F2>", lambda e: self.abrir_pedidos())
        self.root.bind("<F8>", lambda e: self.root.destroy())

        if not self.usuario:
            return

        rol = self.usuario[3]

        if rol in ("ADMIN", "VENDEDOR"):

            self.root.bind("<F3>", lambda e: self.abrir_envios())

        if rol == "ADMIN":

            self.root.bind("<F4>", lambda e: self.abrir_reportes())
            self.root.bind("<F5>", lambda e: self.abrir_historial())
            self.root.bind("<F6>", lambda e: self.abrir_usuarios())
            self.root.bind("<F7>", lambda e: self.abrir_admin())


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

        if not self.usuario or self.usuario[3] != "ADMIN":

            from tkinter import messagebox

            messagebox.showerror(
                "Acceso Denegado",
                "Solo el administrador puede acceder a la gestión de usuarios."
            )

            return

        VentanaUsuarios(self.root)


    def abrir_admin(self):

        if not self.usuario or self.usuario[3] != "ADMIN":

            from tkinter import messagebox

            messagebox.showerror(
                "Acceso Denegado",
                "Solo el administrador puede acceder al panel de administración."
            )

            return

        VentanaAdmin(self.root)


        if __name__ == "__main__":

            VentanaPrincipal()