import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Konfigurasi style untuk publikasi (300 DPI, font serif)
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold'
})

# 1. BACA DATA HASIL PARETO
df_saw = pd.read_csv('hasil_saw_pareto.csv').sort_values('Skor_SAW', ascending=False).reset_index(drop=True)
df_saw['Peringkat_SAW'] = df_saw.index + 1

df_topsis = pd.read_csv('hasil_ahp_topsis_pareto.csv').sort_values('Skor_TOPSIS', ascending=False).reset_index(drop=True)
df_topsis['Peringkat_TOPSIS'] = df_topsis.index + 1

top10_saw = df_saw.head(10)
top10_topsis = df_topsis.head(10)

# =========================================================
# Visualisasi 1: Bar Chart Perbandingan Top 10 (Pareto)
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(data=top10_saw, x='Skor_SAW', y='Nama_Lokasi', ax=axes[0], color='#4C72B0', edgecolor='black', linewidth=1.2)
axes[0].set_title('(a) Top 10 Pareto Candidates - SAW', pad=15)
axes[0].set_xlabel('SAW Score')
axes[0].set_ylabel('Location Name')
axes[0].set_xlim(0, top10_saw['Skor_SAW'].max() * 1.15)
axes[0].grid(axis='x', linestyle='--', alpha=0.7)
for p in axes[0].patches:
    axes[0].annotate(f"{p.get_width():.3f}", (p.get_width() + 0.01, p.get_y() + p.get_height() / 2.), ha='left', va='center', fontsize=11, fontweight='bold')

sns.barplot(data=top10_topsis, x='Skor_TOPSIS', y='Nama_Lokasi', ax=axes[1], color='#DD8452', edgecolor='black', linewidth=1.2)
axes[1].set_title('(b) Top 10 Pareto Candidates - AHP-TOPSIS', pad=15)
axes[1].set_xlabel('TOPSIS Score')
axes[1].set_ylabel('')
axes[1].set_xlim(0, top10_topsis['Skor_TOPSIS'].max() * 1.15)
axes[1].grid(axis='x', linestyle='--', alpha=0.7)
for p in axes[1].patches:
    axes[1].annotate(f"{p.get_width():.3f}", (p.get_width() + 0.01, p.get_y() + p.get_height() / 2.), ha='left', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualisasi_1_Perbandingan_Metode_Pareto.png', dpi=300)
plt.close()

# =========================================================
# Visualisasi 2: Analisis Kriteria Top 5 (Pareto)
# =========================================================
top5_saw = df_saw.head(5).copy()
fig2, axes2 = plt.subplots(1, 2, figsize=(14, 6))

sns.barplot(data=top5_saw, x='Nama_Lokasi', y='C1_Aksesibilitas', ax=axes2[0], color='#55A868', edgecolor='black', linewidth=1.2)
axes2[0].set_title('(a) Accessibility Score (C1) for Top 5 Pareto Candidates', pad=15)
axes2[0].set_xlabel('Location Name')
axes2[0].set_ylabel('Accessibility Score (1-10)')
axes2[0].set_ylim(0, 12)
axes2[0].grid(axis='y', linestyle='--', alpha=0.7)
axes2[0].tick_params(axis='x', rotation=15)
for p in axes2[0].patches:
    axes2[0].annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height() + 0.3), ha='center', va='bottom', fontsize=11, fontweight='bold')

sns.barplot(data=top5_saw, x='Nama_Lokasi', y='C7_Kedekatan_POI', ax=axes2[1], color='#C44E52', edgecolor='black', linewidth=1.2)
axes2[1].set_title('(b) Proximity to POI (C7) for Top 5 Pareto Candidates', pad=15)
axes2[1].set_xlabel('Location Name')
axes2[1].set_ylabel('Number of Nearby POIs')
axes2[1].set_ylim(0, top5_saw['C7_Kedekatan_POI'].max() * 1.2)
axes2[1].grid(axis='y', linestyle='--', alpha=0.7)
axes2[1].tick_params(axis='x', rotation=15)
for p in axes2[1].patches:
    axes2[1].annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2., p.get_height() + 1.5), ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Visualisasi_2_Analisis_Kriteria_Pareto.png', dpi=300)
plt.close()

