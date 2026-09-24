import tkinter as tk
from tkinter import messagebox

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):
    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

    def _buat_tampilan_biodata(self):
        # --- Variabel Kontrol Tkinter ---
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)

        # --- Frame Biodata ---
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=20)
        self.frame_biodata.columnconfigure(1, weight=1)

        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata, 
            text="FORM BIODATA MAHASISWA", 
            font=("Arial", 16, "bold")
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)   

        # Input Nama
        tk.Label(self.frame_biodata, text="Nama:", font=("Arial", 11)).grid(row=1, column=0, sticky="W", pady=5)
        self.entry_nama = tk.Entry(self.frame_biodata, textvariable=self.var_nama, font=("Arial", 11))
        self.entry_nama.grid(row=1, column=1, sticky="EW", pady=5)

        # Input NIM
        tk.Label(self.frame_biodata, text="NIM:", font=("Arial", 11)).grid(row=2, column=0, sticky="W", pady=5)
        self.entry_nim = tk.Entry(self.frame_biodata, textvariable=self.var_nim, font=("Arial", 11))
        self.entry_nim.grid(row=2, column=1, sticky="EW", pady=5)

        # Input Jurusan
        tk.Label(self.frame_biodata, text="Jurusan:", font=("Arial", 11)).grid(row=3, column=0, sticky="W", pady=5)
        self.entry_jurusan = tk.Entry(self.frame_biodata, textvariable=self.var_jurusan, font=("Arial", 11))
        self.entry_jurusan.grid(row=3, column=1, sticky="EW", pady=5)

        # Input Jenis Kelamin
        tk.Label(self.frame_biodata, text="Jenis Kelamin:", font=("Arial", 11)).grid(row=4, column=0, sticky="W", pady=5)
        frame_jk = tk.Frame(self.frame_biodata)
        frame_jk.grid(row=4, column=1, sticky="W", pady=5)
        tk.Radiobutton(frame_jk, text="Pria", variable=self.var_jk, value="Pria").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(frame_jk, text="Wanita", variable=self.var_jk, value="Wanita").pack(side=tk.LEFT, padx=5)

        # Input Alamat
        tk.Label(self.frame_biodata, text="Alamat:", font=("Arial", 11)).grid(row=5, column=0, sticky="NW", pady=5)
        self.text_alamat = tk.Text(self.frame_biodata, width=30, height=4, font=("Arial", 11))
        self.text_alamat.grid(row=5, column=1, sticky="EW", pady=5)

        # Checkbox Persetujuan
        self.check_setuju = tk.Checkbutton(
            self.frame_biodata, 
            text="Saya menyatakan data yang diisi sudah benar", 
            variable=self.var_setuju,
            command=self.validate_form
        )
        self.check_setuju.grid(row=6, column=0, columnspan=2, sticky="W", pady=10)

        # Tombol Submit
        self.btn_submit = tk.Button(
            self.frame_biodata, 
            text="Submit", 
            font=("Arial", 11, "bold"),
            state=tk.DISABLED,
            command=self.submit_data
        )
        self.btn_submit.grid(row=7, column=0, columnspan=2, sticky="EW", pady=10)

        # Bindings untuk Tombol Submit
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)
        self.bind("<Return>", self.submit_shortcut)

        # Tombol Logout
        self.btn_logout = tk.Button(
            self.frame_biodata, 
            text="Logout", 
            font=("Arial", 11),
            command=self._logout
        )
        self.btn_logout.grid(row=8, column=0, columnspan=2, sticky="EW", pady=5)

        # Label Hasil
        self.label_hasil = tk.Label(self.frame_biodata, text="", font=("Arial", 11), justify=tk.LEFT)
        self.label_hasil.grid(row=9, column=0, columnspan=2, pady=10, sticky="W")


    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Judul Login
        tk.Label(
            self.frame_login, 
            text="HALAMAN LOGIN", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Input Username
        tk.Label(
            self.frame_login, 
            text="Username:", 
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)

        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        # Input Password
        tk.Label(
            self.frame_login, 
            text="Password:", 
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="W", pady=5)

        self.entry_password = tk.Entry(
            self.frame_login, 
            font=("Arial", 12), 
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login, 
            text="Login", 
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="EW")

        # Keyboard shortcuts untuk login
        self.entry_username.bind("<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=4, column=0, columnspan=2, pady=10)

    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())


    def submit_data(self):
        # Cek checkbox
        if self.var_setuju.get() == 0:
            messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
            return

        # Ambil data dari form
        nama = self.entry_nama.get()
        nim = self.entry_nim.get()  
        jurusan = self.entry_jurusan.get()
        alamat = self.text_alamat.get("1.0", tk.END).strip()
        jenis_kelamin = self.var_jk.get()

        # Cek field kosong
        if not nama or not nim or not jurusan:
            messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
            return

        # Tampilkan hasil
        hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nJenis Kelamin: {jenis_kelamin}"
        messagebox.showinfo("Data Tersimpan", hasil)

        # Tampilkan hasil di label
        self.label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if nama_valid and nim_valid and jurusan_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    ### TAMBAHAN DARI MODUL - NANTI BAKAL DIHAPUS ###
    def _coba_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Definisi user yang valid (bisa dikembangkan jadi class/DB)
        user_valid = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        if user_valid.get(username) == password:
            messagebox.showinfo("Login Sukses", f"Selamat datang {username}!")
            self._pindah_ke(self.frame_biodata)
            self.entry_password.delete(0, tk.END)  # kosongkan password
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah")
            self.entry_password.delete(0, tk.END)

    def _logout(self):
        """Logout dan kembali ke layar login"""
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?"):
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._pindah_ke(self.frame_login)
    ### TAMBAHAN DARI MODUL - NANTI BAKAL DIHAPUS ###

# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()
    # Menjalankan mainloop dari instance tersebut
    app.mainloop()