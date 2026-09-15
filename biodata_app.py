# Day 1 pakai Python

# Mengimpor library tkinter
import tkinter as tk

# Membuat jendela utama
window = tk.Tk()

# Memberikan judul pada jendela
window.title("Form Biodata Mahasiswa")

# Mengatur ukuran jendela (lebar x tinggi)
window.geometry("1000x1000")

# Mencegah jendela dapat diubah ukurannya
window.resizable(False, False)

# Membuat label judul
label_judul = tk.Label(
    master=window,
    text="FORM BIODATA MAHASISWA",
    font=("Times New Roman", 20, "bold")
)

# Menampilkan label dengan pack
label_judul.pack(pady=50)

# mengatur background
window.configure(bg="firebrick")

# Label untuk input nama
label_nama = tk.Label(master=window, text="Nama Lengkap:", font=("Arial", 12))
label_nama.pack(pady=5)
# Entry untuk input nama
entry_nama = tk.Entry(master=window, width=50)
entry_nama.pack(pady=5)

# Label untuk input nim
label_nim = tk.Label(master=window, text="NIM:", font=("Arial", 12))
label_nim.pack(pady=5)
# Entry untuk input nim
entry_nim = tk.Entry(master=window, width=50)
entry_nim.pack(pady=5)

# Fungsi untuk mengambil teks dari entry dan menampilkannya di label_hasil
def ambil_data():
    nama = entry_nama.get()
    nim = entry_nim.get()
    # Mengubah teks pada label_hasil agar sesuai dengan input
    label_hasil.config(text=f"Biodata diinput: {nama} dengan Nim: {nim}")

# Membuat label kosong untuk menampilkan hasil input nantinya
label_hasil = tk.Label(
    master=window,
    text="", 
    font=("Arial", 16, "bold"), 
    bg="firebrick", 
    fg="white"
)
label_hasil.pack(pady=20)

# Membuat tombol untuk memicu fungsi
btn = tk.Button(window, text="Tampilkan di Window", command=ambil_data, font=("Arial", 12))
btn.pack(pady=10)

# Menjalankan event loop
window.mainloop()