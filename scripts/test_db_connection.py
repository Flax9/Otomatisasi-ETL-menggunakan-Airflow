import pandas as pd
from sqlalchemy import create_engine
import sys

# --- KONFIGURASI ---
# Sesuaikan jika kamu tidak menggunakan password
SOURCE_URL = 'mysql+pymysql://root:@host.docker.internal:3306/db_monitoring_bpom'
TARGET_URL = 'mysql+pymysql://root:@host.docker.internal:3306/db_dashboard_bpom_staging'

def test_connection(name, url):
    print(f"--- Mengetes Koneksi ke {name} ---")
    try:
        engine = create_engine(url)
        # Mencoba melakukan query ringan
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            if result:
                print(f"Berhasil terhubung ke {name}!")
    except Exception as e:
        print(f"Gagal terhubung ke {name}.")
        print(f"Kesalahan: {e}")
        return False
    return True

if __name__ == "__main__":
    source_ok = test_connection("Database Source (Dummy BPOM)", SOURCE_URL)
    target_ok = test_connection("Database Target (Staging)", TARGET_URL)

    if source_ok and target_ok:
        print("\nSemua sistem siap! Kamu bisa lanjut menjalankan Airflow.")
    else:
        print("\nPerhatian: Perbaiki koneksi database sebelum lanjut ke Airflow.")
        sys.exit(1)