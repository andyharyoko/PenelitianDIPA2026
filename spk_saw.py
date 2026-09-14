import pandas as pd
import folium

def hitung_spk_saw():
    csv_path = '/home/andy/VibeCoding/ScrapingLokasi/data_kandidat_kafe.csv'
    print(f"Membaca dataset dari {csv_path}...")
    df = pd.read_csv(csv_path)

    # 1. Tentukan Jenis Kriteria (Benefit / Cost)
    kriteria = {
        'C1_Aksesibilitas': 'benefit',
        'C2_Kepadatan_Penduduk': 'benefit',
        'C3_Infrastruktur': 'benefit',
        'C4_Kompetitor': 'cost',
        'C5_Biaya_Sewa': 'cost',
        'C6_Demografi_Usia_Produktif': 'benefit',
        'C7_Kedekatan_POI': 'benefit'
    }

    # 2. Tentukan Bobot (Total harus 1.0 atau 100%)
    # Asumsi: Biaya sewa dan Kedekatan POI sangat penting
    bobot = {
        'C1_Aksesibilitas': 0.10,
        'C2_Kepadatan_Penduduk': 0.15,
        'C3_Infrastruktur': 0.10,
        'C4_Kompetitor': 0.15,
        'C5_Biaya_Sewa': 0.20,
        'C6_Demografi_Usia_Produktif': 0.10,
        'C7_Kedekatan_POI': 0.20
    }

    print("\n[1/3] Melakukan Normalisasi Matriks (Metode SAW)...")
    df_norm = df.copy()
    
    # Menghindari error pembagian dengan nol (Divide by Zero) pada kriteria Cost
    # Jika ada lokasi yang memiliki 0 kompetitor, kita tambahkan nilai sangat kecil
    if (df['C4_Kompetitor'] == 0).any():
        df_norm['C4_Kompetitor'] = df_norm['C4_Kompetitor'] + 1 

    for col, jenis in kriteria.items():
        if jenis == 'benefit':
            # Jika Benefit: Nilai dibagi dengan Nilai Maksimum
            max_val = df_norm[col].max()
            df_norm[col] = df_norm[col] / max_val
        elif jenis == 'cost':
            # Jika Cost: Nilai Minimum dibagi dengan Nilai
            min_val = df_norm[col].min()
            df_norm[col] = min_val / df_norm[col]

    print("[2/3] Menghitung Nilai Preferensi (Skor Akhir)...")
    df['Skor_Akhir'] = 0.0
    for col in kriteria.keys():
        df['Skor_Akhir'] += df_norm[col] * bobot[col]

    # 3. Mengurutkan berdasarkan Skor Tertinggi
    df = df.sort_values(by='Skor_Akhir', ascending=False).reset_index(drop=True)
    
    # Simpan hasil pemeringkatan
    output_csv = '/home/andy/VibeCoding/ScrapingLokasi/hasil_ranking_saw.csv'
    df.to_csv(output_csv, index=False)
    
    print("\n--- TOP 5 KANDIDAT LOKASI TERBAIK ---")
    top_5 = df.head(5)
    print(top_5[['Kode_Lokasi', 'Nama_Lokasi', 'Skor_Akhir', 'C4_Kompetitor', 'C7_Kedekatan_POI']].to_string(index=False))

    print("\n[3/3] Memetakan Top 5 Lokasi Terbaik ke Peta HTML...")
    # Pusatkan peta di kandidat juara 1
    center_lat = top_5.iloc[0]['Lat']
    center_lon = top_5.iloc[0]['Lon']
    m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
    
    # Warna khusus untuk Top 5
    colors = ['red', 'orange', 'blue', 'purple', 'darkgreen']
    
    for idx, row in top_5.iterrows():
        rank = idx + 1
        warna = colors[idx]
        
        popup_text = f"<b>🏆 Peringkat {rank}</b><br>" \
                     f"Nama: {row['Nama_Lokasi']}<br>" \
                     f"Skor Akhir: {row['Skor_Akhir']:.4f}<br>" \
                     f"Sewa: {row['C5_Biaya_Sewa']} Jt<br>" \
                     f"POI (C7): {row['C7_Kedekatan_POI']}"
                     
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=popup_text,
            tooltip=f"Juara {rank} - {row['Kode_Lokasi']}",
            icon=folium.Icon(color=warna, icon='star')
        ).add_to(m)

    # (Opsional) Tampilkan juga sisa kandidat dengan titik abu-abu kecil
    sisa_kandidat = df.iloc[5:]
    for idx, row in sisa_kandidat.iterrows():
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=3, color='gray', fill=True, fill_opacity=0.3,
            tooltip=f"Peringkat {idx+1}"
        ).add_to(m)

    output_peta = "/home/andy/VibeCoding/ScrapingLokasi/peta_rekomendasi_terbaik.html"
    m.save(output_peta)
    print(f"\nSelesai! File rekomendasi peta disimpan di: {output_peta}")
    print(f"Data lengkap 100 ranking disimpan di: {output_csv}")

if __name__ == "__main__":
    hitung_spk_saw()
