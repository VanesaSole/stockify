import tkinter as tk
from tkinter import ttk, messagebox

from usuarios import obtener_usuarios, activar_usuario, desactivar_usuario

from tema import *


class VentanaUsuarios(tk.Toplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Usuarios")

        self.geometry("1400x850")

        self.configure(
            bg=COLOR_FONDO
        )

        self.crear_widgets()

        self.cargar_datos()

        self.bind(

            "<Escape>",

            lambda e: self.destroy()

        )
        
        
# ====================================
# WIDGETS
# ====================================

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

                pady=(10,5)

            )

        except:

            pass


        # TITULO

        tk.Label(

            self,

            text="USUARIOS",

            bg=COLOR_FONDO,

            fg=COLOR_VIOLETA,

            font=FUENTE_TITULO

        ).pack(

            pady=(0,10)

        )


        frame_superior = tk.Frame(

            self,

            bg=COLOR_FONDO

        )

        frame_superior.pack(

            fill="x",

            padx=10,

            pady=10

        )


        tk.Button(

            frame_superior,

            text="Actualizar",

            bg=COLOR_AZUL,

            fg="white",

            font=FUENTE_BOTON,

            command=self.cargar_datos

        ).pack(

            side="left",

            padx=5

        )


        tk.Button(

            frame_superior,

            text="Nuevo Usuario",

            bg=COLOR_VERDE,

            fg="white",

            font=FUENTE_BOTON,

            command=self.abrir_nuevo_usuario

        ).pack(

            side="left",

            padx=5

        )


        tk.Button(

            frame_superior,

            text="Habilitar",

            bg=COLOR_CELESTE,

            fg="white",

            font=FUENTE_BOTON,

            command=self.habilitar_usuario

        ).pack(

            side="left",

            padx=5

        )


        tk.Button(

            frame_superior,

            text="Deshabilitar",

            bg=COLOR_GRIS,

            fg="white",

            font=FUENTE_BOTON,

            command=self.deshabilitar_usuario

        ).pack(

            side="left",

            padx=5

        )


        tk.Button(

            frame_superior,

            text="Cerrar",

            bg=COLOR_ROJO,

            fg="white",

            font=FUENTE_BOTON,

            command=self.destroy

        ).pack(

            side="left",

            padx=5

        )


        columnas = (

            "ID",

            "Nombre",

            "Email",

            "Rol",

            "Sucursal",

            "Activo"

        )


        self.tree = ttk.Treeview(

            self,

            columns=columnas,

            show="headings"

        )


        for col in columnas:

            self.tree.heading(

                col,

                text=col

            )

            self.tree.column(

                col,

                width=150

            )


        self.tree.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )
    
# ====================================
# DATOS
# ====================================

    def cargar_datos(self):

        for fila in self.tree.get_children():

            self.tree.delete(

                fila

            )


        datos = obtener_usuarios()


        for fila in datos:

            self.tree.insert(

                "",

                "end",

                values=fila

            )


    def habilitar_usuario(self):

        seleccionado = self.tree.focus()

        if not seleccionado:

            messagebox.showwarning("Atención", "Seleccione un usuario primero")

            return

        item = self.tree.item(seleccionado)

        usuario_id = item['values'][0]

        nombre = item['values'][1]


        activar_usuario(usuario_id)

        messagebox.showinfo("Éxito", f"Usuario {nombre} habilitado correctamente")

        self.cargar_datos()


    def deshabilitar_usuario(self):

        seleccionado = self.tree.focus()

        if not seleccionado:

            messagebox.showwarning("Atención", "Seleccione un usuario primero")

            return

        item = self.tree.item(seleccionado)

        usuario_id = item['values'][0]

        nombre = item['values'][1]


        if messagebox.askyesno("Confirmar", f"¿Está seguro de que desea deshabilitar al usuario {nombre}?"):

            desactivar_usuario(usuario_id)

            messagebox.showinfo("Éxito", f"Usuario {nombre} deshabilitado correctamente")

            self.cargar_datos()


    def abrir_nuevo_usuario(self):

        VentanaNuevoUsuario(self, self.cargar_datos)


