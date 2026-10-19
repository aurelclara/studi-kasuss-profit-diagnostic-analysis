# Profit Diagnostic Analysis

Studi kasus **Analisis Diagnostik & Preskriptif** untuk mendeteksi akar masalah penurunan laba bersih pada perusahaan ritel/manufaktur (kasus PT Maju Bersama): pendapatan naik, tetapi laba bersih justru turun.

Proyek ini menggunakan Python (pandas & numpy) untuk mendiagnosis produk atau wilayah mana yang menekan margin keuntungan, lalu memberikan rekomendasi tindakan (*prescriptive action*) bagi manajemen.

🔗 **[Lihat laporan HTML (live)](https://aurelclara.github.io/studi-kasuss-profit-diagnostic-analysis/)**

## Kerangka CRISP-DM

| Tahap | Penjelasan |
|---|---|
| **Business Understanding** | Pendapatan agregat naik, namun laba bersih turun. Manajemen butuh analisis diagnostik untuk menemukan anomali pada lini produk atau wilayah tertentu. |
| **Data Understanding & Preparation** | Menggabungkan data penjualan, HPP (COGS), diskon, dan biaya operasional/pengiriman untuk menghitung *Profit Margin* tiap transaksi. |
| **Modeling / Diagnostic Analysis** | Grouping & agregasi per kategori dan wilayah untuk menemukan segmen dengan volume tinggi tetapi margin rendah/negatif. |
| **Prescriptive Action** | Rekomendasi otomatis, misalnya membatasi diskon atau menaikkan harga jual. |

## Struktur Proyek

```
studi-kasus-profit-diagnostic-analysis/
├── diagnostic_analysis.py   # Skrip analisis utama (hasil di terminal)
├── generate_report.py       # Pembuat laporan HTML
├── index.html               # Laporan visual (buka di browser)
├── requirements.txt         # Dependensi
├── .gitignore
└── README.md
```

## Cara Menjalankan

```bash
git clone https://github.com/aurelclara/studi-kasus-profit-diagnostic-analysis.git
cd studi-kasus-profit-diagnostic-analysis

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python diagnostic_analysis.py    # analisis di terminal
python generate_report.py        # membuat ulang index.html
```

## Laporan HTML

`index.html` berisi ringkasan KPI, grafik laba bersih per kategori dan wilayah, tabel performa, dampak diskon besar, serta rekomendasi manajemen.

- **Membuka lokal:** double-click `index.html` (terbuka di browser, tidak perlu server).
- **Lewat link:** aktifkan GitHub Pages di **Settings → Pages**, pilih branch `main` dan folder `/ (root)`, lalu buka `https://aurelclara.github.io/studi-kasus-profit-diagnostic-analysis/`.

## Output

Skrip mencetak tiga bagian:

1. **Data Understanding**: jumlah transaksi, total pendapatan kotor, dan total laba bersih.
2. **Analisis Diagnostik**: performa per kategori produk dan per wilayah (total penjualan, laba bersih, rata-rata diskon, rata-rata margin).
3. **Analisis Preskriptif**: kategori bermasalah utama beserta rekomendasi tindakan manajemen.

## Catatan

Data yang digunakan adalah **simulasi** (`np.random.seed(123)`, 2.000 transaksi) dengan asumsi HPP 60% dari penjualan dan biaya operasional 10-35% dari penjualan. Untuk penggunaan nyata, ganti fungsi `generate_retail_data()` dengan data transaksi perusahaan.

## Lisensi
Kuliah tamu Informatics Practitioner Lecture Series 2026, Andria Arisal, BRIN.

Proyek ini dibuat untuk keperluan pembelajaran.
