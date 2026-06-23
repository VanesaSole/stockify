import tkinter as tk
from tkinter import messagebox

from database import (
    obtener_usuario_por_email,
    actualizar_password
)


class RecoverWindow:

    def __init__(self, root):

        self.root = root

        root.title("Recuperar Contraseña")

        root.geometry("500x650")

        tk.Label(
            root,
            text="Email"
        ).pack(pady=10)

        self.entry_email = tk.Entry(
            root,
            width=40
        )

        self.entry_email.pack()

        tk.Button(
            root,
            text="Buscar Usuario",
            command=self.buscar_usuario
        ).pack(pady=15)

    def buscar_usuario(self):

        self.email = self.entry_email.get()

        usuario = obtener_usuario_por_email(
            self.email
        )

        if not usuario:

            messagebox.showerror(
                "Error",
                "Usuario no encontrado"
            )

            return

        self.usuario = usuario

        preguntas = [

            usuario[6],
            usuario[8],
            usuario[10]

        ]

        self.respuestas = []

        for p in preguntas:

            tk.Label(
                self.root,
                text=p
            ).pack()

            e = tk.Entry(
                self.root,
                width=40
            )

            e.pack(pady=4)

            self.respuestas.append(e)

        tk.Label(
            self.root,
            text="Nueva contraseña"
        ).pack(pady=10)

        self.nueva_password = tk.Entry(
            self.root,
            show="*",
            width=40
        )

        self.nueva_password.pack()

        tk.Button(
            self.root,
            text="Cambiar Contraseña",
            bg="#173A7A",
            fg="white",
            command=self.validar
        ).pack(pady=20)

    def validar(self):

        ok1 = (
            self.respuestas[0].get().lower()
            == self.usuario[7]
        )

        ok2 = (
            self.respuestas[1].get().lower()
            == self.usuario[9]
        )

        ok3 = (
            self.respuestas[2].get().lower()
            == self.usuario[11]
        )

        if ok1 and ok2 and ok3:

            actualizar_password(
                self.email,
                self.nueva_password.get()
            )

            messagebox.showinfo(
                "OK",
                "Contraseña actualizada"
            )

            self.root.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Respuestas incorrectas"
            )