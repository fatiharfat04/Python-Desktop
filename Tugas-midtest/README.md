# Quiz Interaktif — Tugas Akhir Pemrograman GUI

Aplikasi kuis pilihan ganda interaktif berbasis **Python 3 + Tkinter**.
Dirancang sebagai tugas akhir mata kuliah pemrograman GUI, sekaligus contoh
penerapan **event-driven programming** (event loop, callback, binding, timer).

> **Kabar baik:** program ini **tidak memerlukan library tambahan apa pun**.
> `tkinter` sudah ikut terpasang bersama Python. Jadi yang perlu Anda install
> hanya **Python** itu sendiri.

---

## Daftar Isi

1. [Fitur Aplikasi](#1-fitur-aplikasi)
2. [Persyaratan Sistem](#2-persyaratan-sistem)
3. [Cara Install Python](#3-cara-install-python)
4. [Memeriksa Apakah Tkinter Sudah Siap](#4-memeriksa-apakah-tkinter-sudah-siap)
5. [Cara Menjalankan Aplikasi](#5-cara-menjalankan-aplikasi)
6. [Cara Bermain](#6-cara-bermain)
7. [Cara Mengubah Isi Soal](#7-cara-mengubah-isi-soal)
8. [Tanya Jawab Umum (Troubleshooting)](#8-tanya-jawab-umum-troubleshooting)

---

## 1. Fitur Aplikasi

| Fitur | Penjelasan |
| --- | --- |
| Pilihan ganda | 10 soal, masing-masing dengan 4 opsi jawaban (Radiobutton) |
| Timer hitung mundur | 30 detik per soal; warna berubah **hijau → oranye → merah** saat waktu menipis |
| Timeout otomatis | Jika waktu habis, soal dianggap salah dan langsung lanjut ke soal berikutnya |
| Skor & progres real-time | Menampilkan "Soal 3/10", "Skor: 20", dan progress bar |
| Animasi feedback | Frame berkedip **hijau** (benar) / **merah** (salah/timeout) |
| Validasi jawaban | Tidak boleh lanjut tanpa memilih opsi — muncul peringatan |
| Acak soal & opsi | Urutan soal **dan** urutan opsi diacak tiap sesi (tidak ada kebocoran jawaban) |
| Ringkasan hasil akhir | Skor, persentase, jumlah benar/salah/skip/timeout, tombol Ulangi & Keluar |
| Shortcut keyboard | `Enter` submit, `Esc` lewati, `1`–`4` pilih opsi |

---

## 2. Persyaratan Sistem

- **Sistem operasi:** Windows 7/8/10/11, macOS, atau Linux
- **Python versi 3.10 atau lebih baru** (program memakai fitur `str | None`
  yang baru ada di Python 3.10)
- Tidak perlu koneksi internet setelah Python terpasang
- Tidak perlu `pip install` apa pun

---

## 3. Cara Install Python

### Windows

1. Buka browser, kunjungi **https://www.python.org/downloads/**
2. Klik tombol kuning **"Download Python 3.x.x"**
3. Buka file installer yang sudah terunduh
4. **PENTING:** centang kotak **"Add Python to PATH"** di bagian bawah jendela
   installer (lewatkan ini = program tidak akan dikenali terminal)
5. Klik **"Install Now"**
6. Tunggu sampai selesai, lalu tutup installer

   ![Centang Add Python to PATH sebelum klik Install Now]

### macOS

1. Kunjungi **https://www.python.org/downloads/**
2. Unduh installer `.pkg` untuk macOS
3. Buka file `.pkg`, ikuti petunjuk sampai selesai

> Alternatif (lebih mudah jika sudah punya Homebrew):
> buka Terminal, ketik `brew install python`, lalu tekan Enter.

### Linux (Ubuntu / Debian)

Buka Terminal, lalu jalankan perintah berikut satu per satu:

```bash
sudo apt update
sudo apt install python3 python3-tk
```

> Catatan: di Linux, paket `python3-tk` **wajib** karena Tkinter tidak selalu
> ikut bersama paket `python3` dasar.

---

## 4. Memeriksa Apakah Tkinter Sudah Siap

Buka **Terminal** (Windows: tekan `Win+R`, ketik `cmd`, tekan Enter),
lalu jalankan perintah berikut:

```bash
python --version
```

Jika muncul `Python 3.10.0` (atau versi lebih baru), berarti Python sudah benar.

> **Jika muncul:** `'python' is not recognized as internal or external command`
> berarti Anda lupa mencentang **"Add Python to PATH"** saat install.
> **Solusi cepat:** jalankan ulang installer Python → klik **"Modify"** →
> centang **"Add Python to PATH"** → Next sampai selesai.

Kemudian uji Tkinter dengan menjalankan:

```bash
python -c "import tkinter; print('Tkinter siap!')"
```

Jika muncul **`Tkinter siap!`**, aplikasi sudah siap dijalankan.

---

## 5. Cara Menjalankan Aplikasi

### Cara 1 — Melalui Terminal (disarankan)

1. Buka Terminal / Command Prompt
2. Masuk ke folder tempat file `quiz_app.py` berada.
   Contoh (ganti dengan lokasi folder Anda):

   ```bash
   cd D:\Coding\Desktop-matkul\Tugas-midtest
   ```

3. Jalankan program dengan mengetik:

   ```bash
   python quiz_app.py
   ```

   > macOS/Linux gunakan: `python3 quiz_app.py`

4. Jendela **"Quiz Interaktif - Tugas Akhir"** akan langsung muncul.

### Cara 2 — Klik dua kali file (paling sederhana)

Cukup **klik dua kali** file `quiz_app.py` di File Explorer (Windows) atau
Finder (macOS). Jendela quiz akan terbuka otomatis.

> Syarat: saat install Python, opsi **"Add Python to PATH"** (Windows) atau
> asosiasi file `.py` (macOS) harus aktif.

---

## 6. Cara Bermain

Setelah jendela quiz terbuka:

1. **Baca soal** yang tampil di layar
2. **Pilih salah satu jawaban** dengan cara:
   - Klik salah satu lingkaran (radio button) di pilihan jawaban, **ATAU**
   - Tekan tombol angka **`1`**, **`2`**, **`3`**, atau **`4`** sesuai nomor opsi
3. **Kirim jawaban** dengan:
   - Klik tombol **"Submit Jawaban"**, **ATAU**
   - Tekan tombol **`Enter`**
4. Jika **benar**, frame berkedip **hijau**. Jika **salah**, frame berkedip
   **merah**. Skor bertambah 10 untuk jawaban benar.
5. **Melewati soal** (tanpa skor): klik **"Lewati"** atau tekan **`Esc`**
6. **Perhatikan timer** di pojok kanan atas — warnanya berubah
   hijau → oranye → merah mendekati 0. Jika waktu habis, soal otomatis
   dianggap salah dan aplikasi lanjut sendiri.
7. Setelah soal ke-10, **layar hasil** menampilkan skor akhir, persentase,
   dan predikat.
8. Di layar hasil:
   - **`Enter`** atau tombol **"Ulangi Quiz"** → mulai lagi dari awal
     (soal diacak ulang, skor direset)
   - **`Esc`** atau tombol **"Keluar"** → tutup aplikasi

---

## 7. Cara Mengubah Isi Soal

Seluruh soal tersimpan di dalam list **`bank_soal`** pada method `__init__`
di file `quiz_app.py`. Untuk menambah atau mengubah soal, ikuti pola berikut:

```python
{
    "question": "Tulis pertanyaan di sini?",
    "options": [
        "Opsi pertama",
        "Opsi kedua",
        "Opsi ketiga",
        "Opsi keempat",
    ],
    "correct": 1,   # angka ini menunjuk Opsi ke-(angka+1); 0 = opsi pertama
},
```

**Aturan penting:**

- Setiap soal harus memiliki **tepat 4 opsi**
- Nilai `"correct"` dihitung mulai dari **0** (bukan 1)
  - `"correct": 0` → opsi pertama benar
  - `"correct": 3` → opsi keempat benar
- Anda boleh menambah lebih dari 10 soal — progress bar, perhitungan skor,
  dan persentase akan menyesuaikan secara otomatis

---

## 8. Tanya Jawab Umum (Troubleshooting)

**Q: Muncul pesan `'python' is not recognized` saat mengetik `python quiz_app.py`**
A: Python belum masuk PATH. Jalankan ulang installer Python → klik
**Modify** → centang **"Add Python to PATH"** → selesaikan instalasi ulang.
Alternatif sementara: coba perintah `py quiz_app.py` (hanya Windows).

**Q: Muncul pesan `ModuleNotFoundError: No module named 'tkinter'`**
A: Tkinter belum terpasang.
- **Windows:** jalankan ulang installer Python → klik **Modify** → pastikan
  komponen **"tcl/tk and IDLE"** tercentang.
- **Ubuntu/Debian:** jalankan `sudo apt install python3-tk`
- **macOS:** jalankan ulang installer `.pkg` dari python.org

**Q: Muncul pesan `SyntaxError` saat program dijalankan**
A: Kemungkinan Anda memakai Python versi lama (3.9 ke bawah). Cek versi
dengan `python --version`. Program ini membutuhkan **Python 3.10+**.
Unduh versi terbaru di https://www.python.org/downloads/

**Q: Tombol angka `1`–`4` tidak berfungsi**
A: Pastikan fokus (kursor) ada di **jendela quiz**, bukan di terminal.
Klik sekali pada area kosong jendela quiz lalu coba tekan lagi.

**Q: Jendela quiz tidak muncul padahal terminal tidak menampilkan error**
A: Kemungkinan jendela muncul di layar lain atau tertutup program lain.
Cek **Task Manager** (Windows) atau **Alt+Tab** untuk mencari jendela
berjudul "Quiz Interaktif - Tugas Akhir".

**Q: Layar menjadi "Not Responding" sebentar**
A: Ini tidak seharusnya terjadi karena program memakai `after()` (non-blocking),
bukan `sleep()`. Jika terjadi, kemungkinan komputer sedang sangat lambat.
Tutup aplikasi dan jalankan ulang.

**Q: Bagaimana cara menutup aplikasi di tengah quiz?**
A: Klik tombol **X** di pojok jendela atau tekan **Esc** di layar hasil.
Saat quiz masih berjalan, aplikasi akan menampilkan konfirmasi dulu agar
Anda tidak kehilangan jawaban secara tidak sengaja.

---

## Struktur File

```
Tugas-midtest/
├── quiz_app.py    ← seluruh kode aplikasi (satu file, tanpa dependensi eksternal)
└── README.md      ← panduan ini
```

---

## Jalankan Sekarang

```bash
cd D:\Coding\Desktop-matkul\Tugas-midtest
python quiz_app.py
```

Selamat mengerjakan tugas dan selamat bermain! 🎓
