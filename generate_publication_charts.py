import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Konfigurasi standar untuk publikasi jurnal
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'], # Standar font untuk jurnal ilmiah
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.dpi': 300,        # Resolusi tinggi 300 DPI standar cetak
    'savefig.dpi': 300,       
    'savefig.bbox': 'tight',  # Mencegah ada bagian gambar yang terpotong
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold'
})

# Membaca data dari hasil pemodelan sebelumnya
df_saw = pd.read_csv('hasil_ranking_saw.csv').sort_values('Skor_Akhir', ascending=False)
df_ahp = pd.read_csv('hasil_ranking_ahp_topsis.csv').sort_values('Skor_TOPSIS', ascending=False)

top10_saw = df_saw.head(10)
top10_ahp = df_ahp.head(10)

# ==============================================================================
# Visualisasi 1: Perbandingan Skor 10 Kandidat Terbaik (SAW vs AHP-TOPSIS)
# Dalam 1 gambar (file) terdapat 2 visualisasi (a) dan (b)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Subplot (a) - Hasil SAW
sns.barplot(data=top10_saw, x='Skor_Akhir', y='Nama_Lokasi', ax=axes[0], color='#4C72B0', edgecolor='black', linewidth=1.2)
axes[0].set_title('(a) Top 10 Candidate Locations based on SAW Score', pad=15)
axes[0].set_xlabel('SAW Score')
axes[0].set_ylabel('Location Name')
axes[0].set_xlim(0, top10_saw['Skor_Akhir'].max() * 1.15)
axes[0].grid(axis='x', linestyle='--', alpha=0.7)

# Menambahkan label nilai tepat di sebelah bar agar mudah dibaca
for i, p in enumerate(axes[0].patches):
    axes[0].annotate(f"{p.get_width():.3f}", 
                     (p.get_width() + 0.01, p.get_y() + p.get_height() / 2.), 
                     ha='left', va='center', fontsize=11, fontweight='bold')

# Subplot (b) - Hasil AHP-TOPSIS
sns.barplot(data=top10_ahp, x='Skor_TOPSIS', y='Nama_Lokasi', ax=axes[1], color='#DD8452', edgecolor='black', linewidth=1.2)
axes[1].set_title('(b) Top 10 Candidate Locations based on AHP-TOPSIS Score', pad=15)
axes[1].set_xlabel('TOPSIS Score')
axes[1].set_ylabel('') # Hilangkan ylabel karena sudah jelas
axes[1].set_xlim(0, top10_ahp['Skor_TOPSIS'].max() * 1.15)
axes[1].grid(axis='x', linestyle='--', alpha=0.7)

for i, p in enumerate(axes[1].patches):
    axes[1].annotate(f"{p.get_width():.3f}", 
                     (p.get_width() + 0.01, p.get_y() + p.get_height() / 2.), 
                     ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualisasi_1_Perbandingan_Metode.png', dpi=300)
plt.close()

# ==============================================================================
# Visualisasi 2: Analisis Kriteria Spesifik pada 5 Kandidat Terbaik
# Dalam 1 gambar (file) terdapat 2 visualisasi (a) dan (b)
# ==============================================================================
top5_saw = df_saw.head(5).copy()

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))

# Subplot (a) - Aksesibilitas (C1)
sns.barplot(data=top5_saw, x='Nama_Lokasi', y='C1_Aksesibilitas', ax=axes2[0], color='#55A868', edgecolor='black', linewidth=1.2)
axes2[0].set_title('(a) Accessibility Score (C1) for Top 5 Candidates', pad=15)
axes2[0].set_xlabel('Location Name')
axes2[0].set_ylabel('Accessibility Score (1-10)')
axes2[0].set_ylim(0, 12)
axes2[0].grid(axis='y', linestyle='--', alpha=0.7)
# Memutar teks sumbu x agar tidak bertumpuk
axes2[0].tick_params(axis='x', rotation=15)

for p in axes2[0].patches:
    axes2[0].annotate(f"{int(p.get_height())}", 
                      (p.get_x() + p.get_width() / 2., p.get_height() + 0.3), 
                      ha='center', va='bottom', fontsize=11, fontweight='bold')

# Subplot (b) - Kedekatan POI (C7)
sns.barplot(data=top5_saw, x='Nama_Lokasi', y='C7_Kedekatan_POI', ax=axes2[1], color='#C44E52', edgecolor='black', linewidth=1.2)
axes2[1].set_title('(b) Proximity to POI (C7) for Top 5 Candidates', pad=15)
axes2[1].set_xlabel('Location Name')
axes2[1].set_ylabel('Number of Nearby POIs')
axes2[1].set_ylim(0, top5_saw['C7_Kedekatan_POI'].max() * 1.2)
axes2[1].grid(axis='y', linestyle='--', alpha=0.7)
axes2[1].tick_params(axis='x', rotation=15)

for p in axes2[1].patches:
    axes2[1].annotate(f"{int(p.get_height())}", 
                      (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), 
                      ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualisasi_2_Analisis_Kriteria.png', dpi=300)
plt.close()

# ==============================================================================
# Visualisasi 3: Scatter Plot Distribusi Biaya Sewa vs Kedekatan POI
# ==============================================================================
fig3, ax3 = plt.subplots(figsize=(8, 6))

sns.scatterplot(data=df_saw, x='C5_Biaya_Sewa', y='C7_Kedekatan_POI', 
                size='Skor_Akhir', sizes=(20, 200), hue='Skor_Akhir', palette='viridis', 
                alpha=0.8, edgecolor='black', ax=ax3)

ax3.set_title('Scatter Plot: Rental Cost vs Proximity to POI', pad=15)
ax3.set_xlabel('Rental Cost (C5)')
ax3.set_ylabel('Proximity to POI (C7)')
ax3.grid(True, linestyle='--', alpha=0.7)

# Anotasi 3 kandidat terbaik agar menonjol
for i, row in top5_saw.head(3).iterrows():
    ax3.annotate(row['Nama_Lokasi'], 
                 (row['C5_Biaya_Sewa'], row['C7_Kedekatan_POI']),
                 xytext=(5, 5), textcoords='offset points', 
                 fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('Visualisasi_3_Scatter_Cost_vs_POI.png', dpi=300)
plt.close()

print("File visualisasi standar publikasi berhasil dibuat dengan resolusi tinggi (300 DPI).")
