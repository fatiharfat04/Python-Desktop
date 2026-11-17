import tkinter as tk
from tkinter import ttk

class CustomStyleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Styling dengan ttk")
        self.root.geometry("700x500")
        self.root.configure(bg='#2c3e50')

        # Inisialisasi style
        self.style = ttk.Style()
        self._setup_custom_styles()
        self._buat_interface()

    def _setup_custom_styles(self):
        BG, FG, ACCENT = '#2c3e50', '#ecf0f1', '#3498db'

        # 1. Pakai tema yang menghormati properti warna
        self.style.theme_use('clam')

        # 2. Seragamkan semua container dan label
        self.style.configure('TFrame', background=BG)
        self.style.configure('TLabel', background=BG, foreground=FG)
        self.style.configure('TLabelframe', background=BG, bordercolor=ACCENT)
        self.style.configure('TLabelframe.Label', background=BG, foreground=FG)

        # 3. Tombol (hilangkan bevel dengan menyamakan light/darkcolor)
        self.style.configure('Custom.TButton',
                            background=ACCENT, foreground='white',
                            bordercolor=ACCENT, lightcolor=ACCENT, darkcolor=ACCENT,
                            focuscolor=ACCENT, borderwidth=0, padding=(20, 10))
        self.style.map('Custom.TButton',
                    background=[('pressed', '#21618c'), ('active', '#2980b9')],
                    bordercolor=[('pressed', '#21618c'), ('active', '#2980b9')],
                    lightcolor=[('pressed', '#21618c'), ('active', '#2980b9')],
                    darkcolor=[('pressed', '#21618c'), ('active', '#2980b9')])

        # 4. Entry (efek fokus lewat bordercolor, bukan focuscolor)
        self.style.configure('Custom.TEntry',
                            fieldbackground='#ecf0f1', foreground=BG,
                            insertcolor=BG, bordercolor='#bdc3c7',
                            lightcolor='#bdc3c7', borderwidth=2, padding=(10, 8))
        self.style.map('Custom.TEntry',
                    bordercolor=[('focus', ACCENT)],
                    lightcolor=[('focus', ACCENT)])

        # 5. Label khusus
        self.style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        self.style.configure('Subtitle.TLabel', foreground='#bdc3c7', font=('Arial', 12))

    def _buat_interface(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Header section
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0,30))

        ttk.Label(header_frame, text="Custom Styling Demo",
                 style='Title.TLabel').pack()
        ttk.Label(header_frame, text="Aplikasi dengan styling kustom menggunakan ttk.Style",
                 style='Subtitle.TLabel').pack(pady=(5,0))

        # Form section
        form_frame = ttk.LabelFrame(main_frame, text="Form Input", padding="20")
        form_frame.pack(fill='x', pady=(0,20))

        # Nama input
        ttk.Label(form_frame, text="Nama Lengkap:").pack(anchor='w', pady=(0,5))
        self.nama_entry = ttk.Entry(form_frame, style='Custom.TEntry', width=40)
        self.nama_entry.pack(fill='x', pady=(0,15))

        # Email input
        ttk.Label(form_frame, text="Email:").pack(anchor='w', pady=(0,5))
        self.email_entry = ttk.Entry(form_frame, style='Custom.TEntry', width=40)
        self.email_entry.pack(fill='x', pady=(0,15))

            # Button section
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill='x', pady=(10,0))

        ttk.Button(button_frame, text="Submit Data",
                  style='Custom.TButton', command=self.submit_data).pack(side='left', padx=(0,10))
        ttk.Button(button_frame, text="Reset Form",
                  style='Custom.TButton', command=self.reset_form).pack(side='left')

        # Result section
        self.result_frame = ttk.LabelFrame(main_frame, text="Hasil Input", padding="20")
        self.result_frame.pack(fill='both', expand=True)

        self.result_text = tk.Text(self.result_frame, height=8, bg='#ecf0f1',
                                  fg='#2c3e50', font=('Consolas', 10))
        self.result_text.pack(fill='both', expand=True)

    def submit_data(self):
        nama = self.nama_entry.get()
        email = self.email_entry.get()

        if nama and email:
            result = f"Data berhasil disubmit:\nNama: {nama}\nEmail: {email}\n" + "="*40 + "\n"
            self.result_text.insert('end', result)
            self.result_text.see('end')
        else:
            self.result_text.insert('end', "Error: Semua field harus diisi!\n" + "="*40 + "\n")

    def reset_form(self):
        self.nama_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.result_text.delete('1.0', 'end')

    def run(self):
        self.root.mainloop()

# Jalankan aplikasi
if __name__ == "__main__":
    app = CustomStyleApp()
    app.run()