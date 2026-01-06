from airflow.providers.mysql.hooks.mysql import MySqlHook
import pandas as pd

def run_etl_process():
    # Inisialisasi Hook
    src_hook = MySqlHook(mysql_conn_id='mysql_source')
    dest_hook = MySqlHook(mysql_conn_id='mysql_staging')

    # --- EXTRACT ---
    query_extract = """
    SELECT p.id_pengawasan, r.nama_produk, r.nomor_izin_edar,
           k.nama_kategori, p.tanggal_sampling, p.lokasi_sampling,
           p.hasil_uji, p.tindak_lanjut
    FROM db_monitoring_bpom.pengawasan_lapangan p
    JOIN db_monitoring_bpom.produk_registrasi r ON p.id_produk = r.id_produk
    JOIN db_monitoring_bpom.kategori_produk k ON r.id_kategori = k.id_kategori
    """
    df = src_hook.get_pandas_df(query_extract)

    # --- TRANSFORM ---
    # Logika pembersihan data dipusatkan di sini
    df['tindak_lanjut'] = df['tindak_lanjut'].fillna('Menunggu Evaluasi')
    df['hasil_uji'] = df['hasil_uji'].str.strip()

    # --- LOAD ---
    dest_hook.run("TRUNCATE TABLE db_dashboard_bpom_staging.stg_pengawasan_dashboard")
    dest_hook.insert_rows(
        table='db_dashboard_bpom_staging.stg_pengawasan_dashboard',
        rows=df.values.tolist(),
        target_fields=df.columns.tolist(),
        replace=True
    )
    return f"Sukses memproses {len(df)} baris."