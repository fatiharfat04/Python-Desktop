import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import shutil

class FileExplorer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("File Explorer - File Management Demo")
        self.window.geometry("800x600")
        self.window.configure(bg="lightsteelblue")

        # variable untuk menyimpan informasi file
        self.current_file = None
        self.current_directory = os.getcwd()
        self.selected_files = []

        self.buat_interface()

    def buat_interface(self):
        header_frame = tk.Frame(self.window, bg="darkblue", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="FILE EXPLORER",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="darkblue"
        ).pack(pady=15)

        # Frame untuk path dan navigasi
        nav_frame = tk.Frame(self.window, bg="lightgray", height=40)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Label(
            nav_frame,
            text="Current Directory:",
            font=("Arial", 10, "bold"),
            bg="lightgray"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        self.path_label = tk.Label(
            nav_frame,
            text=self.current_directory,
            font=("Arial", 10),
            bg="lightgray",
            fg="blue",
            anchor="w"
        )
        self.path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)

    def jalankan(self):
        """Method untuk jalankan aplikasi"""
        self.window.mainloop()

# untuk menjalankan aplikasi
if __name__ == "__main__":
    app = FileExplorer()
    app.jalankan()