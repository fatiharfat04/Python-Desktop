from mysql.connector import IntegrityError
from database import koneksi
from model import hitung_gaji, periode_valid

class KaryawanRepository:
    def semua(self, cari="", hanya_aktif=False):
        with koneksi() as db, db.cursor(dictionary=True) as cur:
            sql = "SELECT * FROM karyawan WHERE (LOCATE(%s,nik)>0 OR LOCATE(%s,nama)>0)"
            if hanya_aktif:
                sql += " AND aktif=1"
            cur.execute(sql + " ORDER BY nama,id", (cari,cari))
            return cur.fetchall()

    def simpan(self, m, id_karyawan=None):
        data = (m.nik,m.nama,m.jabatan,m.gaji_pokok,m.tunjangan,m.aktif)
        try:
            with koneksi() as db, db.cursor() as cur:
                if id_karyawan is None:
                    cur.execute("INSERT INTO karyawan(nik,nama,jabatan,gaji_pokok,tunjangan,aktif) VALUES(%s,%s,%s,%s,%s,%s)",data)
                else:
                    cur.execute("SELECT id FROM karyawan WHERE id=%s FOR UPDATE",(id_karyawan,))
                    if cur.fetchone() is None:
                        raise ValueError("Karyawan tidak ditemukan. Muat ulang data.")
                    cur.execute("UPDATE karyawan SET nik=%s,nama=%s,jabatan=%s,gaji_pokok=%s,tunjangan=%s,aktif=%s WHERE id=%s",data+(id_karyawan,))
                db.commit()
        except IntegrityError as exc:
            if exc.errno == 1062:
                raise ValueError("NIK internal sudah digunakan.") from exc
            raise

    def hapus(self, id_karyawan):
        try:
            with koneksi() as db, db.cursor() as cur:
                cur.execute("DELETE FROM karyawan WHERE id=%s",(id_karyawan,))
                if cur.rowcount == 0:
                    raise ValueError("Karyawan tidak ditemukan.")
                db.commit()
        except IntegrityError as exc:
            if exc.errno == 1451:
                raise ValueError("Karyawan memiliki riwayat gaji. Ubah status menjadi nonaktif, jangan dihapus.") from exc
            raise

class GajiRepository:
    def simpan(self, id_karyawan, periode, jam, tarif, potongan):
        periode = periode_valid(periode)
        try:
            with koneksi() as db, db.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM karyawan WHERE id=%s FOR UPDATE",(id_karyawan,))
                k = cur.fetchone()
                if k is None or k["aktif"] != 1:
                    raise ValueError("Karyawan tidak ada atau sudah nonaktif.")
                hasil = hitung_gaji(k["gaji_pokok"],k["tunjangan"],jam,tarif,potongan)
                values = (id_karyawan,periode,k["nik"],k["nama"],k["jabatan"],
                          hasil["gaji_pokok"],hasil["tunjangan"],hasil["jam_lembur"],
                          hasil["tarif_lembur"],hasil["uang_lembur"],hasil["potongan"],
                          hasil["bruto"],hasil["netto"])
                cur.execute("""INSERT INTO penggajian
                    (karyawan_id,periode,nik,nama,jabatan,gaji_pokok,tunjangan,
                     jam_lembur,tarif_lembur,uang_lembur,potongan,bruto,netto)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",values)
                id_gaji = cur.lastrowid
                db.commit()
                return id_gaji
        except IntegrityError as exc:
            if exc.errno == 1062:
                raise ValueError("Gaji karyawan pada periode ini sudah tersimpan.") from exc
            raise

    def semua(self, periode):
        periode = periode_valid(periode)
        with koneksi() as db, db.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM penggajian WHERE periode=%s ORDER BY nama,id",(periode,))
            return cur.fetchall()

    def ringkasan(self, periode):
        with koneksi() as db, db.cursor(dictionary=True) as cur:
            cur.execute("SELECT COUNT(*) AS total FROM karyawan WHERE aktif=1")
            total = cur.fetchone()["total"]
            cur.execute("SELECT COUNT(*) AS slip,COALESCE(SUM(netto),0) AS netto FROM penggajian WHERE periode=%s",(periode_valid(periode),))
            return dict(aktif=total, **cur.fetchone())