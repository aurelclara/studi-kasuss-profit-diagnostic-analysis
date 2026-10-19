import pandas as pd
import numpy as np


def generate_retail_data():
    """Mensimulasikan data transaksi ritel/manufaktur dengan anomali laba"""
    np.random.seed(123)
    n_records = 2000

    categories = ['Elektronik', 'Furnitur', 'Alat Kantor', 'Pakaian']
    regions = ['Jawa', 'Sumatera', 'Kalimantan', 'Sulawesi']

    data = {
        'TransactionID': range(10001, 10001 + n_records),
        'Category': np.random.choice(categories, size=n_records, p=[0.3, 0.2, 0.3, 0.2]),
        'Region': np.random.choice(regions, size=n_records),
        'SalesAmount': np.random.uniform(500000, 15000000, size=n_records),
        'DiscountRate': np.random.choice(
            [0.0, 0.05, 0.10, 0.25, 0.40], size=n_records, p=[0.4, 0.3, 0.15, 0.1, 0.05]
        ),
    }

    df = pd.DataFrame(data)

    # Asumsi HPP dasar adalah 60% dari SalesAmount
    df['COGS'] = df['SalesAmount'] * 0.60

    # Biaya pengiriman dan operasional tambahan
    df['OperationalCost'] = df['SalesAmount'] * np.random.uniform(0.10, 0.35, size=n_records)

    # Menghitung Laba Bersih (Net Profit) setelah diskon, HPP, dan biaya operasional
    # Diskon yang terlalu besar (misal 40%) menggerus habis profit
    df['EffectiveSales'] = df['SalesAmount'] * (1 - df['DiscountRate'])
    df['NetProfit'] = df['EffectiveSales'] - df['COGS'] - df['OperationalCost']
    df['ProfitMargin'] = df['NetProfit'] / df['EffectiveSales']

    return df


def main():
    print("=== TAHAP 1: Data Understanding & Preparation ===")
    df = generate_retail_data()
    print(f"Total Transaksi Tercatat: {len(df)}")
    print(f"Total Pendapatan Kotor: Rp {df['SalesAmount'].sum():,.2f}")
    print(f"Total Laba Bersih Perusahaan: Rp {df['NetProfit'].sum():,.2f}\n")

    print("=== TAHAP 2: Analisis Diagnostik (Mencari Akar Masalah Penurunan Laba) ===")
    # Menganalisis performa berdasarkan Kategori Produk
    diagnostic_category = df.groupby('Category').agg(
        TotalSales=('SalesAmount', 'sum'),
        TotalNetProfit=('NetProfit', 'sum'),
        AvgDiscount=('DiscountRate', 'mean'),
        AvgMargin=('ProfitMargin', 'mean'),
    ).reset_index()

    print("Performa Berdasarkan Kategori Produk:")
    print(diagnostic_category.to_string(index=False))
    print("\n")

    # Menganalisis performa berdasarkan Wilayah
    diagnostic_region = df.groupby('Region').agg(
        TotalSales=('SalesAmount', 'sum'),
        TotalNetProfit=('NetProfit', 'sum'),
        AvgDiscount=('DiscountRate', 'mean'),
    ).reset_index()

    print("Performa Berdasarkan Wilayah:")
    print(diagnostic_region.to_string(index=False))
    print("\n")

    print("=== TAHAP 3: Analisis Preskriptif (Rekomendasi Tindakan Manajemen) ===")
    # Menemukan kategori dengan laba bersih terendah
    problematic_category = diagnostic_category.loc[diagnostic_category['TotalNetProfit'].idxmin()]
    print(f"[REKOMENDASI] Kategori bermasalah utama: '{problematic_category['Category']}'")
    print(
        f"-> Analisis: Kategori ini memiliki rata-rata diskon yang tinggi "
        f"({problematic_category['AvgDiscount'] * 100:.1f}%) yang menyebabkan kontribusi "
        f"laba bersih paling kecil/negatif meskipun penjualannya tinggi."
    )
    print(
        "-> Tindakan Manajemen (Preskriptif): Batasi pemberian diskon maksimal 10% "
        "pada kategori tersebut dan evaluasi ulang biaya operasional logistik wilayah terkait."
    )


if __name__ == "__main__":
    main()
