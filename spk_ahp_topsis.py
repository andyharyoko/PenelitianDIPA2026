import numpy as np
import pandas as pd
import folium
import warnings

warnings.filterwarnings('ignore')

def ahp_weights():
    # 1. Menyusun Matriks Perbandingan Berpasangan AHP (Skala Saaty 1-9)
    # Urutan Kriteria: C1(Akses), C2(Kepadatan), C3(Infra), C4(Kompetisi), C5(Sewa), C6(Demografi), C7(POI)
    # Asumsi: Sewa (C5) dan POI (C7) sama-sama sangat penting dibanding yang lain.
    matrix = np.array([
        [1,   1/2, 1,   1/2, 1/3, 1,   1/3], # C1
        [2,   1,   2,   1,   1/2, 2,   1/2], # C2
        [1,   1/2, 1,   1/2, 1/3, 1,   1/3], # C3
        [2,   1,   2,   1,   1/2, 2,   1/2], # C4
        [3,   2,   3,   2,   1,   3,   1  ], # C5
        [1,   1/2, 1,   1/2, 1/3, 1,   1/3], # C6
        [3,   2,   3,   2,   1,   3,   1  ]  # C7
    ])
    
    # 2. Menghitung Bobot (Eigenvector)
    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum
    weights = norm_matrix.mean(axis=1)
    return weights

def run_topsis(df, weights):
    cols = ['C1_Aksesibilitas', 'C2_Kepadatan_Penduduk', 'C3_Infrastruktur', 
            'C4_Kompetitor', 'C5_Biaya_Sewa', 'C6_Demografi_Usia_Produktif', 'C7_Kedekatan_POI']
    types = ['benefit', 'benefit', 'benefit', 'cost', 'cost', 'benefit', 'benefit']
            
    # 1. Normalisasi TOPSIS: x_ij / sqrt(sum(x_ij^2))
    df_norm = pd.DataFrame()
    for col in cols:
        denominator = np.sqrt((df[col]**2).sum())
        # Proteksi divide by zero
        if denominator == 0: denominator = 1e-9
        df_norm[col] = df[col] / denominator
        
    # 2. Weighted Normalized Matrix (Matriks Normalisasi Terbobot AHP)
    df_weighted = df_norm * weights
    
    # 3. Solusi Ideal Positif (A+) dan Solusi Ideal Negatif (A-)
    A_plus = []
    A_minus = []
    for i, col in enumerate(cols):
        if types[i] == 'benefit':
            A_plus.append(df_weighted[col].max())
            A_minus.append(df_weighted[col].min())
        else: # Kriteria Cost (Terbalik)
            A_plus.append(df_weighted[col].min())
            A_minus.append(df_weighted[col].max())
            
    # 4. Menghitung Jarak Solusi (Separation Measure)
    # Jarak ke Ideal Positif (S+) dan Negatif (S-)
    S_plus = np.sqrt(((df_weighted - A_plus)**2).sum(axis=1))
    S_minus = np.sqrt(((df_weighted - A_minus)**2).sum(axis=1))
    
    # 5. Nilai Preferensi / Kedekatan Relatif (Closeness Coefficient)
    C_star = S_minus / (S_plus + S_minus)
    return C_star

def main():
    print("Menjalankan Pipeline SPK: AHP (Pembobotan) + TOPSIS (Perankingan)...")
    
    # Dapatkan bobot secara matematis dari AHP
    weights = ahp_weights()
    cols_name = ['C1_Akses', 'C2_Kepadatan', 'C3_Infra', 'C4_Kompetitor', 'C5_Sewa', 'C6_Demografi', 'C7_POI']
    
    print("\nBobot Prioritas Hasil Hitung AHP (Eigenvector):")
    for c, w in zip(cols_name, weights):
        print(f" - {c}: {w*100:.1f}%")
        
    # Baca Dataset 100 Kandidat
    csv_path = '/home/andy/VibeCoding/ScrapingLokasi/data_kandidat_kafe.csv'
    df = pd.read_csv(csv_path)
    
    # Eksekusi Algoritma TOPSIS menggunakan bobot AHP
    df['Skor_TOPSIS'] = run_topsis(df, weights)
    
    # Urutkan pemenang
    df = df.sort_values(by='Skor_TOPSIS', ascending=False).reset_index(drop=True)
    out_csv = '/home/andy/VibeCoding/ScrapingLokasi/hasil_ranking_ahp_topsis.csv'
    df.to_csv(out_csv, index=False)
    
    print("\n--- TOP 5 KANDIDAT LOKASI (AHP-TOPSIS) ---")
    top_5 = df.head(5)
    print(top_5[['Kode_Lokasi', 'Nama_Lokasi', 'Skor_TOPSIS', 'C4_Kompetitor', 'C7_Kedekatan_POI']].to_string(index=False))

    # ==========================================
    # PERBANDINGAN DENGAN SAW
    # ==========================================
    try:
        df_saw = pd.read_csv('/home/andy/VibeCoding/ScrapingLokasi/hasil_ranking_saw.csv')
        top_5_saw = df_saw.head(5)['Kode_Lokasi'].tolist()
        top_5_topsis = top_5['Kode_Lokasi'].tolist()
        
        print("\n--- PERBANDINGAN JUARA 1 - 5 ---")
        print(f"Pemenang Metode SAW        : {top_5_saw}")
        print(f"Pemenang Metode AHP-TOPSIS : {top_5_topsis}")
        
        print("\nMembuat Peta Perbandingan Spasial (peta_perbandingan_metode.html)...")
        center_lat = top_5.iloc[0]['Lat']
        center_lon = top_5.iloc[0]['Lon']
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
        
        # Himpunan lokasi juara dari kedua metode
        kodes = set(top_5_saw + top_5_topsis)
        df_plot = df[df['Kode_Lokasi'].isin(kodes)]
        
        for idx, row in df_plot.iterrows():
            k = row['Kode_Lokasi']
            in_saw = k in top_5_saw
            in_top = k in top_5_topsis
            
            if in_saw and in_top:
                warna = 'purple'
                label = f"Juara SAW & TOPSIS ({k})"
            elif in_top:
                warna = 'blue'
                label = f"Juara TOPSIS saja ({k})"
            else:
                warna = 'red'
                label = f"Juara SAW saja ({k})"
                
            popup_text = f"<b>{label}</b><br>Skor TOPSIS: {row['Skor_TOPSIS']:.4f}"
            
            folium.Marker(
                location=[row['Lat'], row['Lon']],
                popup=popup_text,
                tooltip=label,
                icon=folium.Icon(color=warna, icon='star')
            ).add_to(m)

        m.save("/home/andy/VibeCoding/ScrapingLokasi/peta_perbandingan_metode.html")
        print("Selesai! Peta perbandingan metode telah disimpan.")
    except FileNotFoundError:
        print("File ranking SAW tidak ditemukan, lompati perbandingan.")

if __name__ == '__main__':
    main()
