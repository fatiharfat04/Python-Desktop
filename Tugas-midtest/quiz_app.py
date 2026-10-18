"""
Quiz Interaktif - Tugas Akhir Mata Kuliah Pemrograman GUI
==========================================================
Aplikasi kuis pilihan ganda berbasis Tkinter dengan:
  - Timer countdown per soal (after(), tanpa sleep)
  - Animasi feedback benar/salah
  - Tracking skor & progres real-time
  - Ringkasan hasil akhir + restart

Cara menjalankan:  python quiz_app.py
"""

import random
import tkinter as tk
from tkinter import messagebox, ttk

# ============================================================================
# KONSTANTA (menggantikan "magic numbers")
# ============================================================================
WAKTU_PER_SOAL: int = 30          # detik countdown tiap soal
SKOR_PER_BENAR: int = 10          # poin tiap jawaban benar
AMBANG_ORANYE: int = 15           # sisa detik di bawah ini -> warna oranye
AMBANG_MERAH: int = 5             # sisa detik di bawah ini -> warna merah
INTERVAL_TICK: int = 1000         # interval timer (ms)
INTERVAL_FLASH: int = 200         # kecepatan kedipan animasi (ms)
JUMLAH_KEDIPAN: int = 3           # berapa kali frame berkedip

# Palet warna
WARNA_NETRAL: str = "#ecf0f1"
WARNA_BENAR: str = "#27ae60"
WARNA_SALAH: str = "#c0392b"
WARNA_TIMER_NORMAL: str = "#2ecc71"
WARNA_TIMER_ORANYE: str = "#e67e22"
WARNA_TIMER_MERAH: str = "#e74c3c"


