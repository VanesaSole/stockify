import tkinter as tk
from tkinter import messagebox

from database import registrar_usuario
from tema import *


class RegisterWindow:

    def __init__(self, root):

        self.root = root

        root.title("Registro")

        root.geometry("500x750")
        root.configure(bg=COLOR_FONDO)

        self.crear_campos()

    def crear_campos(self):

        labels = [

            "Nombre",
            "Email",
            "Dirección",
            "Contraseña",

            "Pregunta 1",
            "Respuesta 1",

            "Pregunta 2",
            "Respuesta 2",

            "Pregunta 3",
            "Respuesta 3"

        ]

        self.entries = []

        for texto in labels:

            tk.Label(
                self.root,
                text=texto,
                bg=COLOR_FONDO,
                font=FUENTE_NORMAL
            ).pack()

            entry = tk.Entry(
                self.root,
                width=40,
                bg=COLOR_PANEL,
                fg=COLOR_BLANCO,
                insertbackground=COLOR_BLANCO,
                relief="flat"
            )

            entry.pack(pady=4)

            self.entries.append(entry)

        # NAVEGACION

        for i in range(len(self.entries) - 1):

            self.entries[i].bind(
                "<Return>",
                lambda e, idx=i:
                self.entries[idx + 1].focus()
            )

            self.entries[i].bind(
                "<Down>",
                lambda e, idx=i:
                self.entries[idx + 1].focus()
            )

        for i in range(1, len(self.entries)):

            self.entries[i].bind(
                "<Up>",
                lambda e, idx=i:
                self.entries[idx - 1].focus()
            )

        self.entries[-1].bind(
            "<Return>",
            lambda e: self.registrar()
        )

        tk.Button(
            self.root,
            text="Crear Cuenta",
            bg=COLOR_AZUL,
            fg=COLOR_BLANCO,
            width=25,
            command=self.registrar
        ).pack(pady=20)

    def registrar(self):

        datos = [

            e.get()

            for e in self.entries

        ]

        ok = registrar_usuario(*datos)

        if ok is True:

            messagebox.showinfo(
                "OK",
                "Cuenta creada"
            )

            self.root.destroy()

        else:

            messagebox.showerror(
                "Error",
                str(ok)
            )