-- 1. Buat Database
CREATE DATABASE IF NOT EXISTS db_monitoring_bpom;

-- Pilih Database
USE db_monitoring_bpom;

-- 2. Buat Tabel Kategori
CREATE TABLE kategori_produk (
    id_kategori INT PRIMARY KEY AUTO_INCREMENT,
    nama_kategori VARCHAR(50)
);

-- 3. Buat Tabel Produk
CREATE TABLE produk_registrasi (
    id_produk INT PRIMARY KEY AUTO_INCREMENT,
    nomor_izin_edar VARCHAR(20) UNIQUE,
    nama_produk VARCHAR(100),
    nama_perusahaan VARCHAR(100),
    id_kategori INT,
    tanggal_terbit DATE,
    status_registrasi ENUM('Aktif', 'Habis Masa Berlaku', 'Dicabut'),
    FOREIGN KEY (id_kategori) REFERENCES kategori_produk(id_kategori)
);

-- 4. Buat Tabel Pengawasan Lapangan
CREATE TABLE pengawasan_lapangan (
    id_pengawasan INT PRIMARY KEY AUTO_INCREMENT,
    id_produk INT,
    tanggal_sampling DATE,
    lokasi_sampling VARCHAR(100),
    hasil_uji ENUM('Memenuhi Syarat', 'Tidak Memenuhi Syarat'),
    temuan_pelanggaran TEXT,
    tindak_lanjut VARCHAR(100),
    FOREIGN KEY (id_produk) REFERENCES produk_registrasi(id_produk)
);

-- 5. Isi Kategori Awal
INSERT INTO kategori_produk (nama_kategori) VALUES ('Obat'), ('Makanan Olahan'), ('Kosmetik'), ('Suplemen');

-- 6. Kolom Timestamp
ALTER TABLE pengawasan_lapangan ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;