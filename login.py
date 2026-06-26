import tkinter as tk
from tkinter import messagebox

from database import iniciar_sesion
from tema import *

from register import RegisterWindow
from recover import RecoverWindow


class LoginWindow:

    def __init__(self, root, abrir_sistema):

        self.root = root

        self.abrir_sistema = abrir_sistema

        root.title("Stockify Login")

        root.geometry("450x500")
        root.configure(bg=COLOR_FONDO)

        tk.Label(
            root,
            text="STOCKIFY",
            font=("Arial", 24, "bold"),
            fg=COLOR_AZUL,
            bg=COLOR_FONDO
        ).pack(pady=30)

        tk.Label(
            root,
            text="Email",
            fg=COLOR_BLANCO,
            bg=COLOR_FONDO,
            font=FUENTE_NORMAL
        ).pack()

        self.entry_email = tk.Entry(
            root,
            width=35,
            bg=COLOR_PANEL,
            fg=COLOR_BLANCO,
            insertbackground=COLOR_BLANCO,
            relief="flat"
        )

        self.entry_email.pack(pady=5)

        tk.Label(
            root,
            text="Contraseña",
            fg=COLOR_BLANCO,
            bg=COLOR_FONDO,
            font=FUENTE_NORMAL
        ).pack()

        self.entry_password = tk.Entry(
            root,
            show="*",
            width=35
        )

        self.entry_password.pack(pady=5)

        tk.Button(
            root,
            text="Iniciar Sesión",
            bg=COLOR_AZUL,
            fg=COLOR_BLANCO,
            width=25,
            command=self.login
        ).pack(pady=20)

        tk.Button(
            root,
            text="Registrarse",
            width=25,
            bg=COLOR_PANEL,
            fg=COLOR_BLANCO,
            activebackground=COLOR_AZUL,
            command=self.abrir_registro
        ).pack(pady=5)

        tk.Button(
            root,
            text="Recuperar Contraseña",
            width=25,
            bg=COLOR_PANEL,
            fg=COLOR_BLANCO,
            activebackground=COLOR_AZUL,
            command=self.abrir_recuperacion
        ).pack(pady=5)

        # NAVEGACION

        self.entry_email.bind(
            "<Return>",
            lambda e: self.entry_password.focus()
        )

        self.entry_password.bind(
            "<Return>",
            lambda e: self.login()
        )

        self.entry_email.bind(
            "<Down>",
            lambda e: self.entry_password.focus()
        )

        self.entry_password.bind(
            "<Up>",
            lambda e: self.entry_email.focus()
        )

    def login(self):

        email = self.entry_email.get()

        password = self.entry_password.get()

        usuario = iniciar_sesion(
            email,
            password
        )

        if usuario:

            self.root.destroy()

            self.abrir_sistema(usuario)

        else:

            messagebox.showerror(
                "Error",
                "Datos incorrectos"
            )

    def abrir_registro(self):

        ventana = tk.Toplevel(self.root)

        RegisterWindow(ventana)

    def abrir_recuperacion(self):

        ventana = tk.Toplevel(self.root)

        RecoverWindow(ventana)