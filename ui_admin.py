import tkinter as tk
from tkinter import ttk

from ui_usuarios import VentanaUsuarios
from ui_historial import VentanaHistorial
from ui_reportes import VentanaReportes

from tema import *


class VentanaAdmin(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Panel de Administración")

        self.geometry("1000x700")

        self.configure(
            bg=COLOR_FONDO
        )

        self.crear_widgets()

        self.bind(

            "<Escape>",

            lambda e: self.destroy()

        )
        
        
# =====================================
# WIDGETS
# =====================================

    def crear_widgets(self):

        # LOGO

        try:

            self.logo = tk.PhotoImage(
                file="assets/logo.png"
            )

            self.logo = self.logo.subsample(5,5)

            tk.Label(

                self,

                image=self.logo,

                bg=COLOR_FONDO

            ).pack(

                pady=(20,10)

            )

        except:

            pass


        # TITULO

        tk.Label(

            self,

            text="PANEL DE ADMINISTRACIÓN",

            bg=COLOR_FONDO,

            fg=COLOR_ROJO,

            font=FUENTE_TITULO

        ).pack(

            pady=(0,30)

        )


        frame_botones = tk.Frame(

            self,

            bg=COLOR_FONDO

        )

        frame_botones.pack()


        tk.Button(

            frame_botones,

            text="USUARIOS",

            bg=COLOR_VIOLETA,

            fg="white",

            width=25,

            height=2,

            font=FUENTE_BOTON,

            command=self.abrir_usuarios

        ).pack(

            pady=10

        )


        tk.Button(

            frame_botones,

            text="HISTORIAL",

            bg=COLOR_GRIS,

            fg="white",

            width=25,

            height=2,

            font=FUENTE_BOTON,

            command=self.abrir_historial

        ).pack(

            pady=10

        )


        tk.Button(

            frame_botones,

            text="REPORTES",

            bg=COLOR_CELESTE,

            fg="white",

            width=25,

            height=2,

            font=FUENTE_BOTON,

            command=self.abrir_reportes

        ).pack(

            pady=10

        )


        tk.Button(

            frame_botones,

            text="CERRAR",

            bg=COLOR_ROJO,

            fg="white",

            width=25,

            height=2,

            font=FUENTE_BOTON,

            command=self.destroy

        ).pack(

            pady=30

        )

# =====================================
# FUNCIONES
# =====================================

    def abrir_usuarios(self):

        VentanaUsuarios(

            self

        )


    def abrir_historial(self):

        VentanaHistorial(

            self

        )


    def abrir_reportes(self):

        VentanaReportes(

            self

        )


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    VentanaAdmin(root)

    root.mainloop()