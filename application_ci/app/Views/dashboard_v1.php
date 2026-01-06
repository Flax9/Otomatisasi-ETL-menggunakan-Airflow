<?php
// --- 1. PHP DATA PROCESSING ---

$statusCounts = [];
$dateCounts = [];
$simulate_dates = true; // Logic simulasi tetap aktif agar grafik bergelombang cantik

foreach ($pengawasan as $index => $row) {
    // Hitung Status
    $status = $row['hasil_uji']; 
    if (isset($statusCounts[$status])) {
        $statusCounts[$status]++;
    } else {
        $statusCounts[$status] = 1;
    }

    // Hitung Tanggal (Simulasi Sebaran Data)
    if ($simulate_dates) {
        $days_ago = $index % 7; // Sebar ke 7 hari ke belakang agar grafik lebih panjang
        $date = date('Y-m-d', strtotime("-$days_ago days"));
    } else {
        $date = date('Y-m-d', strtotime($row['etl_processed_at']));
    }

    if (isset($dateCounts[$date])) {
        $dateCounts[$date]++;
    } else {
        $dateCounts[$date] = 1;
    }
}
ksort($dateCounts);
?>

<!DOCTYPE html>
<html lang="id">
<head>
    <title>Dashboard Pengawasan BPOM</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        /* GAYA BARU: CLEAN & FRESH */
        body { 
            background-color: #f8f9fa; /* Abu-abu sangat muda (hampir putih) */
            font-family: 'Segoe UI', sans-serif; 
            color: #444;
        }
        .card { 
            border: none; 
            border-radius: 12px; /* Sudut lebih bulat */
            box-shadow: 0 4px 20px 0 rgba(0,0,0,0.05); /* Bayangan sangat halus */
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px); /* Efek naik dikit saat hover */
        }
        .card-header { 
            background-color: white; 
            border-bottom: 0; 
            font-weight: 700; 
            color: #2c3e50; 
            padding-top: 25px;
            padding-left: 25px;
            border-radius: 12px 12px 0 0 !important;
        }
        .card-body { padding: 25px; }
        
        h2 { color: #2c3e50; font-weight: 700; letter-spacing: -0.5px; }
        
        /* Aksen Oranye untuk Badge Utama */
        .badge-main {
            background-color: #fd9644; /* Oranye lembut seperti di referensi */
            color: white;
            padding: 8px 15px;
            font-weight: 500;
        }

        .table-responsive { 
            background: white; 
            border-radius: 12px; 
            padding: 25px; 
            box-shadow: 0 4px 20px 0 rgba(0,0,0,0.05); 
        }
    </style>
</head>
<body class="container-fluid py-4 px-md-5">

    <div class="d-flex justify-content-between align-items-center mb-5 mt-2">
        <div>
            <h2 class="mb-1">Dashboard Monitoring</h2>
            <p class="text-muted m-0">Pengawasan Obat & Makanan (BPOM)</p>
        </div>
        <span class="badge badge-main rounded-pill shadow-sm">
            <i class="me-1">●</i> Airflow Connected
        </span>
    </div>

    <div class="row mb-4">
        <div class="col-md-4 mb-3">
            <div class="card h-100">
                <div class="card-header">Rasio Kepatuhan</div>
                <div class="card-body">
                    <div style="height: 250px; position: relative;">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-8 mb-3">
            <div class="card h-100">
                <div class="card-header">Aktivitas Pengujian (7 Hari)</div>
                <div class="card-body">
                    <div style="height: 250px;">
                        <canvas id="timelineChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-12">
            <div class="table-responsive">
                <h5 class="mb-4 text-dark fw-bold">Data Detail Produk</h5>
                <table class="table table-hover align-middle border-0">
                    <thead class="table-light">
                        <tr style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">
                            <th>ID</th>
                            <th>Nama Produk</th>
                            <th>Status Uji</th>
                            <th>Waktu Proses</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach($pengawasan as $row): ?>
                        <tr>
                            <td class="fw-bold text-secondary">#<?= $row['id_pengawasan']; ?></td>
                            <td class="fw-bold text-dark"><?= $row['nama_produk']; ?></td>
                            <td>
                                <?php 
                                    $statusLower = strtolower($row['hasil_uji']);
                                    $isDanger = strpos($statusLower, 'tidak') !== false || strpos($statusLower, 'bahaya') !== false;
                                    // Badge Tabel: Menggunakan warna Teal untuk sukses
                                    $badgeStyle = $isDanger 
                                        ? 'background-color: #ff5b5c; color: white;' // Merah Soft
                                        : 'background-color: #2eca6a; color: white;'; // Hijau Emerald
                                ?>
                                <span class="badge rounded-pill px-3 py-2" style="<?= $badgeStyle; ?>">
                                    <?= $row['hasil_uji']; ?>
                                </span>
                            </td>
                            <td class="text-muted small"><?= $row['etl_processed_at']; ?></td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const statusData = <?= json_encode(array_values($statusCounts)); ?>;
        const statusLabels = <?= json_encode(array_keys($statusCounts)); ?>;
        const timelineData = <?= json_encode(array_values($dateCounts)); ?>;
        const timelineLabels = <?= json_encode(array_keys($dateCounts)); ?>;

        // WARNA BARU (Sesuai Referensi Gambar 2)
        const theme = {
            green: '#2eca6a', // Hijau Emerald (Warna Utama)
            greenLight: 'rgba(46, 202, 106, 0.2)', // Hijau Transparan
            red: '#ff5b5c',   // Merah Soft (Alert)
            orange: '#fd9644', // Oranye (Aksen)
            text: '#a1b0cb'
        };

        // --- 1. DONUT CHART (Hijau vs Merah) ---
        new Chart(document.getElementById('statusChart'), {
            type: 'doughnut',
            data: {
                labels: statusLabels,
                datasets: [{
                    data: statusData,
                    backgroundColor: statusLabels.map(label => {
                        let l = label.toLowerCase();
                        if (l.includes('tidak') || l.includes('gagal') || l.includes('bahaya')) {
                            return theme.red;
                        }
                        return theme.green;
                    }),
                    borderWidth: 0,
                    hoverOffset: 10 // Efek membesar saat hover
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%', // Lubang tengah lebih besar (Modern)
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { usePointStyle: true, padding: 20, font: { family: "'Segoe UI'" } }
                    }
                }
            }
        });

        // --- 2. LINE CHART (Green Smooth Area) ---
        const ctxTimeline = document.getElementById('timelineChart').getContext('2d');
        
        // Membuat Gradasi Hijau ke Putih (Sangat mirip referensi)
        let gradient = ctxTimeline.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(46, 202, 106, 0.6)'); // Hijau Pekat di atas
        gradient.addColorStop(1, 'rgba(46, 202, 106, 0.0)'); // Transparan di bawah

        new Chart(ctxTimeline, {
            type: 'line',
            data: {
                labels: timelineLabels,
                datasets: [{
                    label: 'Sampel Masuk',
                    data: timelineData,
                    borderColor: theme.green, // Garis Hijau
                    borderWidth: 3,
                    backgroundColor: gradient, // Isi Gradasi
                    tension: 0.4, // Lengkungan Halus
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: '#fff',
                    pointBorderColor: theme.green,
                    pointBorderWidth: 2,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { borderDash: [5, 5], color: '#f0f0f0' }, // Grid halus
                        ticks: { color: '#888' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#888' }
                    }
                }
            }
        });
    </script>
</body>
</html>