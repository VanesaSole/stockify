# login_ui.py

import tkinter as tk

from tkinter import messagebox

from auth import (
    registrar_usuario,
    iniciar_sesion
)

from ui import App


class LoginUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Stockify Login")

        self.root.geometry("500x600")

        self.root.resizable(False, False)

        self.crear_login()

    # ==================================================
    # LOGIN
    # ==================================================

    def crear_login(self):

        self.limpiar()

        tk.Label(
            self.root,
            text="STOCKIFY",
            font=("Arial", 28, "bold"),
            fg="#173A7A"
        ).pack(pady=30)

        tk.Label(
            self.root,
            text="Email"
        ).pack()

        self.email = tk.Entry(
            self.root,
            width=35
        )

        self.email.pack(pady=5)

        tk.Label(
            self.root,
            text="Contraseña"
        ).pack()

        self.password = tk.Entry(
            self.root,
            width=35,
            show="*"
        )

        self.password.pack(pady=5)

        tk.Button(
            self.root,
            text="Iniciar Sesión",
            width=25,
            bg="#173A7A",
            fg="white",
            command=self.login
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Registrarse",
            width=25,
            command=self.crear_registro
        ).pack()

    # ==================================================
    # REGISTRO
    # ==================================================

    def crear_registro(self):

        self.limpiar()

        tk.Label(
            self.root,
            text="Registro",
            font=("Arial", 24, "bold"),
            fg="#173A7A"
        ).pack(pady=20)

        self.reg_nombre = self.crear_input("Nombre")

        self.reg_email = self.crear_input("Email")

        self.reg_password = self.crear_input(
            "Contraseña",
            oculto=True
        )

        self.reg_repetir = self.crear_input(
            "Repetir Contraseña",
            oculto=True
        )

        self.reg_direccion = self.crear_input("Dirección")

        self.reg_telefono = self.crear_input("Teléfono")

        tk.Button(
            self.root,
            text="Crear Cuenta",
            width=25,
            bg="#173A7A",
            fg="white",
            command=self.registrar
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Volver",
            width=25,
            command=self.crear_login
        ).pack()

    # ==================================================
    # INPUTS
    # ==================================================

    def crear_input(
        self,
        texto,
        oculto=False
    ):

        tk.Label(
            self.root,
            text=texto
        ).pack()

        entry = tk.Entry(
            self.root,
            width=35,
            show="*" if oculto else ""
        )

        entry.pack(pady=5)

        return entry

    # ==================================================
    # REGISTRAR
    # ==================================================

    def registrar(self):

        nombre = self.reg_nombre.get()

        email = self.reg_email.get()

        password = self.reg_password.get()

        repetir = self.reg_repetir.get()

        direccion = self.reg_direccion.get()

        telefono = self.reg_telefono.get()

        if password != repetir:

            messagebox.showerror(
                "Error",
                "Las contraseñas no coinciden"
            )

            return

        resultado = registrar_usuario(
            nombre,
            email,
            password,
            direccion,
            telefono
        )

        if resultado is True:

            messagebox.showinfo(
                "OK",
                "Cuenta creada"
            )

            self.crear_login()

        else:

            messagebox.showerror(
                "Error",
                str(resultado)
            )

    # ==================================================
    # LOGIN
    # ==================================================

    def login(self):

        email = self.email.get()

        password = self.password.get()

        usuario = iniciar_sesion(
            email,
            password
        )

        if not usuario:

            messagebox.showerror(
                "Error",
                "Credenciales incorrectas"
            )

            return

        # cerrar login
        self.limpiar()

        # abrir app
        App(
            self.root,
            usuario
        )

    # ==================================================
    # LIMPIAR
    # ==================================================

    def limpiar(self):

        for widget in self.root.winfo_children():

            widget.destroy()