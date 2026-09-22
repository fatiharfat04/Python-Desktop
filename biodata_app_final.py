# ==========================================
# FILE: biodata_app_final.py
# DESKRIPSI: Aplikasi Biodata Mahasiswa menggunakan GUI Tkinter
# ==========================================

# ==========================================
# 1. IMPORT LIBRARY
# ==========================================
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 2. INISIALISASI JENDELA UTAMA
# ==========================================
window = tk.Tk()
window.title("Form Biodata") # Menambahkan title yang sebelumnya belum ada
window.resizable(True, True)
window.minsize(500, 600)

# ==========================================
# 3. VARIABEL KONTROL (Tkinter Variables)
# ==========================================
# Variabel untuk menyimpan input form dan mentrigger validasi
var_nama = tk.StringVar()
var_nim = tk.StringVar()
var_jurusan = tk.StringVar()

# Variabel untuk radio button dan checkbox
var_jk = tk.StringVar(value="Pria")
var_setuju = tk.IntVar()


# ==========================================
# 4. FUNGSI-FUNGSI LOGIKA APLIKASI
# ==========================================

def validate_form(*args):
    """Validasi form secara real-time. Tombol submit aktif jika semua syarat terpenuhi."""
    nama_valid = var_nama.get().strip() != ""
    nim_valid = var_nim.get().strip() != ""
    jurusan_valid = var_jurusan.get().strip() != ""
    setuju_valid = var_setuju.get() == 1

    if nama_valid and nim_valid and jurusan_valid and setuju_valid:
        btn_submit.config(state=tk.NORMAL)
    else:
        btn_submit.config(state=tk.DISABLED)

def submit_data():
    """Mengambil semua data, mengecek validasi akhir, lalu menampilkannya."""
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui pengumpulan data!")
        return

    # Mengambil nilai dari input form
    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    jenis_kelamin = var_jk.get()
    
    if not nama or not nim or not jurusan:
        messagebox.showwarning("Input Kosong", "Semua field harus diisi!")
        return

    # Format hasil output
    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
    
    # Menampilkan hasil ke pop-up dan label di aplikasi
    messagebox.showinfo("Data Tersimpan", hasil)
    label_hasil.config(text=f"BIODATA TERSIMPAN:\n\n{hasil}")

def submit_shortcut(event=None):
    """Trigger submit ketika tombol Enter ditekan pada input."""
    if btn_submit['state'] == tk.NORMAL:
        submit_data()

