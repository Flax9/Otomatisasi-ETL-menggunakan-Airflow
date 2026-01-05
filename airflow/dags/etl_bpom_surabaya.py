from airflow import DAG
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import logging

# --- KONFIGURASI KONEKSI ---
# Jika menggunakan Docker, gunakan 'host.docker.internal' untuk akses MySQL di XAMPP Windows
SOURCE_DB_URL = 'mysql+pymysql://root:@host.docker.internal:3306/db_monitoring_bpom'
TARGET_DB_URL = 'mysql+pymysql://root:@host.docker.internal:3306/db_dashboard_bpom_staging'

default_args = {
    'owner': 'magang_bpom_surabaya',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def run_etl_process():
    try:
        # 1. Inisialisasi Engine Database
        source_engine = create_engine(SOURCE_DB_URL)
        target_engine = create_engine(TARGET_DB_URL)

        logging.info("Memulai proses ETL...")

        # 2. Cek ID terakhir yang ada di tabel tujuan (Staging)
        # Langkah ini penting agar data tidak duplikat di dashboard
        try:
            last_id_df = pd.read_sql("SELECT MAX(id_pengawasan) as last_id FROM stg_pengawasan_dashboard", target_engine)
            last_id = last_id_df['last_id'].iloc[0]
            if last_id is None:
                last_id = 0
        except Exception as e:
            logging.info(f"Tabel staging belum ada atau kosong: {e}")
            last_id = 0

        # 3. Query Extract & Transform
        # Kita melakukan JOIN agar data di dashboard sudah lengkap dengan Nama Produk & Kategori
        query = f"""
            SELECT
                pl.id_pengawasan,
                pr.nama_produk,
                pr.nomor_izin_edar,
                kp.nama_kategori,
                pl.tanggal_sampling,
                pl.lokasi_sampling,
                pl.hasil_uji,
                pl.tindak_lanjut,
                NOW() as etl_processed_at
            FROM pengawasan_lapangan pl
            JOIN produk_registrasi pr ON pl.id_produk = pr.id_produk
            JOIN kategori_produk kp ON pr.id_kategori = kp.id_kategori
            WHERE pl.id_pengawasan > {last_id}
        """

        # 4. Ambil data dari Source
        df_new_data = pd.read_sql(query, source_engine)

        # 5. Load data ke Staging
        if not df_new_data.empty:
            df_new_data.to_sql('stg_pengawasan_dashboard', target_engine, if_exists='append', index=False)
            logging.info(f"Berhasil memindahkan {len(df_new_data)} data baru ke Staging.")
        else:
            logging.info("Tidak ada data baru untuk disinkronkan.")

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat ETL: {e}")
        raise e

# --- DEFINISI DAG ---
with DAG(
    'etl_bpom_surabaya_monitoring',
    default_args=default_args,
    description='Sinkronisasi data pengawasan BPOM Surabaya ke Dashboard Staging',
    schedule_interval='*/5 * * * *',  # Berjalan otomatis setiap 5 menit
    catchup=False,
    tags=['bpom', 'surabaya', 'etl']
) as dag:

    etl_task = PythonOperator(
        task_id='sinkronisasi_data_pengawasan',
        python_callable=run_etl_process
    )