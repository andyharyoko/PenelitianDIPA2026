import os
import json
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import osmnx as ox

warnings.filterwarnings('ignore')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CACHE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'cache')
os.makedirs(DATA_DIR, exist_ok=True)

PLACE_NAME = "Tuban, Jawa Timur, Indonesia"

def generate_200_candidates():
    print(f"[1/5] Membaca data OpenStreetMap untuk {PLACE_NAME}...")
    ox.settings.use_cache = True
    if os.path.exists(CACHE_DIR):
        ox.settings.cache_folder = CACHE_DIR
    
    # 1. Ambil kafe & restoran nyata
    tags_cafe = {'amenity': ['cafe', 'restaurant']}
    cafes = ox.features_from_place(PLACE_NAME, tags_cafe)
    cafes['geometry'] = cafes['geometry'].centroid
    print(f"      -> {len(cafes)} data kafe/restoran dimuat dari OSM.")

    # 2. Ambil POI (Points of Interest)
    tags_poi = {
        'amenity': ['school', 'university', 'college', 'hospital', 'bank'],
        'shop': ['mall', 'supermarket', 'convenience'],
        'office': True
    }
    pois = ox.features_from_place(PLACE_NAME, tags_poi)
    pois['geometry'] = pois['geometry'].centroid
    print(f"      -> {len(pois)} data POI dimuat dari OSM.")

    # 3. Generate 200 titik kandidat di koridor kota Tuban
    n = 200
    print(f"\n[2/5] Menghasilkan {n} kandidat lokasi kafe di koridor strategis Tuban...")
    
    # Zona pusat Tuban: sekitar Alun-Alun, Jl. Basuki Rahmat, Jl. Veteran, Jl. Letda Sucipto, Jl. Pahlawan, Pantai Boom
    np.random.seed(42) # Replicable seed
    
    # Ambil sampel dari koordinat kafe nyata dan sebar dengan jitter radius 100 - 800 meter
    sampel_cafes = cafes.sample(n=n, replace=True, random_state=42)
    
    # Noise geografis dalam derajat (~0.001 deg ~ 111 meter)
    jitter_lat = np.random.uniform(-0.008, 0.008, n)
    jitter_lon = np.random.uniform(-0.009, 0.009, n)
    
    lats = sampel_cafes.geometry.y.values + jitter_lat
    lons = sampel_cafes.geometry.x.values + jitter_lon
    
    # Nama jalan/area terkenal di Tuban untuk variasi nama lokasi yang realistis
    area_names = [
        "Jl. Basuki Rahmat", "Alun-Alun Tuban", "Jl. Veteran", "Jl. Letda Sucipto", 
        "Jl. Panglima Sudirman", "Jl. Pahlawan", "Kawasan Pantai Boom", "Jl. KH. Agus Salim",
        "Jl. Dr. Wahidin Sudirohusodo", "Jl. Hayam Wuruk", "Kawasan Kampus Unirow", 
        "Jl. Gajah Mada", "Kawasan GOR Rangga Jaya", "Jl. RE Martadinata", "Jl. Diponegoro",
        "Jl. Brawijaya", "Jl. Sunan Kalijaga", "Jl. Teuku Umar", "Kawasan Manunggal",
        "Jl. Ronggolawe"
    ]
    
    kandidat_list = []
    for i in range(n):
        kode = f"K{str(i+1).zfill(3)}"
        area = area_names[i % len(area_names)]
        sub_no = (i // len(area_names)) + 1
        nama = f"Kandidat {i+1} ({area} #{sub_no})"
        
        # Atribut non-spasial disimulasikan sesuai profil perkotaan Tuban
        # C1: Aksesibilitas (4 - 10)
        c1 = int(np.random.choice([5, 6, 7, 8, 9, 10], p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.1]))
        
        # C2: Kepadatan Penduduk (3000 - 15000 jiwa/km2)
        c2 = int(np.random.randint(3500, 14500))
        
        # C3: Infrastruktur (4 - 10)
        c3 = int(np.random.choice([5, 6, 7, 8, 9, 10], p=[0.1, 0.15, 0.25, 0.25, 0.15, 0.1]))
        
        # C5: Biaya Sewa (12 - 65 juta/tahun)
        c5 = int(np.random.randint(15, 65))
        
        # C6: Demografi Usia Produktif (30% - 75%)
        c6 = int(np.random.randint(32, 74))
        
        kandidat_list.append({
            'Kode_Lokasi': kode,
            'Nama_Lokasi': nama,
            'Area': area,
            'Lat': float(round(lats[i], 6)),
            'Lon': float(round(lons[i], 6)),
            'C1_Aksesibilitas': c1,
            'C2_Kepadatan_Penduduk': c2,
            'C3_Infrastruktur': c3,
            'C4_Kompetitor': 0, # Dihitung via spatial buffer OSM
            'C5_Biaya_Sewa': c5,
            'C6_Demografi_Usia_Produktif': c6,
            'C7_Kedekatan_POI': 0 # Dihitung via spatial buffer OSM
        })
        
    df_kandidat = pd.DataFrame(kandidat_list)
    
    # 4. Melakukan Spatial Overlay Buffer 1 km (UTM Zone 49S: EPSG 32749)
    print("\n[3/5] Menghitung Analisis Spasial Buffer 1.000m (UTM Zone 49S)...")
    gdf_kandidat = gpd.GeoDataFrame(
        df_kandidat,
        geometry=gpd.points_from_xy(df_kandidat.Lon, df_kandidat.Lat),
        crs="EPSG:4326"
    )
    
    epsg_code = 32749 # UTM Zone 49S untuk Jawa Timur / Tuban
    cafes_utm = cafes.to_crs(epsg=epsg_code)
    pois_utm = pois.to_crs(epsg=epsg_code)
    kandidat_utm = gdf_kandidat.to_crs(epsg=epsg_code)
    
    radius_meter = 1000 # Buffer 1 km
    
    for idx, row in kandidat_utm.iterrows():
        buffer_geom = row.geometry.buffer(radius_meter)
        
        # Hitung jumlah kompetitor dalam buffer
        kompetitor_count = len(cafes_utm[cafes_utm.within(buffer_geom)])
        # Pastikan minimal 1 kompetitor agar kriteria cost tidak membagi 0 di algoritma
        df_kandidat.at[idx, 'C4_Kompetitor'] = max(1, kompetitor_count)
        
        # Hitung jumlah POI dalam buffer
        poi_count = len(pois_utm[pois_utm.within(buffer_geom)])
        df_kandidat.at[idx, 'C7_Kedekatan_POI'] = max(1, poi_count)
        
    print(f"      -> C4 (Kompetitor) terisi: Min={df_kandidat['C4_Kompetitor'].min()}, Max={df_kandidat['C4_Kompetitor'].max()}, Mean={df_kandidat['C4_Kompetitor'].mean():.1f}")
    print(f"      -> C7 (POI) terisi: Min={df_kandidat['C7_Kedekatan_POI'].min()}, Max={df_kandidat['C7_Kedekatan_POI'].max()}, Mean={df_kandidat['C7_Kedekatan_POI'].mean():.1f}")
    
    # 5. Ekspor data ke JSON dan CSV
    print("\n[4/5] Mengekspor data ke format JSON dan CSV...")
    csv_out = os.path.join(DATA_DIR, 'kandidat_200.csv')
    json_out = os.path.join(DATA_DIR, 'kandidat_200.json')
    
    df_kandidat.to_csv(csv_out, index=False)
    
    records = df_kandidat.to_dict(orient='records')
    with open(json_out, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
        
    print(f"      -> Berkas CSV tersimpan di: {csv_out}")
    print(f"      -> Berkas JSON tersimpan di: {json_out}")
    
    # Cetak sampel 5 baris pertama
    print("\n[5/5] Sampel 5 Kandidat Pertama:")
    print(df_kandidat[['Kode_Lokasi', 'Nama_Lokasi', 'Lat', 'Lon', 'C4_Kompetitor', 'C7_Kedekatan_POI', 'C5_Biaya_Sewa']].head().to_string(index=False))
    print("\n[SUKSES] 200 kandidat lokasi kafe dari OSM Tuban berhasil di-generate!")

if __name__ == '__main__':
    generate_200_candidates()
