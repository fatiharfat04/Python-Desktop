# List (mutable, paling sering dipakai)
angka = [1, 2, 3, 4, 5]
angka.append(6)
angka.remove(2)
print(angka[0])          # akses index
print(angka[-1])         # index terakhir
print(angka[1:3])        # slicing

# Tuple (immutable)
koordinat = (10, 20)

# Dictionary (key-value pair)
mahasiswa = {
    "nama": "Ani",
    "umur": 21
}
print(mahasiswa["nama"])
mahasiswa["jurusan"] = "Informatika"  # tambah key baru

# Set (unik, tidak berurutan)
warna = {"merah", "biru", "hijau"}