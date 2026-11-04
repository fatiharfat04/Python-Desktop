CREATE DATABASE IF NOT EXISTS db_penggajian_modul5 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_penggajian_modul5;
CREATE TABLE IF NOT EXISTS karyawan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nik VARCHAR(20) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    jabatan VARCHAR(60) NOT NULL,
    gaji_pokok BIGINT NOT NULL,
    tunjangan BIGINT NOT NULL DEFAULT 0,
    aktif TINYINT NOT NULL DEFAULT 1
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS penggajian (
    id INT AUTO_INCREMENT PRIMARY KEY,
    karyawan_id INT NOT NULL,
    periode CHAR(7) NOT NULL,
    nik VARCHAR(20) NOT NULL,
    nama VARCHAR(100) NOT NULL,
    jabatan VARCHAR(60) NOT NULL,
    gaji_pokok BIGINT NOT NULL,
    tunjangan BIGINT NOT NULL,
    jam_lembur INT NOT NULL,
    tarif_lembur BIGINT NOT NULL,
    uang_lembur BIGINT NOT NULL,
    potongan BIGINT NOT NULL,
    bruto BIGINT NOT NULL,
    netto BIGINT NOT NULL,
    dibuat_pada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_gaji_karyawan FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE RESTRICT,
    CONSTRAINT uq_gaji_periode UNIQUE (karyawan_id, periode)
) ENGINE=InnoDB;