import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Konfigurasi style untuk publikasi
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

# Load Data
df_saw = pd.read_csv('hasil_ranking_saw.csv').sort_values('Skor_Akhir', ascending=False).reset_index(drop=True)
df_saw['Peringkat_SAW'] = df_saw.index + 1

df_ahp = pd.read_csv('hasil_ranking_ahp_topsis.csv').sort_values('Skor_TOPSIS', ascending=False).reset_index(drop=True)
df_ahp['Peringkat_TOPSIS'] = df_ahp.index + 1

# Merge Data untuk Tabel Perbandingan
df_merge = pd.merge(df_saw[['Kode_Lokasi', 'Nama_Lokasi', 'Skor_Akhir', 'Peringkat_SAW']], 
                    df_ahp[['Kode_Lokasi', 'Skor_TOPSIS', 'Peringkat_TOPSIS']], 
                    on='Kode_Lokasi')

# Hitung Perubahan Peringkat (Positif = Naik Peringkat di TOPSIS, Negatif = Turun)
df_merge['Perubahan_Peringkat'] = df_merge['Peringkat_SAW'] - df_merge['Peringkat_TOPSIS']

# Ambil Top 15 dari salah satu metode untuk visualisasi Slopegraph
top_15_saw = df_merge[df_merge['Peringkat_SAW'] <= 15]
top_15_ahp = df_merge[df_merge['Peringkat_TOPSIS'] <= 15]
top_candidates = pd.concat([top_15_saw, top_15_ahp]).drop_duplicates(subset=['Kode_Lokasi']).sort_values('Peringkat_SAW')

# 1. Simpan Tabel Perbandingan lengkap
df_merge.sort_values('Peringkat_SAW').to_csv('Tabel_Perbandingan_Metode_Lengkap.csv', index=False)

# Simpan Tabel Perbandingan Top 15 ke format teks agar bisa dibaca AI untuk referensi markdown
top_candidates.sort_values('Peringkat_SAW').to_csv('Tabel_Top15_Perbandingan.csv', index=False)

# ==============================================================================
# 2. Membuat Visualisasi Perubahan Peringkat (Slopegraph / Bump Chart)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 12))

for idx, row in top_candidates.iterrows():
    # Tentukan warna: hijau jika naik peringkat (TOPSIS < SAW), merah jika turun, abu-abu jika tetap
    if row['Perubahan_Peringkat'] > 0:
        color = '#2ca02c' # Hijau (Naik)
    elif row['Perubahan_Peringkat'] < 0:
        color = '#d62728' # Merah (Turun)
    else:
        color = '#7f7f7f' # Abu-abu (Tetap)
        
    ax.plot([1, 2], [row['Peringkat_SAW'], row['Peringkat_TOPSIS']], 
            marker='o', markersize=8, linewidth=2.5, color=color, alpha=0.8)
    
    # Label kiri (SAW)
    ax.text(0.95, row['Peringkat_SAW'], f"{row['Nama_Lokasi']} (Rank {row['Peringkat_SAW']})", 
            ha='right', va='center', fontsize=11)
    
    # Label kanan (TOPSIS)
    ax.text(2.05, row['Peringkat_TOPSIS'], f"(Rank {row['Peringkat_TOPSIS']}) {row['Nama_Lokasi']}", 
            ha='left', va='center', fontsize=11)

ax.set_xlim(0.3, 2.7)
ax.set_xticks([1, 2])
ax.set_xticklabels(['Metode SAW', 'Metode AHP-TOPSIS'], fontsize=14, fontweight='bold')
ax.invert_yaxis()
ax.set_ylabel('Peringkat', fontsize=14, fontweight='bold')
ax.set_title('Perbandingan Peringkat Kandidat Lokasi Terbaik (Top 15)', pad=25, fontsize=16, fontweight='bold')

# Hapus garis-garis yang tidak perlu agar bersih
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='y', which='both', left=False, labelleft=False)
ax.tick_params(axis='x', which='both', bottom=False)

# Tambahkan legenda manual
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='#2ca02c', lw=2.5, marker='o', label='Peringkat Naik di AHP-TOPSIS'),
                   Line2D([0], [0], color='#7f7f7f', lw=2.5, marker='o', label='Peringkat Tetap'),
                   Line2D([0], [0], color='#d62728', lw=2.5, marker='o', label='Peringkat Turun di AHP-TOPSIS')]
ax.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('Visualisasi_4_Perubahan_Peringkat.png', dpi=300)
plt.close()

# ==============================================================================
# 3. Visualisasi Scatter Plot Korelasi Skor Keseluruhan
# ==============================================================================
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df_merge, x='Skor_Akhir', y='Skor_TOPSIS', alpha=0.7, color='#1f77b4', edgecolor='black', s=60)

# Tambahkan garis tren (regresi linier)
sns.regplot(data=df_merge, x='Skor_Akhir', y='Skor_TOPSIS', scatter=False, ax=ax2, color='#d62728', line_kws={'linestyle':'--'})

ax2.set_title('Korelasi Skor Keseluruhan: SAW vs AHP-TOPSIS', pad=15, fontweight='bold')
ax2.set_xlabel('Skor Akhir (SAW)')
ax2.set_ylabel('Skor Preferensi (AHP-TOPSIS)')
ax2.grid(True, linestyle='--', alpha=0.7)

# Anotasi korelasi Pearson
corr = df_merge['Skor_Akhir'].corr(df_merge['Skor_TOPSIS'])
ax2.text(0.05, 0.95, f'Korelasi Pearson: {corr:.3f}', transform=ax2.transAxes, 
         fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('Visualisasi_5_Korelasi_Metode.png', dpi=300)
plt.close()

print("Selesai membuat tabel perbandingan dan visualisasi komparatif.")