class VentanaNuevoUsuario(tk.Toplevel):

    def __init__(self, master, al_guardar):

        super().__init__(master)

        self.title("Nuevo Usuario")

        self.geometry("450x550")

        self.configure(bg=COLOR_FONDO)

        self.al_guardar = al_guardar

        self.crear_widgets()


    def crear_widgets(self):

        tk.Label(

            self,

            text="NUEVO USUARIO",

            bg=COLOR_FONDO,

            fg=COLOR_AZUL,

            font=FUENTE_SUBTITULO

        ).pack(pady=15)


        frame = tk.Frame(self, bg=COLOR_FONDO)

        frame.pack(padx=20, pady=10, fill="both", expand=True)


        tk.Label(frame, text="Nombre:", bg=COLOR_FONDO, font=FUENTE_NORMAL).grid(row=0, column=0, sticky="w", pady=5)

        self.entry_nombre = ttk.Entry(frame, width=30)

        self.entry_nombre.grid(row=0, column=1, pady=5, padx=10)


        tk.Label(frame, text="Email:", bg=COLOR_FONDO, font=FUENTE_NORMAL).grid(row=1, column=0, sticky="w", pady=5)

        self.entry_email = ttk.Entry(frame, width=30)

        self.entry_email.grid(row=1, column=1, pady=5, padx=10)


        tk.Label(frame, text="Contraseña:", bg=COLOR_FONDO, font=FUENTE_NORMAL).grid(row=2, column=0, sticky="w", pady=5)

        self.entry_password = ttk.Entry(frame, width=30, show="*")

        self.entry_password.grid(row=2, column=1, pady=5, padx=10)


        tk.Label(frame, text="Rol:", bg=COLOR_FONDO, font=FUENTE_NORMAL).grid(row=3, column=0, sticky="w", pady=5)

        self.combo_rol = ttk.Combobox(frame, values=["ADMIN", "VENDEDOR"], state="readonly", width=28)

        self.combo_rol.set("VENDEDOR")

        self.combo_rol.grid(row=3, column=1, pady=5, padx=10)


        tk.Label(frame, text="Sucursal:", bg=COLOR_FONDO, font=FUENTE_NORMAL).grid(row=4, column=0, sticky="w", pady=5)


        from sucursales import obtener_sucursales

        self.sucursales_list = obtener_sucursales()

        nombres_sucursales = [s[1] for s in self.sucursales_list]


        self.combo_sucursal = ttk.Combobox(frame, values=nombres_sucursales, state="readonly", width=28)

        if nombres_sucursales:

            self.combo_sucursal.set(nombres_sucursales[0])

        self.combo_sucursal.grid(row=4, column=1, pady=5, padx=10)


        btn_frame = tk.Frame(self, bg=COLOR_FONDO)

        btn_frame.pack(pady=20)


        tk.Button(

            btn_frame,

            text="Guardar",

            bg=COLOR_VERDE,

            fg="white",

            font=FUENTE_BOTON,

            width=12,

            command=self.guardar

        ).pack(side="left", padx=10)


        tk.Button(

            btn_frame,

            text="Cancelar",

            bg=COLOR_ROJO,

            fg="white",

            font=FUENTE_BOTON,

            width=12,

            command=self.destroy

        ).pack(side="left", padx=10)


    def guardar(self):

        nombre = self.entry_nombre.get().strip()

        email = self.entry_email.get().strip()

        password = self.entry_password.get()

        rol = self.combo_rol.get()


        sucursal_nombre = self.combo_sucursal.get()

        sucursal_id = None

        for s in self.sucursales_list:

            if s[1] == sucursal_nombre:

                sucursal_id = s[0]

                break


        if not nombre or not email or not password:

            messagebox.showwarning("Error", "Todos los campos son obligatorios.")

            return


        from usuarios import crear_usuario

        exito = crear_usuario(nombre, email, password, rol, sucursal_id)

        if exito:

            messagebox.showinfo("Éxito", "Usuario creado correctamente.")

            self.al_guardar()

            self.destroy()

        else:

            messagebox.showerror("Error", "No se pudo crear el usuario. Verifique el email.")


if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    VentanaUsuarios(root)

    root.mainloop()