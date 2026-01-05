USE db_monitoring_bpom;

-- Melihat 10 produk terbaru yang terdaftar
SELECT * FROM produk_registrasi ORDER BY tanggal_terbit; --DESC LIMIT 10;

-- Melihat statistik: Berapa jumlah produk per kategori?
SELECT k.nama_kategori, COUNT(p.id_produk) as total_produk
FROM kategori_produk k
LEFT JOIN produk_registrasi p ON k.id_kategori = p.id_kategori
GROUP BY k.nama_kategori;

-- Melihat produk yang Tidak Memenuhi Syarat (dari tabel pengawasan)
SELECT p.nama_produk, p.nomor_izin_edar, l.hasil_uji, l.lokasi_sampling
FROM produk_registrasi p
JOIN pengawasan_lapangan l ON p.id_produk = l.id_produk
WHERE l.hasil_uji = 'Tidak Memenuhi Syarat';

-- Melihat total produk terdaftar
SELECT COUNT(*) as total_produk FROM produk_registrasi;

-- Melihat total data pengawasan lapangan
SELECT COUNT(*) as total_pengawasan FROM pengawasan_lapangan;

-- Melihat jumlah produk berdasarkan kategori
SELECT k.nama_kategori, COUNT(p.id_produk) as jumlah
FROM kategori_produk k
LEFT JOIN produk_registrasi p ON k.id_kategori = p.id_kategori
GROUP BY k.nama_kategori;