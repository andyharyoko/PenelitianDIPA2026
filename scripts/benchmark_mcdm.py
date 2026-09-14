import json
import numpy as np
import pandas as pd

# 1. Kriteria & Matriks AHP
# Urutan: C1, C2, C3, C4, C5, C6, C7
criteria_meta = [
    {"code": "C1_Aksesibilitas", "name": "Aksesibilitas Jalan", "type": "benefit"},
    {"code": "C2_Kepadatan_Penduduk", "name": "Kepadatan Penduduk", "type": "benefit"},
    {"code": "C3_Infrastruktur", "name": "Ketersediaan Infrastruktur", "type": "benefit"},
    {"code": "C4_Kompetitor", "name": "Jumlah Kompetitor (OSM 1km)", "type": "cost"},
    {"code": "C5_Biaya_Sewa", "name": "Biaya Sewa Lahan/Tahun", "type": "cost"},
    {"code": "C6_Demografi_Usia_Produktif", "name": "Persentase Usia Produktif", "type": "benefit"},
    {"code": "C7_Kedekatan_POI", "name": "Kedekatan Fasilitas/POI (OSM 1km)", "type": "benefit"},
]

matrix_ahp = np.array([
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], # C1
    [2.0, 1.0, 2.0, 1.0, 1/2, 2.0, 1/2], # C2
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], # C3
    [2.0, 1.0, 2.0, 1.0, 1/2, 2.0, 1/2], # C4
    [3.0, 2.0, 3.0, 2.0, 1.0, 3.0, 1.0], # C5
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], # C6
    [3.0, 2.0, 3.0, 2.0, 1.0, 3.0, 1.0]  # C7
])

# Hitung bobot AHP (Eigenvector rata-rata baris matriks ternormalisasi kolom)
col_sum = matrix_ahp.sum(axis=0)
norm_matrix = matrix_ahp / col_sum
weights = norm_matrix.mean(axis=1)

Aw = matrix_ahp.dot(weights)
lambda_max = float((Aw / weights).mean())
n = len(weights)
CI = float((lambda_max - n) / (n - 1))
RI = 1.32 # Saaty index for n=7
CR = float(CI / RI)

print(f"--- AHP CONSISTENCY CALCULATION ---")
print(f"Lambda Max: {lambda_max:.5f}")
print(f"Consistency Index (CI): {CI:.5f}")
print(f"Random Index (RI n=7): {RI}")
print(f"Consistency Ratio (CR): {CR:.5f} ({CR*100:.3f}%) -> {'KONSISTEN (CR < 0.1)' if CR < 0.1 else 'TIDAK KONSISTEN'}")
print("Bobot Prioritas Kriteria:")
for meta, w in zip(criteria_meta, weights):
    print(f"  * {meta['code']} ({meta['name']}): {w:.4f} ({w*100:.2f}%)")

# Baca Data 200 Kandidat
df = pd.read_csv('/home/andy/VibeCoding/ScrapingLokasi/webapp/data/kandidat_200.csv')
cols = [c['code'] for c in criteria_meta]
types = [c['type'] for c in criteria_meta]

# --- METODE SAW ---
df_saw_norm = df.copy()
for i, col in enumerate(cols):
    if types[i] == 'benefit':
        df_saw_norm[col] = df[col] / df[col].max()
    else:
        df_saw_norm[col] = df[col].min() / df[col]

df['Skor_SAW'] = 0.0
for i, col in enumerate(cols):
    df['Skor_SAW'] += df_saw_norm[col] * weights[i]

df['Rank_SAW'] = df['Skor_SAW'].rank(ascending=False, method='min').astype(int)

# --- METODE TOPSIS ---
df_topsis_norm = pd.DataFrame()
for i, col in enumerate(cols):
    denom = np.sqrt((df[col]**2).sum())
    df_topsis_norm[col] = (df[col] / denom) * weights[i]

A_pos = []
A_neg = []
for i, col in enumerate(cols):
    if types[i] == 'benefit':
        A_pos.append(df_topsis_norm[col].max())
        A_neg.append(df_topsis_norm[col].min())
    else:
        A_pos.append(df_topsis_norm[col].min())
        A_neg.append(df_topsis_norm[col].max())

D_pos = np.sqrt(((df_topsis_norm - A_pos)**2).sum(axis=1))
D_neg = np.sqrt(((df_topsis_norm - A_neg)**2).sum(axis=1))
df['Skor_TOPSIS'] = D_neg / (D_pos + D_neg)
df['Rank_TOPSIS'] = df['Skor_TOPSIS'].rank(ascending=False, method='min').astype(int)

# --- METODE WP (WEIGHTED PRODUCT) ---
# Bobot dipastikan totalnya 1: w_wp = weights / sum(weights)
w_wp = weights / weights.sum()
wp_powers = []
for i, t in enumerate(types):
    if t == 'benefit':
        wp_powers.append(w_wp[i])
    else:
        wp_powers.append(-w_wp[i])

# Vektor S
S = np.ones(len(df))
for i, col in enumerate(cols):
    S = S * (df[col].values.astype(float) ** wp_powers[i])

df['Vektor_S_WP'] = S
df['Skor_WP'] = S / S.sum()
df['Rank_WP'] = df['Skor_WP'].rank(ascending=False, method='min').astype(int)

# Tampilkan Top 10 masing-masing
print("\n--- TOP 10 SAW ---")
print(df.sort_values('Rank_SAW')[['Rank_SAW', 'Kode_Lokasi', 'Nama_Lokasi', 'Skor_SAW', 'Rank_TOPSIS', 'Rank_WP']].head(10).to_string(index=False))

print("\n--- TOP 10 TOPSIS ---")
print(df.sort_values('Rank_TOPSIS')[['Rank_TOPSIS', 'Kode_Lokasi', 'Nama_Lokasi', 'Skor_TOPSIS', 'Rank_SAW', 'Rank_WP']].head(10).to_string(index=False))

print("\n--- TOP 10 WP ---")
print(df.sort_values('Rank_WP')[['Rank_WP', 'Kode_Lokasi', 'Nama_Lokasi', 'Skor_WP', 'Rank_SAW', 'Rank_TOPSIS']].head(10).to_string(index=False))

# Hitung korelasi ranking Spearman
corr_spearman = df[['Rank_SAW', 'Rank_TOPSIS', 'Rank_WP']].corr(method='spearman')
print("\n--- KORELASI SPEARMAN PERINGKAT ---")
print(corr_spearman)

# Simpan hasil gabungan ke webapp/data/hasil_mcdm_lengkap.csv
df.to_csv('/home/andy/VibeCoding/ScrapingLokasi/webapp/data/hasil_mcdm_lengkap.csv', index=False)
print("\nHasil benchmark tersimpan di webapp/data/hasil_mcdm_lengkap.csv")
