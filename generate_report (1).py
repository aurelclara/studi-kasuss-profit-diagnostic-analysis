"""Membuat laporan HTML (index.html) dari hasil analisis diagnostik.

Jalankan:  python generate_report.py
Lalu buka index.html dengan double-click (atau lewat GitHub Pages).
"""
from html import escape

from diagnostic_analysis import generate_retail_data


def num(x, decimals=0):
    """Format angka gaya Indonesia: 1.234.567,89"""
    s = f"{x:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def rp(v):
    """Format rupiah ringkas: miliar / juta."""
    if abs(v) >= 1e9:
        return f"Rp {num(v / 1e9, 2)} miliar"
    return f"Rp {num(v / 1e6, 1)} juta"


def bar_chart(rows, label_key, value_key, caption):
    """Grafik batang horizontal murni HTML/CSS (tanpa library)."""
    max_v = max(abs(r[value_key]) for r in rows) or 1
    items = []
    for r in sorted(rows, key=lambda r: r[value_key]):
        width = abs(r[value_key]) / max_v * 100
        items.append(
            f'<div class="bar-row">'
            f'<div class="bar-label">{escape(str(r[label_key]))}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>'
            f'<div class="bar-value">{rp(r[value_key])}</div>'
            f"</div>"
        )
    return (
        f'<figure class="chart" role="img" aria-label="{escape(caption)}">'
        f'<figcaption>{escape(caption)}</figcaption>{"".join(items)}</figure>'
    )


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--text:#1a2230;--muted:#5d6878;--line:#e2e6ec;
--accent:#2563eb;--bad:#c2410c;--bad-bg:#fff4ed;--track:#e9edf3}
@media (prefers-color-scheme:dark){:root{--bg:#0f141b;--card:#18202b;--text:#e8ecf2;--muted:#9aa6b6;
--line:#2a3441;--accent:#6ea0ff;--bad:#ff9a6b;--bad-bg:#2a1d16;--track:#263040}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:960px;margin:0 auto;padding:32px 16px 56px}
h1{font-size:1.7rem;margin:0 0 4px}
h2{font-size:1.2rem;margin:36px 0 12px}
.sub{color:var(--muted);margin:0 0 24px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.kpi,.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.kpi span{display:block;color:var(--muted);font-size:.85rem}
.kpi strong{display:block;font-size:1.35rem;margin-top:4px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:16px}
@media (max-width:480px){.grid2{grid-template-columns:1fr}}
.chart{margin:0}
.chart figcaption{font-weight:600;margin-bottom:12px}
.bar-row{display:grid;grid-template-columns:96px 1fr 110px;gap:10px;align-items:center;margin:8px 0;font-size:.9rem}
.bar-track{background:var(--track);border-radius:6px;height:16px;overflow:hidden}
.bar-fill{background:var(--accent);height:100%;border-radius:6px}
.bar-value{text-align:right;font-variant-numeric:tabular-nums;color:var(--muted)}
.tablewrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.9rem}
th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
th{color:var(--muted);font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.rec{background:var(--bad-bg);border:1px solid var(--bad);border-radius:12px;padding:16px 20px}
.rec h2{margin-top:0;color:var(--bad)}
.rec li{margin:6px 0}
.note{color:var(--muted);font-size:.85rem;margin-top:32px}
"""


def build_html(df):
    total_sales = df["SalesAmount"].sum()
    total_profit = df["NetProfit"].sum()
    overall_margin = total_profit / df["EffectiveSales"].sum()

    cat = (
        df.groupby("Category")
        .agg(TotalSales=("SalesAmount", "sum"), TotalNetProfit=("NetProfit", "sum"),
             AvgDiscount=("DiscountRate", "mean"), AvgMargin=("ProfitMargin", "mean"))
        .reset_index()
    )
    reg = (
        df.groupby("Region")
        .agg(TotalSales=("SalesAmount", "sum"), TotalNetProfit=("NetProfit", "sum"),
             AvgDiscount=("DiscountRate", "mean"), AvgMargin=("ProfitMargin", "mean"))
        .reset_index()
    )
    cat_rows = cat.to_dict("records")
    reg_rows = reg.to_dict("records")

    worst = cat.loc[cat["TotalNetProfit"].idxmin()]
    top_discount = cat.loc[cat["AvgDiscount"].idxmax()]
    worst_region = reg.loc[reg["TotalNetProfit"].idxmin()]

    # Transaksi dengan diskon >= 25% vs lainnya
    heavy = df[df["DiscountRate"] >= 0.25]
    light = df[df["DiscountRate"] < 0.25]
    heavy_margin = heavy["NetProfit"].sum() / heavy["EffectiveSales"].sum()
    light_margin = light["NetProfit"].sum() / light["EffectiveSales"].sum()

    def cols(first):
        return [
            (first, first_key[first], lambda v: escape(str(v)), ""),
            ("Total penjualan", "TotalSales", rp, "n"),
            ("Laba bersih", "TotalNetProfit", rp, "n"),
            ("Rata-rata diskon", "AvgDiscount", lambda v: f"{num(v * 100, 1)}%", "n"),
            ("Rata-rata margin", "AvgMargin", lambda v: f"{num(v * 100, 1)}%", "n"),
        ]

    first_key = {"Kategori": "Category", "Wilayah": "Region"}

    def render_table(rows, first):
        c = cols(first)
        head = "".join(f'<th class="{cls}">{escape(h)}</th>' for h, _, _, cls in c)
        body = "".join(
            "<tr>" + "".join(f'<td class="{cls}">{fmt(r[key])}</td>' for _, key, fmt, cls in c) + "</tr>"
            for r in rows
        )
        return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    return f"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Laporan Analisis Diagnostik Laba Bersih</title>
<style>{CSS}</style>
</head>
<body>
<main>
<h1>Laporan Analisis Diagnostik &amp; Preskriptif</h1>
<p class="sub">Studi kasus PT Maju Bersama: pendapatan naik, laba bersih turun. Data simulasi {num(len(df))} transaksi.</p>

<section class="kpis" aria-label="Ringkasan">
<div class="kpi"><span>Total transaksi</span><strong>{num(len(df))}</strong></div>
<div class="kpi"><span>Pendapatan kotor</span><strong>{rp(total_sales)}</strong></div>
<div class="kpi"><span>Laba bersih</span><strong>{rp(total_profit)}</strong></div>
<div class="kpi"><span>Margin laba keseluruhan</span><strong>{num(overall_margin * 100, 1)}%</strong></div>
</section>

<h2>Diagnostik: di mana laba terkumpul?</h2>
<div class="grid2">
<div class="card">{bar_chart(cat_rows, "Category", "TotalNetProfit", "Laba bersih per kategori produk")}</div>
<div class="card">{bar_chart(reg_rows, "Region", "TotalNetProfit", "Laba bersih per wilayah")}</div>
</div>

<h2>Performa per kategori produk</h2>
<div class="card">{render_table(cat_rows, "Kategori")}</div>

<h2>Performa per wilayah</h2>
<div class="card">{render_table(reg_rows, "Wilayah")}</div>

<h2>Dampak diskon besar</h2>
<div class="card">
<p>Transaksi dengan diskon 25% ke atas ({num(len(heavy))} transaksi) memiliki margin laba
<strong>{num(heavy_margin * 100, 1)}%</strong>, dibandingkan <strong>{num(light_margin * 100, 1)}%</strong>
pada transaksi dengan diskon lebih kecil. Diskon besar menggerus margin karena HPP dan biaya operasional tetap sama.</p>
</div>

<section class="rec" style="margin-top:36px">
<h2>Rekomendasi tindakan manajemen (preskriptif)</h2>
<ul>
<li>Kategori dengan laba bersih terendah: <strong>{escape(str(worst["Category"]))}</strong>
({rp(worst["TotalNetProfit"])}, rata-rata margin {num(worst["AvgMargin"] * 100, 1)}%).</li>
<li>Rata-rata diskon tertinggi ada pada kategori <strong>{escape(str(top_discount["Category"]))}</strong>
({num(top_discount["AvgDiscount"] * 100, 1)}%).</li>
<li>Wilayah dengan laba bersih terendah: <strong>{escape(str(worst_region["Region"]))}</strong>
({rp(worst_region["TotalNetProfit"])}).</li>
<li>Batasi diskon maksimal 10% pada kategori bermasalah dan tinjau ulang diskon 25% ke atas.</li>
<li>Evaluasi biaya operasional dan logistik pada wilayah dengan laba terendah.</li>
</ul>
</section>

<p class="note">Catatan: data dibangkitkan secara acak (seed 123) dengan asumsi HPP 60% dan biaya operasional 10-35% dari penjualan.
Selisih antar kategori dan wilayah relatif kecil, jadi kesimpulan ini hanya ilustrasi metode. Ganti dengan data transaksi nyata untuk analisis sebenarnya.</p>
</main>
</body>
</html>
"""


def main():
    df = generate_retail_data()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(build_html(df))
    print("index.html berhasil dibuat. Buka dengan double-click di browser.")


if __name__ == "__main__":
    main()
