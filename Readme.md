# 📊 Sistem Dashboard Pengawasan BPOM (ETL Pipeline)

Proyek ini merupakan sistem integrasi antara **Airflow (Python/Docker)** sebagai mesin pengolah data (ETL) dan **CodeIgniter 4 (PHP)** sebagai interface dashboard utama.

## 🏗️ Struktur Proyek

* `airflow/`: Konfigurasi orchestrator dan file DAG (Python).
* `application_ci/`: Web Dashboard berbasis Framework CodeIgniter 4.
* `dashboard/`: Prototype dashboard menggunakan Streamlit.
* `data_dummy/`: Dataset awal dan script generator data untuk simulasi.

---

## ✨ Fitur Dashboard Visual (Baru)

Interface CodeIgniter kini dilengkapi dengan visualisasi data interaktif:

* **Analitik Kepatuhan (Donut Chart)**: Visualisasi persentase produk "Memenuhi Syarat" vs "Tidak Memenuhi Syarat" secara real-time.
* **Tren Pengujian (Area Chart)**: Grafik pergerakan jumlah sampel data yang masuk dari pipeline ETL dalam 7 hari terakhir.
* **Smart Badging**: Penandaan otomatis warna pada tabel data untuk identifikasi cepat produk berbahaya.

> **⚠️ Prasyarat Koneksi:**
> Dashboard ini menggunakan library **Chart.js** dan **Bootstrap 5** melalui CDN. Pastikan perangkat memiliki **koneksi internet aktif** saat menjalankan dashboard.

---

## 🚀 Langkah-Langkah Persiapan (Setup)

### 1. Konfigurasi Lingkungan (Environment Variables)

Sistem ini membutuhkan **2 file `.env`** yang berbeda. Silakan buat file `.env` di lokasi berikut dan salin konfigurasi di bawah ini:

#### A. Konfigurasi Root (Docker & Airflow)
Buat file bernama `.env` di **folder root** proyek utama:

```ini
# --- AIRFLOW CONFIGURATION ---
AIRFLOW_UID=50000
COMPOSE_PROJECT_NAME=bpom_etl_pipeline

# --- DATABASE CREDENTIALS ---
# Masukkan password database lokal Anda di sini
MYSQL_AIRFLOW_USER=airflow_sys
MYSQL_AIRFLOW_PASSWORD=
MYSQL_AIRFLOW_DB=airflow_db

MYSQL_WORKER_USER=etl_worker_bpom
MYSQL_WORKER_PASSWORD=
MYSQL_WORKER_DB=db_pengawasan_bpom

# Host Database (Akses dari dalam container Docker)
DB_HOST=host.docker.internal
DB_PORT=3306