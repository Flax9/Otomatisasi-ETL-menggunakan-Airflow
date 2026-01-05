-- 1. Buat Database Staging (Jika belum ada)
CREATE DATABASE IF NOT EXISTS db_dashboard_bpom_staging;
USE db_dashboard_bpom_staging;

-- 2. Buat Tabel Flat untuk Dashboard
-- Tabel ini akan menampung gabungan data dari kategori, produk, dan hasil pengawasan
CREATE TABLE stg_pengawasan_dashboard (
    id_pengawasan INT PRIMARY KEY,         -- Diambil dari source
    nama_produk VARCHAR(100),              -- Hasil Join
    nomor_izin_edar VARCHAR(20),           -- Hasil Join
    nama_kategori VARCHAR(50),             -- Hasil Join
    tanggal_sampling DATE,                 -- Data mentah
    lokasi_sampling VARCHAR(100),          -- Data mentah
    hasil_uji VARCHAR(50),                 -- Memenuhi / Tidak Memenuhi Syarat
    tindak_lanjut VARCHAR(100),            -- Rekomendasi tindakan
    etl_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Audit trail ETL
);

-- 3. (Opsional) Buat Index untuk mempercepat loading dashboard
CREATE INDEX idx_hasil_uji ON stg_pengawasan_dashboard(hasil_uji);
CREATE INDEX idx_kategori ON stg_pengawasan_dashboard(nama_kategori);