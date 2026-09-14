import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Konfigurasi Figure
fig, ax = plt.subplots(figsize=(10, 12), dpi=300)
ax.axis('off')

# Warna yang profesional untuk jurnal
color_primary = '#2B475D'    # Biru Gelap
color_secondary = '#E85A4F'  # Merah Bata
color_tertiary = '#3AAFA9'   # Tosca
color_bg = '#F4F4F2'         # Putih Tulang

fig.patch.set_facecolor('white')

# Definisi koordinat Box (X, Y, Lebar, Tinggi, Teks, Warna)
boxes = {
    'Tahap1': (0.5, 0.90, 0.6, 0.08, "TAHAP 1: PENGUMPULAN DATA SPASIAL\nEkstraksi 100 Kandidat Lokasi dari OpenStreetMap", color_primary),
    
    'Tahap2': (0.5, 0.75, 0.6, 0.08, "TAHAP 2: PENYARINGAN (SCREENING)\nPareto Optimality (Membuang Kandidat Terdominasi)", color_tertiary),
    
    'Tahap3A': (0.3, 0.55, 0.35, 0.08, "TAHAP 3A: PEMERINGKATAN\nMetode SAW", color_secondary),
    'Tahap3B': (0.7, 0.55, 0.35, 0.08, "TAHAP 3B: PEMERINGKATAN\nMetode AHP-TOPSIS", color_secondary),
    
    'Tahap4': (0.5, 0.35, 0.6, 0.08, "TAHAP 4: OPTIMASI RUTE LAPANGAN\nTraveling Salesperson Problem (TSP) untuk Ground Truth", color_tertiary),
    
    'Tahap5': (0.5, 0.20, 0.6, 0.08, "TAHAP 5: VISUALISASI KEPUTUSAN\nDashboard WebGIS Interaktif Rekomendasi Lokasi", color_primary)
}

# Menggambar Box
for key, (x, y, w, h, text, color) in boxes.items():
    # Menghitung titik sudut kiri bawah kotak
    x0 = x - w/2
    y0 = y - h/2
    
    box = mpatches.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.03", 
                                  edgecolor='black', facecolor=color, linewidth=1.5)
    ax.add_patch(box)
    
    # Menambahkan Teks
    ax.text(x, y, text, ha='center', va='center', fontsize=11, color='white', 
            fontweight='bold', fontfamily='serif', linespacing=1.5)

# Definisi Panah (Start Key, End Key, Teks Penjelasan Panah)
arrows = [
    ('Tahap1', 'Tahap2', 'Menghasilkan 100 Data Mentah'),
    ('Tahap2', 'Tahap3A', '82 Kandidat Optimal'),
    ('Tahap2', 'Tahap3B', '82 Kandidat Optimal'),
    ('Tahap3A', 'Tahap4', 'Perbandingan\nRanking'),
    ('Tahap3B', 'Tahap4', ''),
    ('Tahap4', 'Tahap5', 'Integrasi Rute & Peringkat')
]

# Menggambar Panah
for start_key, end_key, arrow_text in arrows:
    start_pos = boxes[start_key]
    end_pos = boxes[end_key]
    
    # Koordinat x,y panah
    start_x = start_pos[0]
    start_y = start_pos[1] - start_pos[3]/2 - 0.03 # Keluar dari bawah box
    
    end_x = end_pos[0]
    end_y = end_pos[1] + end_pos[3]/2 + 0.03 # Masuk ke atas box
    
    # Anotasi panah
    ax.annotate("",
                xy=(end_x, end_y), xycoords='data',
                xytext=(start_x, start_y), textcoords='data',
                arrowprops=dict(arrowstyle="->", color="black", lw=2, connectionstyle="arc3,rad=0"))
    
    # Menambahkan teks di tengah panah jika ada
    if arrow_text:
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Penyesuaian khusus teks panah agar tidak menabrak garis
        if start_key == 'Tahap2' and end_key == 'Tahap3A':
            mid_x -= 0.1
        elif start_key == 'Tahap2' and end_key == 'Tahap3B':
            mid_x += 0.1
            
        ax.text(mid_x, mid_y, arrow_text, ha='center', va='center', fontsize=9, 
                fontfamily='serif', fontweight='bold', style='italic', color='#333333',
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.8))

# Judul Utama
plt.title("Bagan Alir (Pipeline) Metodologi Penelitian", fontsize=16, fontweight='bold', fontfamily='serif', y=0.98)

# Border titik-titik keliling gambar
rect = plt.Rectangle((0.1, 0.1), 0.8, 0.88, fill=False, edgecolor='gray', linestyle='--', lw=1.5, alpha=0.5)
ax.add_patch(rect)

# Save
plt.savefig('Pipeline_Metodologi_Pareto_TSP.png', bbox_inches='tight', dpi=300)
plt.close()

print("Gambar Pipeline Metodologi berhasil dibuat.")
