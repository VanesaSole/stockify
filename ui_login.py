# ui_login.py

import tkinter as tk
from tkinter import ttk, messagebox

from ui_principal import VentanaPrincipal

from tema import *


class VentanaLogin:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Stockify V2")

        self.root.geometry("500x650")

        self.root.resizable(False, False)

        self.root.configure(
            bg=COLOR_FONDO
        )

        self.crear_widgets()

        self.root.bind(
            "<Return>",
            self.ingresar
        )

        self.root.bind(
            "<Escape>",
            lambda e: self.root.destroy()
        )

        self.entry_usuario.focus()

        self.root.mainloop()


    # ====================================
    # WIDGETS
    # ====================================

    def crear_widgets(self):

        frame = tk.Frame(

            self.root,

            bg=COLOR_FONDO

        )

        frame.pack(

            fill="both",

            expand=True

        )


        # LOGO

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo.png"
            )
            self.logo = self.logo.subsample(4, 4)

            tk.Label(

                frame,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(

                pady=(30,10)

            )

        except:

            pass


        # TITULO

        tk.Label(

            frame,

            text="STOCKIFY",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_TITULO

        ).pack()


        tk.Label(

            frame,

            text="Versión Beta",

            bg=COLOR_FONDO,

            fg="gray",

            font=FUENTE_NORMAL

        ).pack(

            pady=(0,30)

        )


        # USUARIO

        tk.Label(

            frame,

            text="Usuario",

            bg=COLOR_FONDO,

            font=FUENTE_SUBTITULO

        ).pack()

        self.entry_usuario = ttk.Entry(

            frame,

            width=30

        )

        self.entry_usuario.pack(

            pady=10,

            ipady=5

        )


        # PASSWORD

        tk.Label(

            frame,

            text="Contraseña",

            bg=COLOR_FONDO,

            font=FUENTE_SUBTITULO

        ).pack(

            pady=(15,0)

        )

        self.entry_password = ttk.Entry(

            frame,

            width=30,

            show="*"

        )

        self.entry_password.pack(

            pady=10,

            ipady=5

        )


        # RECORDAR

        self.recordar = tk.BooleanVar()

        ttk.Checkbutton(

            frame,

            text="Recordarme",

            variable=self.recordar

        ).pack(

            pady=20

        )


        # BOTON

        tk.Button(

            frame,

            text="INGRESAR",

            bg=COLOR_AZUL,

            fg="white",

            font=FUENTE_BOTON,

            width=20,

            command=self.ingresar

        ).pack(

            pady=15,

            ipady=8

        )


        # PIE

        tk.Label(

            frame,

            text="Stockify V2 - 2026",

            bg=COLOR_FONDO,

            fg="gray"

        ).pack(

            side="bottom",

            pady=20

        )


    def ingresar(self, event=None):

        usuario = self.entry_usuario.get()

        password = self.entry_password.get()


        from auth import validar_login

        user_data = validar_login(usuario, password)


        if user_data:

            messagebox.showinfo(

                "Stockify",

                "Login correcto"

            )

            # Ocultamos la ventana de login y abrimos la principal como Toplevel
            # para no crear una nueva instancia de Tk y evitar nested mainloops.
            self.root.withdraw()
            VentanaPrincipal(user_data, master=self.root)

        else:

            messagebox.showerror(

                "Error",

                "Usuario o contraseña incorrectos o cuenta inactiva"

            )


if __name__ == "__main__":

    VentanaLogin()