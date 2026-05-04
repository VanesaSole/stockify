# main.py

import tkinter as tk
from ui import App


def main():
    root = tk.Tk()

    # opcional: mejorar apariencia inicial
    root.minsize(800, 600)

    app = App(root)

    root.mainloop()


if __name__ == "__main__":
    main()