import mysql.connector
import random
from datetime import datetime, timedelta

# Koneksi ke Database Docker/Local kamu
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_monitoring_bpom"
)
cursor = db.cursor()

def generate_dummy_data(n=100):
    perusahaan = ["PT. Farmasi Jaya", "CV. Kosmetik Alam", "PT. Pangan Sejahtera", "Lestari Herbal"]
    kategori = [1, 2, 3, 4]

    for _ in range(n):
        # Generate Produk
        nie = f"N{random.choice(['A','B','D'])}{random.randint(100000, 999999)}"
        nama = f"Produk Gen-{random.randint(1, 1000)}"
        pt = random.choice(perusahaan)
        kat = random.choice(kategori)
        tgl = (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime('%Y-%m-%d')

        cursor.execute("""
            INSERT INTO produk_registrasi (nomor_izin_edar, nama_produk, nama_perusahaan, id_kategori, tanggal_terbit, status_registrasi)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nie, nama, pt, kat, tgl, 'Aktif'))

        # Simulasi Post-Market: 30% produk punya histori pengawasan
        if random.random() < 0.3:
            id_produk = cursor.lastrowid
            hasil = random.choice(['Memenuhi Syarat', 'Tidak Memenuhi Syarat'])
            lokasi = random.choice(['Jakarta', 'Surabaya', 'Medan', 'Makassar'])
            tindak = "N/A" if hasil == 'Memenuhi Syarat' else "Penarikan Produk"

            cursor.execute("""
                INSERT INTO pengawasan_lapangan (id_produk, tanggal_sampling, lokasi_sampling, hasil_uji, tindak_lanjut)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_produk, datetime.now().strftime('%Y-%m-%d'), lokasi, hasil, tindak))

    db.commit()
    print(f"Berhasil memasukkan {n} data dummy!")

generate_dummy_data(200) # Ganti angka ini untuk jumlah data lebih besar