def simpan_hasil():
    """Menyimpan data hasil inputan ke dalam file .txt."""
    hasil_tersimpan = label_hasil.cget("text")

    if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
        messagebox.showwarning("Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
        return

    # Menyimpan ke file teks
    try:
        with open("biodata_tersimpan.txt", "w") as file:
            file.write(hasil_tersimpan)
        messagebox.showinfo("Info", "Data berhasil disimpan ke file 'biodata_tersimpan.txt'.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

def keluar_aplikasi():
    """Fungsi prompt konfirmasi untuk menutup aplikasi."""
    if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
        window.destroy()

# Fungsi untuk efek visual Hover Tombol
def on_enter(event):
    if btn_submit['state'] == tk.NORMAL:
        btn_submit.config(bg="lightblue")

def on_leave(event):
    btn_submit.config(bg="SystemButtonFace") # Mengembalikan ke warna default


# ==========================================
# 5. BINDING & TRACING (Observer)
# ==========================================
# Memantau perubahan teks untuk memanggil fungsi validate_form
var_nama.trace_add("write", validate_form)
var_nim.trace_add("write", validate_form)
var_jurusan.trace_add("write", validate_form)


# ==========================================
# 6. PEMBUATAN UI (User Interface)
# ==========================================

# -- Frame Utama --
main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.grid_columnconfigure(1, weight=1) # Membuat layout responsif

# -- Judul Form --
label_judul = tk.Label(master=main_frame, text="FORM BIODATA MAHASISWA", font=("Arial", 16, "bold"))
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

# -- Frame Input (Grup ber-border) --
frame_input = tk.Frame(master=main_frame, relief=tk.GROOVE, borderwidth=3, padx=10, pady=10)
frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")
frame_input.grid_columnconfigure(1, weight=1) # Agar Entry bisa expand/melebar

# 1. Input Nama
label_nama = tk.Label(master=frame_input, text="Nama Lengkap:", font=("Arial", 12))
label_nama.grid(row=0, column=0, sticky="W", pady=5)
entry_nama = tk.Entry(master=frame_input, font=("Arial", 12), textvariable=var_nama)
entry_nama.grid(row=0, column=1, sticky="EW", pady=5)

# 2. Input NIM
label_nim = tk.Label(master=frame_input, text="NIM:", font=("Arial", 12))
label_nim.grid(row=1, column=0, sticky="W", pady=5)
entry_nim = tk.Entry(master=frame_input, font=("Arial", 12), textvariable=var_nim)
entry_nim.grid(row=1, column=1, sticky="EW", pady=5)

# 3. Input Jurusan
label_jurusan = tk.Label(master=frame_input, text="Jurusan:", font=("Arial", 12))
label_jurusan.grid(row=2, column=0, sticky="W", pady=5)
entry_jurusan = tk.Entry(master=frame_input, font=("Arial", 12), textvariable=var_jurusan)
entry_jurusan.grid(row=2, column=1, sticky="EW", pady=5)

# 4. Input Alamat (Widget Text & Scrollbar)
label_alamat = tk.Label(master=frame_input, text="Alamat:", font=("Arial", 12))
label_alamat.grid(row=3, column=0, sticky="NW", pady=5)

frame_alamat = tk.Frame(master=frame_input, relief=tk.SUNKEN, borderwidth=1)
frame_alamat.grid(row=3, column=1, sticky="EW", pady=5)
frame_alamat.grid_columnconfigure(0, weight=1)

scrollbar_alamat = tk.Scrollbar(master=frame_alamat)
scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

text_alamat = tk.Text(master=frame_alamat, height=5, font=("Arial", 12))
text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Menghubungkan text widget dengan scrollbar
scrollbar_alamat.config(command=text_alamat.yview)
text_alamat.config(yscrollcommand=scrollbar_alamat.set)

# 5. Radio Button Jenis Kelamin
label_jk = tk.Label(master=frame_input, text="Jenis Kelamin:", font=("Arial", 12))
label_jk.grid(row=4, column=0, sticky="W", pady=5)

frame_jk = tk.Frame(master=frame_input)
frame_jk.grid(row=4, column=1, sticky="W")

radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
radio_pria.pack(side=tk.LEFT)
radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
radio_wanita.pack(side=tk.LEFT)

# 6. Checkbox Persetujuan
check_setuju = tk.Checkbutton(
    master=frame_input,
    text="Saya menyetujui pengumpulan data ini.",
    variable=var_setuju,
    font=("Arial", 10),
    command=validate_form # Validasi setiap kali dicentang/uncentang
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

# -- Tombol Submit --
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit Biodata", 
    font=("Arial", 12, "bold"),
    command=submit_data,
    state=tk.DISABLED
)
btn_submit.grid(row=2, column=0, columnspan=2, pady=20, sticky="EW")

# Menambahkan efek visual pada tombol
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

# -- Label Teks Hasil --
label_hasil = tk.Label(master=main_frame, text="", font=("Arial", 12, "italic"), justify=tk.LEFT)
label_hasil.grid(row=3, column=0, columnspan=2, sticky="W", padx=10)


# ==========================================
# 7. SHORTCUT KEYBOARD
# ==========================================
# Menghubungkan tombol "Enter" di keyboard dengan fungsi submit
entry_nama.bind("<Return>", submit_shortcut)
entry_nim.bind("<Return>", submit_shortcut)
entry_jurusan.bind("<Return>", submit_shortcut)
text_alamat.bind("<Return>", submit_shortcut)


# ==========================================
# 8. MENU BAR
# ==========================================
menu_bar = tk.Menu(master=window)
window.config(menu=menu_bar)

# Menu Utama "File"
file_menu = tk.Menu(master=menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

# Sub-menu di dalam "File"
file_menu.add_command(label="Simpan Hasil", command=simpan_hasil)
file_menu.add_separator() # Garis pemisah
file_menu.add_command(label="Keluar", command=keluar_aplikasi)


# ==========================================
# 9. MAIN LOOP
# ==========================================
# Menjalankan event loop GUI aplikasi
if __name__ == "__main__":
    window.mainloop()