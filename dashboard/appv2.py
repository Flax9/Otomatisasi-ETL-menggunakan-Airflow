import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px # Opsional untuk grafik lebih bagus

st.set_page_config(page_title="Dashboard BPOM", layout="wide")

st.title("🛡️ Dashboard Monitoring Pengawasan BPOM")
st.markdown("Data ini ditarik secara otomatis menggunakan **Apache Airflow**.")

# Fungsi Koneksi
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="etl_worker_bpom",
        password="etl_password_456",
        database="db_dashboard_bpom_staging"
    )
    query = "SELECT * FROM stg_pengawasan_dashboard"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    # 1. Menarik data mentah dari database XAMPP
    df = load_data()

    # 2. Mendefinisikan perhitungan metrik (REVISI DISINI)
    total_sampling = len(df)

    # Mencari teks yang sama persis dengan yang ada di tabel phpMyAdmin Anda
    ms_count = len(df[df['hasil_uji'] == 'Memenuhi Syarat'])
    tms_count = len(df[df['hasil_uji'] == 'Tidak Memenuhi Syarat'])

    # 3. Menampilkan metrik ke Dashboard
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sampling", total_sampling)
    col2.metric("Memenuhi Syarat (MS)", ms_count)
    col3.metric("Tidak Memenuhi Syarat (TMS)", tms_count)

    # Tabel Data
    st.subheader("📋 Data Hasil Pengawasan Terkini")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan database staging di XAMPP sudah ada. Error: {e}")