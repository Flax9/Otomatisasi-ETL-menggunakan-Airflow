import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard Monitoring BPOM", layout="wide")

st.title("📊 Monitoring Pengawasan Lapangan - BPOM Surabaya")

# Koneksi ke Database Staging
# Gunakan 'localhost' jika menjalankan streamlit dari terminal lokal
engine = create_engine('mysql+pymysql://root:@localhost:3306/db_dashboard_bpom_staging')

try:
    df = pd.read_sql("SELECT * FROM stg_pengawasan_dashboard", engine)

    # Metrik Ringkas
    col1, col2 = st.columns(2)
    col1.metric("Total Pengawasan", len(df))
    col2.metric("Produk TMS (Tidak Memenuhi Syarat)", len(df[df['hasil_uji'] == 'Tidak Memenuhi Syarat']))

    # Tabel Data
    st.subheader("Data Hasil Sinkronisasi ETL")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data: {e}")
    st.info("Pastikan database staging sudah ada dan Airflow sudah memindahkan data.")