# =========================================================
# Visualisasi 3: Scatter Plot Cost vs POI (Pareto)
# =========================================================
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df_saw, x='C5_Biaya_Sewa', y='C7_Kedekatan_POI', size='Skor_SAW', sizes=(20, 200), hue='Skor_SAW', palette='viridis', alpha=0.8, edgecolor='black', ax=ax3)
ax3.set_title('Pareto Filtered Candidates: Rental Cost vs Proximity to POI', pad=15)
ax3.set_xlabel('Rental Cost (C5)')
ax3.set_ylabel('Proximity to POI (C7)')
ax3.grid(True, linestyle='--', alpha=0.7)
for i, row in top5_saw.head(3).iterrows():
    ax3.annotate(row['Nama_Lokasi'], (row['C5_Biaya_Sewa'], row['C7_Kedekatan_POI']), xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
plt.tight_layout()
plt.savefig('Visualisasi_3_Scatter_Cost_vs_POI_Pareto.png', dpi=300)
plt.close()

# =========================================================
# Menghitung Perubahan Peringkat dan Menyimpan Tabel
# =========================================================
df_merge = pd.merge(df_saw[['Kode_Lokasi', 'Nama_Lokasi', 'Skor_SAW', 'Peringkat_SAW']], 
                    df_topsis[['Kode_Lokasi', 'Skor_TOPSIS', 'Peringkat_TOPSIS']], 
                    on='Kode_Lokasi')
df_merge['Perubahan_Peringkat'] = df_merge['Peringkat_SAW'] - df_merge['Peringkat_TOPSIS']

# Ambil Top 15 untuk divisualisasikan
top_15_saw = df_merge[df_merge['Peringkat_SAW'] <= 15]
top_15_topsis = df_merge[df_merge['Peringkat_TOPSIS'] <= 15]
top_candidates = pd.concat([top_15_saw, top_15_topsis]).drop_duplicates(subset=['Kode_Lokasi']).sort_values('Peringkat_SAW')

# Simpan CSV
top_candidates.to_csv('Tabel_Top15_Perbandingan_Pareto.csv', index=False)

# =========================================================
# Visualisasi 4: Slopegraph Perubahan Peringkat (Pareto)
# =========================================================
fig4, ax4 = plt.subplots(figsize=(10, 12))
for idx, row in top_candidates.iterrows():
    if row['Perubahan_Peringkat'] > 0: color = '#2ca02c'
    elif row['Perubahan_Peringkat'] < 0: color = '#d62728'
    else: color = '#7f7f7f'
    ax4.plot([1, 2], [row['Peringkat_SAW'], row['Peringkat_TOPSIS']], marker='o', markersize=8, linewidth=2.5, color=color, alpha=0.8)
    ax4.text(0.95, row['Peringkat_SAW'], f"{row['Nama_Lokasi']} (Rank {row['Peringkat_SAW']})", ha='right', va='center', fontsize=11)
    ax4.text(2.05, row['Peringkat_TOPSIS'], f"(Rank {row['Peringkat_TOPSIS']}) {row['Nama_Lokasi']}", ha='left', va='center', fontsize=11)

ax4.set_xlim(0.3, 2.7)
ax4.set_xticks([1, 2])
ax4.set_xticklabels(['Metode SAW (Pareto)', 'Metode AHP-TOPSIS (Pareto)'], fontsize=14, fontweight='bold')
ax4.invert_yaxis()
ax4.set_ylabel('Peringkat', fontsize=14, fontweight='bold')
ax4.set_title('Perbandingan Peringkat Top 15 (Setelah Filter Pareto)', pad=25, fontsize=16, fontweight='bold')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_visible(False)
ax4.spines['bottom'].set_visible(False)
ax4.tick_params(axis='y', which='both', left=False, labelleft=False)
ax4.tick_params(axis='x', which='both', bottom=False)

from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='#2ca02c', lw=2.5, marker='o', label='Naik di AHP-TOPSIS'),
                   Line2D([0], [0], color='#7f7f7f', lw=2.5, marker='o', label='Tetap'),
                   Line2D([0], [0], color='#d62728', lw=2.5, marker='o', label='Turun di AHP-TOPSIS')]
ax4.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('Visualisasi_4_Perubahan_Peringkat_Pareto.png', dpi=300)
plt.close()

# =========================================================
# Visualisasi 5: Scatter Plot Korelasi Keseluruhan (Pareto)
# =========================================================
fig5, ax5 = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df_merge, x='Skor_SAW', y='Skor_TOPSIS', alpha=0.7, color='#1f77b4', edgecolor='black', s=60)
sns.regplot(data=df_merge, x='Skor_SAW', y='Skor_TOPSIS', scatter=False, ax=ax5, color='#d62728', line_kws={'linestyle':'--'})
ax5.set_title('Korelasi Skor Kandidat Pareto: SAW vs AHP-TOPSIS', pad=15, fontweight='bold')
ax5.set_xlabel('Skor SAW')
ax5.set_ylabel('Skor AHP-TOPSIS')
ax5.grid(True, linestyle='--', alpha=0.7)
corr = df_merge['Skor_SAW'].corr(df_merge['Skor_TOPSIS'])
ax5.text(0.05, 0.95, f'Korelasi Pearson: {corr:.3f}', transform=ax5.transAxes, fontsize=12, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('Visualisasi_5_Korelasi_Metode_Pareto.png', dpi=300)
plt.close()

print("Selesai membuat semua visualisasi dan tabel untuk hasil Pareto.")
