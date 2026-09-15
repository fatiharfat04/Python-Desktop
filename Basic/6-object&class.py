class Mahasiswa:
    # Constructor
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

    # Method
    def perkenalan(self):
        return f"Saya {self.nama}, umur {self.umur} tahun"

# Membuat object (instance)
mhs1 = Mahasiswa("Ani", 21)
print(mhs1.perkenalan())

# Inheritance (pewarisan)
class MahasiswaS2(Mahasiswa):
    def __init__(self, nama, umur, universitas):
        super().__init__(nama, umur)
        self.universitas = universitas

    def info(self):
        return f"{self.nama} kuliah S2 di {self.universitas}"

mhs2 = MahasiswaS2("Rio", 24, "UGM")
print(mhs2.info())