class QuizApp:
    """Aplikasi quiz interaktif berbasis Tkinter."""

    def __init__(self) -> None:
        """Inisialisasi window, data soal, state, lalu membangun UI."""
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("700x500")
        self.window.minsize(640, 460)
        # Tutup window harus melewati handler (bisa muncul konfirmasi)
        self.window.protocol("WM_DELETE_WINDOW", self.keluar_aplikasi)

        # ----- Bank soal (10 soal event-driven programming & Tkinter) -----
        self.bank_soal: list[dict] = [
            {
                "question": "Apa itu event-driven programming?",
                "options": [
                    "Program yang berjalan berurutan dari atas ke bawah",
                    "Program yang merespons kejadian (event)",
                    "Program tanpa antarmuka grafis",
                    "Program yang hanya berbasis web",
                ],
                "correct": 1,
            },
            {
                "question": "Method apa yang memulai siklus event loop pada Tkinter?",
                "options": ["update()", "mainloop()", "start()", "run()"],
                "correct": 1,
            },
            {
                "question": "Fungsi widget.bind() digunakan untuk apa?",
                "options": [
                    "Mengikat sebuah event ke fungsi callback/event handler",
                    "Mengikat dua widget agar posisinya sama",
                    "Menyimpan data ke dalam variabel",
                    "Mengubah warna latar belakang widget",
                ],
                "correct": 0,
            },
            {
                "question": "Variabel Tkinter (tk.IntVar, tk.StringVar) bermanfaat agar...",
                "options": [
                    "Widget bisa dibuat lebih cepat",
                    "Nilainya otomatis tersinkron dengan widget yang terkait",
                    "Program tidak perlu mainloop",
                    "Tidak perlu lagi menulis callback",
                ],
                "correct": 1,
            },
            {
                "question": "Apa fungsi method window.after(delay, callback)?",
                "options": [
                    "Menjalankan callback secara blocking/sinkron",
                    "Menjadwalkan callback setelah delay milidetik tanpa membekukan GUI",
                    "Mengulang callback selamanya tanpa henti",
                    "Menutup window setelah delay tertentu",
                ],
                "correct": 1,
            },
            {
                "question": "Kenapa time.sleep() tidak boleh dipakai di GUI?",
                "options": [
                    "Karena sleep() hanya bekerja di Python 2",
                    "Karena sleep() memblokir event loop sehingga GUI menjadi tidak responsif",
                    "Karena sleep() menyebabkan memory leak",
                    "Karena sleep() tidak tersedia di modul tkinter",
                ],
                "correct": 1,
            },
            {
                "question": "Apa perbedaan utama antara widget Button(command=...) dan widget.bind('<Button-1>', ...)?",
                "options": [
                    "Tidak ada perbedaan, keduanya sama persis",
                    "command hanya untuk Button, sedangkan bind bisa dipakai pada banyak widget dan event berbeda",
                    "bind hanya bisa dipakai pada window utama",
                    "command berjalan lebih cepat daripada bind",
                ],
                "correct": 1,
            },
            {
                "question": "Apa isi atribut event.keysym saat menangani event keyboard?",
                "options": [
                    "Kode numerik dari tombol keyboard",
                    "Nama simbolis tombol yang ditekan (mis. 'Return', 'Escape', 'a')",
                    "Nilai dari widget Entry terkait",
                    "Waktu saat tombol ditekan",
                ],
                "correct": 1,
            },
            {
                "question": "Widget container biasa digunakan untuk apa?",
                "options": [
                    "Menyimpan file sementara",
                    "Mengelompokkan dan menata (layout) widget lain di dalamnya",
                    "Menggantikan fungsi event loop",
                    "Mengubah tema operasi sistem",
                ],
                "correct": 1,
            },
            {
                "question": "Apa fungsi method after_cancel(id)?",
                "options": [
                    "Menjalankan ulang callback dengan ID tersebut",
                    "Membatalkan callback yang dijadwalkan dengan ID tersebut",
                    "Menghapus widget dengan ID tersebut",
                    "Menghentikan seluruh program",
                ],
                "correct": 1,
            },
        ]

        # ----- State management (satu struktur rapi) -----
        self.state: dict = {
            "current_question": 0,
            "score": 0,
            "time_left": WAKTU_PER_SOAL,
            "answers": [],       # riwayat jawaban per soal
            "status": "belum",   # belum | bermain | selesai
            "locked": False,     # kunci input saat animasi (cegah double submit)
        }
        # Variabel Tkinter: -1 = belum ada opsi terpilih
        self.selected_answer = tk.IntVar(value=-1)

        # Penanda ID callback after() agar bisa dibatalkan (anti timer ganda)
        self._id_timer: str | None = None
        self._id_animasi: str | None = None

        # Daftar soal sesi berjalan (hasil acak)
        self.soal_aktif: list[dict] = []

        # Referensi widget yang butuh "kunci/buka kunci"
        self._radio_buttons: list[tk.Radiobutton] = []

        self.buat_interface()
        self.mulai_quiz()

    # ======================================================================
    # UI
    # ======================================================================
    def buat_interface(self) -> None:
        """Membangun seluruh widget: layar soal dan layar hasil (frame bertumpuk)."""
        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure(" hijau.Horizontal.TProgressbar",
                        troughcolor="#bdc3c7", background=WARNA_BENAR)

        # --- Header: judul + info soal/skor + progress bar ---
        header = tk.Frame(self.window, bg="#34495e", pady=8, padx=12)
        header.pack(fill="x")

        tk.Label(
            header, text="QUIZ INTERAKTIF", font=("Segoe UI", 16, "bold"),
            bg="#34495e", fg="white",
        ).pack(anchor="w")

        baris_info = tk.Frame(header, bg="#34495e")
        baris_info.pack(fill="x", pady=(4, 0))

        self.label_soal = tk.Label(
            baris_info, text="Soal 1/10", font=("Segoe UI", 11, "bold"),
            bg="#34495e", fg="white",
        )
        self.label_soal.pack(side="left")

        self.label_skor = tk.Label(
            baris_info, text="Skor: 0", font=("Segoe UI", 11, "bold"),
            bg="#34495e", fg="white",
        )
        self.label_skor.pack(side="right")

        # Progress bar progres soal
        self.progress = ttk.Progressbar(
            baris_info, orient="horizontal", length=220,
            mode="determinate", style=" hijau.Horizontal.TProgressbar",
        )
        self.progress.pack(side="right", padx=14)

        # --- Layar Soal ---
        self.frame_soal = tk.Frame(self.window, bg=WARNA_NETRAL, padx=24, pady=16)
        self.frame_soal.pack(fill="both", expand=True)

        # Timer countdown (label besar di kanan atas layar soal)
        self.label_timer = tk.Label(
            self.frame_soal, text=f"{WAKTU_PER_SOAL}s",
            font=("Segoe UI", 20, "bold"), fg=WARNA_TIMER_NORMAL, bg=WARNA_NETRAL,
        )
        self.label_timer.pack(anchor="e")

        # Label teks soal
        self.label_pertanyaan = tk.Label(
            self.frame_soal, text="", font=("Segoe UI", 13),
            wraplength=620, justify="left", anchor="w",
            bg=WARNA_NETRAL, fg="#2c3e50", pady=10,
        )
        self.label_pertanyaan.pack(fill="x")

        # Wadah opsi jawaban (Radiobutton dibuat sekali, teks diganti tiap soal)
        self.frame_opsi = tk.Frame(self.frame_soal, bg=WARNA_NETRAL)
        self.frame_opsi.pack(fill="x", pady=6)
        self._radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(
                self.frame_opsi, text="", variable=self.selected_answer,
                value=i, font=("Segoe UI", 11), anchor="w",
                bg=WARNA_NETRAL, fg="#2c3e50", selectcolor="white",
                activebackground=WARNA_NETRAL, activeforeground="#2c3e50",
                indicatoron=True, pady=4, wraplength=600, justify="left",
            )
            rb.pack(fill="x", pady=2, anchor="w")
            self._radio_buttons.append(rb)

        # Tombol aksi + petunjuk keyboard
        baris_aksi = tk.Frame(self.frame_soal, bg=WARNA_NETRAL)
        baris_aksi.pack(fill="x", pady=(10, 0))

        self.btn_submit = tk.Button(
            baris_aksi, text="Submit Jawaban (Enter)", font=("Segoe UI", 11, "bold"),
            bg=WARNA_BENAR, fg="white", activebackground="#219a52",
            activeforeground="white", relief="flat", padx=12, pady=6,
            command=self.submit_answer,
        )
        self.btn_submit.pack(side="left")

        self.btn_skip = tk.Button(
            baris_aksi, text="Lewati (Esc)", font=("Segoe UI", 11),
            bg="#7f8c8d", fg="white", activebackground="#6f7c7d",
            activeforeground="white", relief="flat", padx=12, pady=6,
            command=self.lewati_soal,
        )
        self.btn_skip.pack(side="left", padx=10)

        tk.Label(
            baris_aksi,
            text="Shortcut: [1-4] pilih opsi  •  [Enter] submit  •  [Esc] lewati",
            font=("Segoe UI", 9), bg=WARNA_NETRAL, fg="#7f8c8d",
        ).pack(side="right")

        # --- Layar Hasil (tersembunyi di awal, di-`pack` saat show_result) ---
        self.frame_hasil = tk.Frame(self.window, bg=WARNA_NETRAL, padx=24, pady=20)

        tk.Label(
            self.frame_hasil, text="HASIL QUIZ", font=("Segoe UI", 20, "bold"),
            bg=WARNA_NETRAL, fg="#2c3e50",
        ).pack(pady=(6, 14))

        self.var_hasil = tk.StringVar(value="")
        tk.Label(
            self.frame_hasil, textvariable=self.var_hasil,
            font=("Segoe UI", 13), bg=WARNA_NETRAL, fg="#2c3e50",
            justify="center",
        ).pack(pady=6)

        self.var_predikat = tk.StringVar(value="")
        # Simpan referensi Label-nya juga, agar warna teksnya bisa diubah di show_result()
        self.label_predikat = tk.Label(
            self.frame_hasil, textvariable=self.var_predikat,
            font=("Segoe UI", 14, "bold"), bg=WARNA_NETRAL,
        )
        self.label_predikat.pack(pady=(4, 16))

        baris_hasil = tk.Frame(self.frame_hasil, bg=WARNA_NETRAL)
        baris_hasil.pack(pady=6)

        tk.Button(
            baris_hasil, text="Ulangi Quiz", font=("Segoe UI", 11, "bold"),
            bg=WARNA_BENAR, fg="white", relief="flat", padx=16, pady=6,
            command=self.reset_quiz,
        ).pack(side="left", padx=8)

        tk.Button(
            baris_hasil, text="Keluar", font=("Segoe UI", 11),
            bg=WARNA_SALAH, fg="white", relief="flat", padx=16, pady=6,
            command=self.keluar_aplikasi,
        ).pack(side="left", padx=8)

        tk.Label(
            self.frame_hasil, text="Shortcut: [Enter] ulangi  •  [Esc] keluar",
            font=("Segoe UI", 9), bg=WARNA_NETRAL, fg="#7f8c8d",
        ).pack(pady=(14, 0))

        # ----- Bindings keyboard (dipasang sekali di window) -----
        self.window.bind("<Return>", self._on_key_enter)
        self.window.bind("<KP_Enter>", self._on_key_enter)
        self.window.bind("<Escape>", lambda e: self._on_key_escape())
        for angka in "1234":
            self.window.bind(angka, self._on_key_angka)
            # Nama keysym keypad di Tkinter adalah "KP_1".."KP_4" (bukan "KeyPad_1")
            self.window.bind(f"<KP_{angka}>", self._on_key_angka)

    # ======================================================================
    # STATE & ALUR SOAL
    # ======================================================================
    def _acak_soal(self) -> list[dict]:
        """Mengacak urutan soal DAN urutan opsi, tetap melacak indeks benar.

        Returns:
            Daftar dict soal baru (salinan, bukan merusak bank_soal).
        """
        daftar = [dict(q) for q in self.bank_soal]
        random.shuffle(daftar)
        for soal in daftar:
            # Gabungkan opsi dengan penanda benar, acak, lalu hitung ulang indeks
            penanda = [i == soal["correct"] for i in range(len(soal["options"]))]
            pasangan = list(zip(soal["options"], penanda))
            random.shuffle(pasangan)
            soal["options"] = [p[0] for p in pasangan]
            soal["correct"] = [i for i, p in enumerate(pasangan) if p[1]][0]
        return daftar

    def _reset_state(self) -> None:
        """Mereset seluruh state quiz ke kondisi awal."""
        self.state = {
            "current_question": 0,
            "score": 0,
            "time_left": WAKTU_PER_SOAL,
            "answers": [],
            "status": "bermain",
            "locked": False,
        }
        self.selected_answer.set(-1)
        self.soal_aktif = self._acak_soal()
        self.progress["maximum"] = len(self.soal_aktif)
        self.progress["value"] = 0

    def mulai_quiz(self) -> None:
        """Titik masuk: reset state + tampilkan soal pertama."""
        self._reset_state()
        self.frame_hasil.pack_forget()
        self.frame_soal.pack(fill="both", expand=True)
        self.load_question()

    def reset_quiz(self) -> None:
        """Mengulang quiz dari awal (dipanggil dari layar hasil)."""
        self._batalkan_callback()
        self.mulai_quiz()

    def load_question(self) -> None:
        """Memuat soal current_question ke interface dan memulai timer."""
        idx = self.state["current_question"]

        # Guard: soal habis -> layar hasil
        if idx >= len(self.soal_aktif):
            self.show_result()
            return

        soal = self.soal_aktif[idx]
        total = len(self.soal_aktif)

        # Update header + pilihan jawaban (reset ke -1 = belum memilih)
        self.label_soal.config(text=f"Soal {idx + 1}/{total}")
        self.label_skor.config(text=f"Skor: {self.state['score']}")
        self.progress["value"] = idx
        self.selected_answer.set(-1)

        self.label_pertanyaan.config(text=f"{idx + 1}. {soal['question']}")
        for i, rb in enumerate(self._radio_buttons):
            rb.config(text=f"{i + 1}. {soal['options'][i]}")

        self.state["status"] = "bermain"
        self._kunci_input(False)          # buka kunci input
        self._warnai_frame(WARNA_NETRAL)  # kembalikan warna netral
        self.start_timer()

    # ======================================================================
    # TIMER
    # ======================================================================
    def start_timer(self) -> None:
        """Memulai countdown 30 detik dengan window.after()."""
        self._batalkan_callback()  # cegah timer ganda
        self.state["time_left"] = WAKTU_PER_SOAL
        self._perbarui_label_timer()
        self._id_timer = self.window.after(INTERVAL_TICK, self._tick)

    def _tick(self) -> None:
        """Callback tiap detik: kurangi waktu, ganti warna, cek habis."""
        if self.state["status"] != "bermain":
            return

        self.state["time_left"] -= 1
        self._perbarui_label_timer()

        if self.state["time_left"] <= 0:
            self._id_timer = None
            self._waktu_habis()
        else:
            self._id_timer = self.window.after(INTERVAL_TICK, self._tick)

    def _perbarui_label_timer(self) -> None:
        """Menampilkan sisa waktu + mengubah warna (hijau -> oranye -> merah)."""
        sisa = self.state["time_left"]
        self.label_timer.config(text=f"{sisa}s")
        if sisa > AMBANG_ORANYE:
            warna = WARNA_TIMER_NORMAL
        elif sisa > AMBANG_MERAH:
            warna = WARNA_TIMER_ORANYE
        else:
            warna = WARNA_TIMER_MERAH
        self.label_timer.config(fg=warna)

    def _waktu_habis(self) -> None:
        """Timeout: catat sebagai salah/terlewat, kedip merah, lanjut otomatis."""
        soal = self.soal_aktif[self.state["current_question"]]
        self.state["answers"].append({
            "soal": soal["question"],
            "jawaban_user": None,
            "jawaban_benar": soal["correct"],
            "status": "timeout",
        })
        self._kunci_input(True)
        self._kedip(WARNA_SALAH, lanjut=True)

    # ======================================================================
    # SUBMIT / SKIP
    # ======================================================================
    def submit_answer(self) -> None:
        """Memvalidasi dan memproses jawaban user (dipanggil Enter/klik)."""
        # Abaikan jika animasi berjalan (mencegah double-submit)
        if self.state["locked"] or self.state["status"] != "bermain":
            return

        pilihan = self.selected_answer.get()
        # Validasi: user belum memilih opsi -> peringatan, tidak crash
        if pilihan == -1:
            messagebox.showwarning(
                "Belum Menjawab",
                "Silakan pilih salah satu jawaban terlebih dahulu!",
                parent=self.window,
            )
            return

        soal = self.soal_aktif[self.state["current_question"]]
        benar = (pilihan == soal["correct"])
        if benar:
            self.state["score"] += SKOR_PER_BENAR
        self.label_skor.config(text=f"Skor: {self.state['score']}")

        self.state["answers"].append({
            "soal": soal["question"],
            "jawaban_user": pilihan,
            "jawaban_benar": soal["correct"],
            "status": "benar" if benar else "salah",
        })

        # Kunci input selama animasi, lalu tampilkan warna feedback
        self._kunci_input(True)
        warna = WARNA_BENAR if benar else WARNA_SALAH
        self._kedip(warna, lanjut=True)

    def lewati_soal(self) -> None:
        """Melewati soal tanpa skor (Esc). Catat status 'skip' lalu lanjut."""
        if self.state["locked"] or self.state["status"] != "bermain":
            return

        soal = self.soal_aktif[self.state["current_question"]]
        self.state["answers"].append({
            "soal": soal["question"],
            "jawaban_user": None,
            "jawaban_benar": soal["correct"],
            "status": "skip",
        })
        self._kunci_input(True)
        self._lanjut_soal()

    def _lanjut_soal(self) -> None:
        """Majukan ke soal berikutnya atau tutup quiz jika sudah selesai."""
        self.state["current_question"] += 1
        self.state["locked"] = False
        if self.state["current_question"] >= len(self.soal_aktif):
            self.show_result()
        else:
            self.load_question()

    # ======================================================================
    # ANIMASI (semua via after(), tanpa sleep)
    # ======================================================================
    def _kedip(self, warna: str, lanjut: bool, sisa: int = JUMLAH_KEDIPAN) -> None:
        """Membalik-balikkan warna frame sebanyak sisa kali, lalu lanjut/akhiri.

        Args:
            warna: warna tujuan flash (hijau/merah).
            lanjut: True = pindah soal setelah animasi selesai.
            sisa: jumlah kedipan tersisa (rekursif, tiap panggilan berkurang).
        """
        if sisa <= 0:
            self._id_animasi = None
            self._warnai_frame(WARNA_NETRAL)
            if lanjut:
                self._lanjut_soal()
            return

        # Ganjil -> warna feedback, genap -> kembali netral (efek kedip)
        self._warnai_frame(warna if sisa % 2 == 1 else WARNA_NETRAL)
        self._id_animasi = self.window.after(
            INTERVAL_FLASH, lambda: self._kedip(warna, lanjut, sisa - 1)
        )

    def _warnai_frame(self, warna: str) -> None:
        """Mewarnai frame soal dan seluruh opsi dengan warna tertentu."""
        self.frame_soal.config(bg=warna)
        self.frame_opsi.config(bg=warna)
        self.label_pertanyaan.config(bg=warna)
        self.label_timer.config(bg=warna)
        for rb in self._radio_buttons:
            rb.config(bg=warna, activebackground=warna)

    def _kunci_input(self, terkunci: bool) -> None:
        """Mengunci/membuka kunci seluruh input (cegah double-submit)."""
        self.state["locked"] = terkunci
        status = "disabled" if terkunci else "normal"
        for rb in self._radio_buttons:
            rb.config(state=status)
        self.btn_submit.config(state=status)
        self.btn_skip.config(state=status)

    def _batalkan_callback(self) -> None:
        """Membatalkan semua callback after() yang masih mungkin berjalan."""
        if self._id_timer is not None:
            self.window.after_cancel(self._id_timer)
            self._id_timer = None
        if self._id_animasi is not None:
            self.window.after_cancel(self._id_animasi)
            self._id_animasi = None

    # ======================================================================
    # HASIL AKHIR
    # ======================================================================
    def show_result(self) -> None:
        """Menampilkan ringkasan hasil: skor, persentase, benar/salah/skip."""
        self._batalkan_callback()
        self.state["status"] = "selesai"
        self.state["locked"] = True

        total = len(self.soal_aktif)
        skor = self.state["score"]
        maksimal = total * SKOR_PER_BENAR
        persen = (skor / maksimal * 100) if maksimal else 0

        jumlah = {"benar": 0, "salah": 0, "skip": 0, "timeout": 0}
        for a in self.state["answers"]:
            jumlah[a["status"]] += 1
        # Sisa soal yang tak sempat dijawab sama sekali (jaga-jaga)
        jumlah["salah"] += total - len(self.state["answers"])

        self.var_hasil.set(
            f"Skor akhir : {skor} / {maksimal}  ({persen:.0f}%)\n"
            f"Benar      : {jumlah['benar']}\n"
            f"Salah      : {jumlah['salah']}\n"
            f"Skip       : {jumlah['skip']}\n"
            f"Timeout    : {jumlah['timeout']}"
        )

        # Predikat + warna
        if persen >= 80:
            predikat, warna = "SANGAT BAIK - Kamu paham materi event-driven!", WARNA_BENAR
        elif persen >= 60:
            predikat, warna = "BAIK - Tinggal dipelajari sedikit lagi.", "#2980b9"
        elif persen >= 40:
            predikat, warna = "CUKUP - Ayo pelajari ulang materinya.", WARNA_TIMER_ORANYE
        else:
            predikat, warna = "KURANG - Jangan menyerah, coba lagi!", WARNA_SALAH
        self.var_predikat.set(predikat)
        # Ubah warna pada Label-nya (StringVar tidak punya method config fg/bg)
        self.label_predikat.config(fg=warna)

        self.progress["value"] = total
        self.frame_soal.pack_forget()
        self.frame_hasil.pack(fill="both", expand=True)

    # ======================================================================
    # HANDLER KEYBOARD
    # ======================================================================
    def _on_key_enter(self, _event: tk.Event | None = None) -> str:
        """Enter: submit saat bermain, ulangi saat di layar hasil."""
        if self.state["status"] == "selesai":
            self.reset_quiz()
        else:
            self.submit_answer()
        return "break"  # cegah perilaku default Tkinter

    def _on_key_escape(self) -> None:
        """Esc: lewati soal saat bermain, keluar saat di layar hasil."""
        if self.state["status"] == "selesai":
            self.keluar_aplikasi()
        else:
            self.lewati_soal()

    def _on_key_angka(self, event: tk.Event) -> str:
        """Tombol 1-4: memilih opsi jawaban sesuai nomornya."""
        if self.state["locked"] or self.state["status"] != "bermain":
            return "break"
        teks = event.keysym
        # Normalisasi Keypad_1 -> 1
        angka = int(teks[-1])
        self.selected_answer.set(angka - 1)
        return "break"

    # ======================================================================
    # LAIN-LAIN
    # ======================================================================
    def keluar_aplikasi(self) -> None:
        """Konfirmasi lalu tutup aplikasi dengan bersih (batalkan callback)."""
        if self.state["status"] == "bermain":
            if not messagebox.askyesno(
                "Keluar", "Quiz belum selesai. Yakin ingin keluar?", parent=self.window
            ):
                return
        self._batalkan_callback()
        self.window.destroy()

    def jalankan(self) -> None:
        """Memulai event loop Tkinter - WAJIB dipanggil agar aplikasi tampil."""
        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
