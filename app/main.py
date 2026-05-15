# main.py

import tkinter as tk

from database import crear_tablas

from login_ui import LoginUI


def main():

    crear_tablas()

    root = tk.Tk()

    LoginUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()