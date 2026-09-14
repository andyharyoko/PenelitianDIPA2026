import pandas as pd
import numpy as np
import folium
import math
import networkx as nx
from networkx.algorithms import approximation
import os

def run_pipeline():
    CSV_PATH = '../data_kandidat_kafe.csv'
    if not os.path.exists(CSV_PATH):
        print(f"File {CSV_PATH} tidak ditemukan.")
        return
        
    print(f"Membaca dataset awal dari {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    # Definisi Kriteria & Bobot
    kriteria = {
        'C1_Aksesibilitas': 'benefit',
        'C2_Kepadatan_Penduduk': 'benefit',
        'C3_Infrastruktur': 'benefit',
        'C4_Kompetitor': 'cost',
        'C5_Biaya_Sewa': 'cost',
        'C6_Demografi_Usia_Produktif': 'benefit',
        'C7_Kedekatan_POI': 'benefit'
    }
    bobot_dict = {
        'C1_Aksesibilitas': 0.10,
        'C2_Kepadatan_Penduduk': 0.15,
        'C3_Infrastruktur': 0.10,
        'C4_Kompetitor': 0.15,
        'C5_Biaya_Sewa': 0.20,
        'C6_Demografi_Usia_Produktif': 0.10,
        'C7_Kedekatan_POI': 0.20
    }

    # =====================================================================
    # 1. PARETO OPTIMIZATION (SCREENING AWAL)
    # =====================================================================
    print("\n[1/5] Melakukan Pareto Screening untuk menyaring kandidat terdominasi...")
    def is_dominated(x, y, kriteria_dict):
        # Mengecek apakah kandidat x didominasi oleh kandidat y
        worse_in_any = False
        better_in_any = False
        for k, v in kriteria_dict.items():
            if v == 'benefit':
                if y[k] < x[k]: better_in_any = True
                elif y[k] > x[k]: worse_in_any = True
            else: # cost
                if y[k] > x[k]: better_in_any = True
                elif y[k] < x[k]: worse_in_any = True
        
        # Jika y tidak lebih buruk di kriteria apa pun, dan lebih baik di minimal satu kriteria
        if not better_in_any and worse_in_any:
            return True # x didominasi oleh y
        return False

    pareto_mask = []
    rows = df.to_dict('records')
    for i, row1 in enumerate(rows):
        dominated = False
        for j, row2 in enumerate(rows):
            if i != j:
                if is_dominated(row1, row2, kriteria):
                    dominated = True
                    break
        pareto_mask.append(not dominated)

    df_pareto = df[pareto_mask].reset_index(drop=True)
    print(f"--> Pareto Selesai: Dari {len(df)} kandidat awal, tersaring menjadi {len(df_pareto)} kandidat Pareto Optimal (Non-dominated).")
    df_pareto.to_csv('kandidat_pareto.csv', index=False)


    # =====================================================================
    # 2. TRAVELING SALESPERSON PROBLEM (TSP) PADA PARETO FRONT
    # Mengoptimasi rute survei / logistik lapangan
    # =====================================================================
    print("\n[2/5] Menghitung Rute TSP Terpendek untuk Validasi Lapangan (Pareto Candidates)...")
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0 # Radius bumi (km)
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    G = nx.Graph()
    for i, r1 in df_pareto.iterrows():
        for j, r2 in df_pareto.iterrows():
            if i != j:
                dist = haversine(r1['Lat'], r1['Lon'], r2['Lat'], r2['Lon'])
                G.add_edge(i, j, weight=dist)

    # Menggunakan Aproksimasi TSP dari NetworkX
    tsp_path = approximation.traveling_salesman_problem(G, cycle=True)
    
    # Hitung total jarak
    total_jarak = sum(G[tsp_path[i]][tsp_path[i+1]]['weight'] for i in range(len(tsp_path)-1))
    print(f"--> Rute TSP Ditemukan! Total perhentian: {len(tsp_path)}, Total Jarak: {total_jarak:.2f} km.")

    # Visualisasi Peta TSP
    m_tsp = folium.Map(location=[df_pareto['Lat'].mean(), df_pareto['Lon'].mean()], zoom_start=12)
    tsp_coords = []
    
    for urutan, node_idx in enumerate(tsp_path):
        r = df_pareto.iloc[node_idx]
        tsp_coords.append([r['Lat'], r['Lon']])
        
        # Penanda titik
        if urutan == 0 or urutan == len(tsp_path)-1: # Titik Awal/Akhir
            folium.Marker([r['Lat'], r['Lon']], popup=f"START/END: {r['Nama_Lokasi']}", icon=folium.Icon(color='red', icon='play')).add_to(m_tsp)
        else:
            folium.CircleMarker([r['Lat'], r['Lon']], radius=5, color='blue', fill=True, popup=f"Ke-{urutan}: {r['Nama_Lokasi']}").add_to(m_tsp)

    # Gambar rute jalan
    folium.PolyLine(tsp_coords, color="purple", weight=3, opacity=0.8, dash_array="5, 5").add_to(m_tsp)
    m_tsp.save('peta_rute_tsp_pareto.html')


    # =====================================================================
    # 3. METODE SAW PADA KANDIDAT PARETO
    # =====================================================================
    print("\n[3/5] Melakukan SAW pada kandidat Pareto...")
    df_saw = df_pareto.copy()
    if (df_saw['C4_Kompetitor'] == 0).any():
        df_saw['C4_Kompetitor'] = df_saw['C4_Kompetitor'] + 1 
        
    for col, jenis in kriteria.items():
        if jenis == 'benefit':
            df_saw[col] = df_saw[col] / df_saw[col].max()
        else:
            df_saw[col] = df_saw[col].min() / df_saw[col]

    df_pareto_saw = df_pareto.copy()
    df_pareto_saw['Skor_SAW'] = sum(df_saw[col] * bobot_dict[col] for col in kriteria.keys())
    df_pareto_saw = df_pareto_saw.sort_values('Skor_SAW', ascending=False).reset_index(drop=True)
    df_pareto_saw.to_csv('hasil_saw_pareto.csv', index=False)


    # =====================================================================
    # 4. METODE AHP-TOPSIS PADA KANDIDAT PARETO
    # =====================================================================
    print("\n[4/5] Melakukan AHP-TOPSIS pada kandidat Pareto...")
    df_topsis = df_pareto.copy()
    
    # Matriks Ternormalisasi Terbobot
    for col in kriteria.keys():
        pembagi = np.sqrt(sum(df_topsis[col]**2))
        df_topsis[col] = df_topsis[col] / pembagi * bobot_dict[col]

    # Solusi Ideal Positif & Negatif
    ideal_positif = {}
    ideal_negatif = {}
    for col, jenis in kriteria.items():
        if jenis == 'benefit':
            ideal_positif[col] = df_topsis[col].max()
            ideal_negatif[col] = df_topsis[col].min()
        else:
            ideal_positif[col] = df_topsis[col].min()
            ideal_negatif[col] = df_topsis[col].max()

    # Jarak & Skor Preferensi
    d_positif = np.sqrt(sum((df_topsis[col] - ideal_positif[col])**2 for col in kriteria.keys()))
    d_negatif = np.sqrt(sum((df_topsis[col] - ideal_negatif[col])**2 for col in kriteria.keys()))
    
    df_pareto_topsis = df_pareto.copy()
    df_pareto_topsis['Skor_TOPSIS'] = d_negatif / (d_positif + d_negatif)
    df_pareto_topsis = df_pareto_topsis.sort_values('Skor_TOPSIS', ascending=False).reset_index(drop=True)
    df_pareto_topsis.to_csv('hasil_ahp_topsis_pareto.csv', index=False)

    print("\n[5/5] Selesai! Semua pipeline berhasil dieksekusi.")
    print("Files yang disimpan:")
    print(" - kandidat_pareto.csv (Kandidat yang lulus filter Pareto)")
    print(" - peta_rute_tsp_pareto.html (Visualisasi peta Rute Ground Truth)")
    print(" - hasil_saw_pareto.csv (Ranking SAW untuk Pareto)")
    print(" - hasil_ahp_topsis_pareto.csv (Ranking TOPSIS untuk Pareto)")

if __name__ == "__main__":
    run_pipeline()
