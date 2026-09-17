import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi dengan Navbar")
        self.root.geometry("600x400")

        self.create_navbar()

    def create_navbar(self):
        # Membuat menubar utama
        menubar = tk.Menu(self.root)

        # 1. Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.dummy_action)
        file_menu.add_command(label="Open", command=self.dummy_action)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # 2. Menu Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.dummy_action)
        edit_menu.add_command(label="Copy", command=self.dummy_action)
        edit_menu.add_command(label="Paste", command=self.dummy_action)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # 3. Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Memasang menubar ke dalam window root
        self.root.config(menu=menubar)

    def dummy_action(self):
        print("Menu item diklik!")

    def show_about(self):
        messagebox.showinfo("About", "Ini adalah contoh aplikasi dengan Navbar menggunakan Tkinter.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()