import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import os
import re

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class AplikasiBiodata(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Biodata Mahasiswa")
        self.geometry("560x640")
        self.resizable(True, True)

        # File penyimpanan username terakhir (fitur Remember Me)
        self.file_username_terakhir = "username_terakhir.txt"

        # Database pengguna sederhana (username: password)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
        }

        # Warna background berdasarkan role user
        self.user_colors = {
            "admin": "#a3c4f3",       # biru
            "user1": "#a7f3d0",       # hijau
            "mahasiswa": "#fde68a",   # kuning
        }
        self.default_bg = self.cget("bg")

        self.current_user = None
        self.frame_aktif = None

        # Siapkan struktur tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Alur awal: kunci akses dan paksa ke halaman login
        self._pindah_ke(self.frame_login)

        # Log aplikasi start
        logging.info("Aplikasi dimulai")

    # ------------------ SISTEM FRAME & NAVIGASI ------------------
    def _pindah_ke(self, frame_tujuan):
        """Menyembunyikan frame sebelumnya dan menampilkan frame target."""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Fokus otomatis pada input pertama
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())

    def _buat_menu(self):
        """Menu bar hanya muncul saat user sudah berstatus login."""
        self.menu_bar = tk.Menu(master=self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar saat posisi logout / di halaman login."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _update_title(self):
        if self.current_user:
            self.title(f"Aplikasi Biodata Mahasiswa — Sesi: {self.current_user}")
        else:
            self.title("Login - Sistem Biodata Mahasiswa")

    def _set_bg_recursive(self, widget, color):
        """Set background color pada widget dan semua child-nya secara rekursif."""
        try:
            widget.configure(bg=color)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self._set_bg_recursive(child, color)

    def _apply_user_bg(self):
        """Terapkan warna background sesuai role user yang sedang login."""
        color = self.user_colors.get(self.current_user, self.default_bg)
        self._set_bg_recursive(self.frame_biodata, color)

    def _reset_user_bg(self):
        """Kembalikan background frame biodata ke default."""
        self._set_bg_recursive(self.frame_biodata, self.default_bg)

    # ------------------ HALAMAN 1: LOGIN (GERBANG AWAL) ------------------
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=30, pady=40)
        self.frame_login.grid_columnconfigure(0, weight=0)
        self.frame_login.grid_columnconfigure(1, weight=1)
        self.frame_login.grid_columnconfigure(2, weight=0)

        # Variabel kontrol halaman login
        self.var_ingat_username = tk.IntVar(value=0)

        # Judul Form Login
        tk.Label(
            self.frame_login,
            text="LOGIN SISTEM",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(0, 25))

        # Username Input
        tk.Label(self.frame_login, text="Username:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="W", pady=8
        )
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 11))
        self.entry_username.grid(row=1, column=1, columnspan=2, pady=8, sticky="EW")

        # Password Input
        tk.Label(self.frame_login, text="Password:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="W", pady=8
        )
        self.entry_password = tk.Entry(
            self.frame_login, font=("Arial", 11), show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=8, sticky="EW")

        # Tombol Show/Hide Password
        self.btn_lihat_password = tk.Button(
            self.frame_login,
            text="Tampilkan",
            font=("Arial", 9),
            relief=tk.GROOVE,
            cursor="hand2",
            command=self._toggle_lihat_password,
        )
        self.btn_lihat_password.grid(row=2, column=2, padx=(6, 0), pady=8, sticky="W")

        # Checkbox Remember Me (username terakhir)
        self.check_ingat_username = tk.Checkbutton(
            self.frame_login,
            text="Ingat username saya",
            variable=self.var_ingat_username,
            font=("Arial", 10),
            anchor="w",
            command=self._ubah_ingat_username,
        )
        self.check_ingat_username.grid(row=3, column=1, columnspan=2, sticky="W", pady=(2, 0))

        # Tombol Aksi Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Masuk",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            command=self._coba_login,
        )
        self.btn_login.grid(row=4, column=0, columnspan=3, pady=20, sticky="EW")

        # Shortcut Enter pada login
        self.entry_username.bind(
            "<Return>", lambda e: self.entry_password.focus_set()
        )
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Petunjuk Akun Uji Coba
        info_label = tk.Label(
            self.frame_login,
            text="Akun tersedia:\n• admin (password: 123)\n• user1 (password: password1)\n• mahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="#64748b",
            justify=tk.LEFT,
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=10, sticky="W")

        # Muat username terakhir yang disimpan oleh fitur Remember Me
        username_terakhir = self._baca_username_ingat()
        if username_terakhir:
            self.entry_username.insert(0, username_terakhir)
            self.var_ingat_username.set(1)

    # ------------------ FITUR LOGIN TAMBAHAN ------------------
    def _set_lihat_password(self, tampil):
        """Tampilkan atau sembunyikan isi field password."""
        if tampil:
            self.entry_password.config(show="")
            self.btn_lihat_password.config(text="Sembunyikan")
        else:
            self.entry_password.config(show="*")
            self.btn_lihat_password.config(text="Tampilkan")

    def _toggle_lihat_password(self):
        """Tombol Show/Hide Password: ganti status tampil/sembunyi."""
        sedang_tampil = self.entry_password.cget("show") == ""
        self._set_lihat_password(not sedang_tampil)
        logging.info("Password ditampilkan" if not sedang_tampil else "Password disembunyikan")

    def _ubah_ingat_username(self):
        """Callback checkbox Remember Me: simpan atau hapus username terakhir."""
        if self.var_ingat_username.get() == 1:
            username = self.entry_username.get().strip()
            if username:
                self._simpan_username_ingat(username)
                logging.info(f"Remember Me aktif untuk username: {username}")
        else:
            self._lupakan_username_ingat()
            logging.info("Remember Me dinonaktifkan")

    def _simpan_username_ingat(self, username):
        """Simpan username terakhir ke file agar bisa diingat aplikasi."""
        try:
            with open(self.file_username_terakhir, "w", encoding="utf-8") as file:
                file.write(username)
        except OSError as e:
            logging.error(f"Gagal menyimpan username (Remember Me): {e}")

    def _baca_username_ingat(self):
        """Baca username terakhir dari file. Kembalikan string kosong bila tidak ada."""
        try:
            if os.path.exists(self.file_username_terakhir):
                with open(self.file_username_terakhir, "r", encoding="utf-8") as file:
                    return file.read().strip()
        except OSError as e:
            logging.error(f"Gagal membaca username (Remember Me): {e}")
        return ""

    def _lupakan_username_ingat(self):
        """Hapus username terakhir dari file."""
        try:
            if os.path.exists(self.file_username_terakhir):
                os.remove(self.file_username_terakhir)
        except OSError as e:
            logging.error(f"Gagal menghapus username (Remember Me): {e}")

    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(f"Empty credentials attempt for username: {username}")
            messagebox.showwarning("Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning("Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")

            # Fitur Remember Me: simpan atau lupakan username terakhir
            if self.var_ingat_username.get() == 1:
                self._simpan_username_ingat(username)
            else:
                self._lupakan_username_ingat()

            messagebox.showinfo("Login Berhasil", f"Selamat Datang, {username}!")

            # Pasang menu dan alihkan ke dashboard form biodata
            self._buat_menu()
            self._reset_form_biodata()
            self._apply_user_bg()
            self._update_title()
            self._pindah_ke(self.frame_biodata)

            # Bersihkan field input login (password selalu disembunyikan lagi)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._set_lihat_password(False)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror("Login Gagal", "Username atau password yang dimasukkan salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title()
            # Hapus menu (hanya tersedia saat user login)
            self._hapus_menu()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._set_lihat_password(False)
            # Remember Me: kembalikan username terakhir bila dicentang
            if self.var_ingat_username.get() == 1:
                username_terakhir = self._baca_username_ingat()
                if username_terakhir:
                    self.entry_username.insert(0, username_terakhir)
            # Reset form biodata
            self._reset_form_biodata()
            self._reset_user_bg()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    # ------------------ HALAMAN 2: FORM BIODATA (SETELAH LOGIN) ------------------
    def _buat_tampilan_biodata(self):
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=10)

        # Variabel kontrol data
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl_lahir = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar(value=0)

        # Tracing untuk validasi tombol submit secara real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self._validate_nim_visual)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self._validate_email_visual)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self._validate_telepon_visual)
        self.var_tgl_lahir.trace_add("write", self.validate_form)
        self.var_tgl_lahir.trace_add("write", self._validate_tgl_lahir_visual)
        self.var_setuju.trace_add("write", self.validate_form)

        # Header Form
        label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 15, "bold"),
        )
        label_judul.pack(pady=10)

        # Container Input
        frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=15,
            pady=12,
        )
        frame_input.pack(fill=tk.X, expand=False)
        frame_input.columnconfigure(1, weight=1)

        # Nama
        tk.Label(frame_input, text="Nama Lengkap:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="W", pady=5
        )
        self.entry_nama = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, sticky="EW", pady=5)

        # NIM
        tk.Label(frame_input, text="NIM:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="W", pady=5
        )
        self.entry_nim = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, sticky="EW", pady=5)

        # Jurusan
        tk.Label(frame_input, text="Jurusan:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="W", pady=5
        )
        self.entry_jurusan = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, sticky="EW", pady=5)

        # Email (validasi format)
        tk.Label(frame_input, text="Email:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="W", pady=5
        )
        self.entry_email = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_email
        )
        self.entry_email.grid(row=3, column=1, sticky="EW", pady=5)

        # Telepon (validasi format Indonesia)
        tk.Label(frame_input, text="Telepon:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="W", pady=5
        )
        self.entry_telepon = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_telepon
        )
        self.entry_telepon.grid(row=4, column=1, sticky="EW", pady=5)

        # Tanggal Lahir (format DD/MM/YYYY)
        tk.Label(
            frame_input,
            text="Tanggal Lahir:\n(DD/MM/YYYY)",
            font=("Arial", 10),
            justify=tk.LEFT,
        ).grid(row=5, column=0, sticky="W", pady=5)
        self.entry_tgl_lahir = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_tgl_lahir
        )
        self.entry_tgl_lahir.grid(row=5, column=1, sticky="EW", pady=5)

        # Alamat (Text Area + Scrollbar)
        tk.Label(frame_input, text="Alamat:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="NW", pady=5
        )
        frame_alamat = tk.Frame(frame_input, relief=tk.SUNKEN, borderwidth=1)
        frame_alamat.grid(row=6, column=1, sticky="EW", pady=5)

        scrollbar_alamat = tk.Scrollbar(frame_alamat)
        scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(
            frame_alamat,
            height=4,
            font=("Arial", 10),
            yscrollcommand=scrollbar_alamat.set,
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_alamat.config(command=self.text_alamat.yview)

        # Jenis Kelamin
        tk.Label(frame_input, text="Jenis Kelamin:", font=("Arial", 10)).grid(
            row=7, column=0, sticky="W", pady=5
        )
        frame_jk = tk.Frame(frame_input)
        frame_jk.grid(row=7, column=1, sticky="W", pady=5)

        tk.Radiobutton(
            frame_jk, text="Pria", variable=self.var_jk, value="Pria"
        ).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(
            frame_jk, text="Wanita", variable=self.var_jk, value="Wanita"
        ).pack(side=tk.LEFT)

        # Checkbox Persetujuan
        check_setuju = tk.Checkbutton(
            frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 9),
            command=self.validate_form,
        )
        check_setuju.grid(row=8, column=0, columnspan=2, sticky="W", pady=10)

        # Tombol Aksi (Submit status awal: DISABLED + Reset Form)
        frame_aksi = tk.Frame(master=self.frame_biodata)
        frame_aksi.pack(fill=tk.X, pady=10)
        frame_aksi.columnconfigure(0, weight=1)
        frame_aksi.columnconfigure(1, weight=1)

        self.btn_submit = tk.Button(
            frame_aksi,
            text="Simpan Data Biodata",
            font=("Arial", 11, "bold"),
            command=self.submit_data,
            state=tk.DISABLED,
        )
        self.btn_submit.grid(row=0, column=0, sticky="EW", padx=(0, 5))

        # Tombol Reset Form (Tugas 2)
        self.btn_reset = tk.Button(
            frame_aksi,
            text="Reset Form",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            cursor="hand2",
            command=self.reset_form,
        )
        self.btn_reset.grid(row=0, column=1, sticky="EW", padx=(5, 0))

        # Shortcut Enter pada entry
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)

        # Preview Data Tersimpan
        self.label_hasil = tk.Label(
            self.frame_biodata,
            text="",
            font=("Arial", 10),
            justify=tk.LEFT,
            fg="#1e293b",
        )
        self.label_hasil.pack(anchor="w", padx=5, pady=5)

    # ------------------ LOGIKA VALIDASI & AKSI BIODATA ------------------
    def _get_current_bg(self):
        """Ambil warna background sesuai role user yang login, atau default."""
        if self.current_user:
            return self.user_colors.get(self.current_user, self.default_bg)
        return self.default_bg

    def _validate_nim_visual(self, *args):
        """Feedback visual: bg merah jika NIM diisi tapi kurang dari 8 karakter."""
        nim = self.var_nim.get().strip()
        if nim and (len(nim) < 8 or not nim.isdigit()):
            self.entry_nim.config(bg="#fca5a5")
        else:
            self.entry_nim.config(bg=self._get_current_bg())

    # ------------------ VALIDASI LANJUTAN (TUGAS 3) ------------------
    def _set_bg_entry(self, entry, terisi, valid):
        """Feedback visual: bg merah jika terisi namun formatnya tidak valid."""
        if terisi and not valid:
            entry.config(bg="#fca5a5")
        else:
            entry.config(bg=self._get_current_bg())

    def _is_email_valid(self, email):
        """Cek format email: nama@domain.com"""
        email = email.strip()
        return bool(
            re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", email)
        )

    def _is_telepon_valid(self, telepon):
        """Cek format nomor telepon Indonesia: 08xx / 02xx / +62 / 62."""
        bersih = re.sub(r"[\s\-\(\)\.]", "", telepon.strip())
        if not re.fullmatch(r"\+?[0-9]{9,15}", bersih):
            return False

        # Normalisasi ke format lokal (diawali 0)
        if bersih.startswith("+62"):
            lokal = "0" + bersih[3:]
        elif bersih.startswith("62"):
            lokal = "0" + bersih[2:]
        else:
            lokal = bersih

        # Wajib nomor Indonesia: 08 (seluler) atau 02-07 (darat), panjang 10-15 digit
        if not re.match(r"^0(8\d|[2-7]\d)", lokal):
            return False
        return 10 <= len(lokal) <= 15

    def _parse_tgl_lahir(self, teks):
        """Ubah teks tanggal lahir menjadi objek date. None jika format tidak valid."""
        teks = teks.strip()
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.datetime.strptime(teks, fmt).date()
            except ValueError:
                continue
        return None

    def _is_tgl_lahir_valid(self, teks):
        """Validasi tanggal lahir: format benar, bukan tanggal masa depan, bukan > 100 tahun lalu."""
        tanggal = self._parse_tgl_lahir(teks)
        if tanggal is None:
            return False
        hari_ini = datetime.date.today()
        if tanggal > hari_ini:
            return False
        # Usia maksimal 100 tahun
        if tanggal < hari_ini - datetime.timedelta(days=365 * 100):
            return False
        return True

    def _validate_email_visual(self, *args):
        email = self.var_email.get().strip()
        self._set_bg_entry(self.entry_email, email != "", self._is_email_valid(email))

    def _validate_telepon_visual(self, *args):
        telepon = self.var_telepon.get().strip()
        self._set_bg_entry(
            self.entry_telepon, telepon != "", self._is_telepon_valid(telepon)
        )

    def _validate_tgl_lahir_visual(self, *args):
        tgl = self.var_tgl_lahir.get().strip()
        self._set_bg_entry(
            self.entry_tgl_lahir, tgl != "", self._is_tgl_lahir_valid(tgl)
        )

    def validate_form(self, *args):
        """Tombol submit hanya aktif jika semua field terisi dan formatnya valid."""
        nama_ada = self.var_nama.get().strip() != ""
        nim_ada = self.var_nim.get().strip() != ""
        jurusan_ada = self.var_jurusan.get().strip() != ""
        setuju = self.var_setuju.get() == 1

        email = self.var_email.get().strip()
        telepon = self.var_telepon.get().strip()
        tgl_lahir = self.var_tgl_lahir.get().strip()

        email_valid = self._is_email_valid(email)
        telepon_valid = self._is_telepon_valid(telepon)
        tgl_lahir_valid = self._is_tgl_lahir_valid(tgl_lahir)

        if (
            nama_ada
            and nim_ada
            and jurusan_ada
            and setuju
            and email_valid
            and telepon_valid
            and tgl_lahir_valid
        ):
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def submit_shortcut(self, event=None):
        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tgl_lahir = self.var_tgl_lahir.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning("Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            if not email or not telepon or not tgl_lahir:
                messagebox.showwarning(
                    "Input Kosong",
                    "Email, Telepon, dan Tanggal Lahir harus diisi!",
                )
                return

            # Validasi format email
            if not self._is_email_valid(email):
                self._validate_email_visual()
                messagebox.showwarning(
                    "Format Email Salah",
                    "Email tidak valid!\nContoh format yang benar: nama@domain.com",
                )
                self.entry_email.focus_set()
                return

            # Validasi format telepon Indonesia
            if not self._is_telepon_valid(telepon):
                self._validate_telepon_visual()
                messagebox.showwarning(
                    "Format Telepon Salah",
                    "Nomor telepon tidak valid!\nGunakan format Indonesia, contoh: 081234567890 atau +6281234567890",
                )
                self.entry_telepon.focus_set()
                return

            # Validasi tanggal lahir
            tanggal_obj = self._parse_tgl_lahir(tgl_lahir)
            if tanggal_obj is None:
                self._validate_tgl_lahir_visual()
                messagebox.showwarning(
                    "Format Tanggal Lahir Salah",
                    "Tanggal lahir tidak valid!\nGunakan format DD/MM/YYYY, contoh: 17/08/2005",
                )
                self.entry_tgl_lahir.focus_set()
                return

            if tanggal_obj > datetime.date.today():
                self._validate_tgl_lahir_visual()
                messagebox.showwarning(
                    "Tanggal Lahir Tidak Valid",
                    "Tanggal lahir tidak boleh di masa depan!",
                )
                self.entry_tgl_lahir.focus_set()
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                self.entry_nim.config(bg="#fca5a5")
                messagebox.showwarning("Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning("Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.focus_set()
                return

            # Tampilkan hasil
            hasil = (
                f"Nama: {nama}\n"
                f"NIM: {nim}\n"
                f"Jurusan: {jurusan}\n"
                f"Email: {email}\n"
                f"Telepon: {telepon}\n"
                f"Tanggal Lahir: {tanggal_obj.strftime('%d/%m/%Y')}\n"
                f"Alamat: {alamat}\n"
                f"Jenis Kelamin: {jenis_kelamin}"
            )
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            # Log successful data submission
            logging.info(f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            # Log error submission
            logging.error(f"Error in submit_data by {self.current_user}: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

    def _reset_form_biodata(self):
        """Mengosongkan isian formulir."""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl_lahir.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.btn_submit.config(state=tk.DISABLED)
        self.entry_nim.config(bg=self._get_current_bg())
        self.entry_email.config(bg=self._get_current_bg())
        self.entry_telepon.config(bg=self._get_current_bg())
        self.entry_tgl_lahir.config(bg=self._get_current_bg())

    def _form_ada_isian(self):
        """Cek apakah masih ada isian pada form biodata."""
        if (
            self.var_nama.get().strip()
            or self.var_nim.get().strip()
            or self.var_jurusan.get().strip()
            or self.var_email.get().strip()
            or self.var_telepon.get().strip()
            or self.var_tgl_lahir.get().strip()
            or self.text_alamat.get("1.0", tk.END).strip()
            or self.var_setuju.get() == 1
            or self.var_jk.get() != "Pria"
        ):
            return True
        return False

    def reset_form(self):
        """Tombol Reset Form (Tugas 2): kosongkan seluruh field biodata."""
        if self._form_ada_isian():
            if not messagebox.askyesno(
                "Reset Form",
                "Yakin ingin mereset semua field biodata?",
            ):
                return

        self._reset_form_biodata()
        logging.info(f"Form biodata direset oleh user: {self.current_user}")
        self.entry_nama.focus_set()

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo("Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror("Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    # def _buat_menu(self):
    #     """Membuat menu bar untuk aplikasi"""
    #     menu_bar = tk.Menu(master=self)
    #     self.config(menu=menu_bar)

    #     file_menu = tk.Menu(master=menu_bar, tearoff=0)
    #     file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
    #     file_menu.add_separator()
    #     file_menu.add_command(label="Logout", command=self._logout)
    #     file_menu.add_separator()
    #     file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

    #     menu_bar.add_cascade(label="File", menu=file_menu)

if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()