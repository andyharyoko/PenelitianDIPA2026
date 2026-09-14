import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from shapely.geometry import Point
import warnings

# Mengabaikan pesan warning agar terminal tetap bersih
warnings.filterwarnings('ignore')

PLACE_NAME = "Tuban, Jawa Timur, Indonesia"

def run_osm_analysis():
    print(f"Mengunduh data geospasial untuk: {PLACE_NAME}")
    
    # 1. Ekstrak Kompetitor
    print("[1/5] Mengunduh data kompetitor (Cafe/Resto)...")
    tags_cafe = {'amenity': ['cafe', 'restaurant']}
    try:
        cafes = ox.features_from_place(PLACE_NAME, tags_cafe)
        cafes['geometry'] = cafes['geometry'].centroid
        print(f"      -> Ditemukan {len(cafes)} titik kompetitor.")
    except Exception as e:
        print(f"Gagal mengambil kompetitor: {e}")
        return

    # 2. Ekstrak POI
    print("[2/5] Mengunduh data Point of Interest (POI)...")
    tags_poi = {
        'amenity': ['school', 'university', 'college', 'hospital', 'bank'],
        'shop': ['mall', 'supermarket', 'convenience'],
        'office': True
    }
    try:
        pois = ox.features_from_place(PLACE_NAME, tags_poi)
        pois['geometry'] = pois['geometry'].centroid
        print(f"      -> Ditemukan {len(pois)} Titik Minat (POI).")
    except Exception as e:
        print(f"Gagal mengambil POI: {e}")
        return

    print("\n[3/5] Menggeser 100 data kandidat ke area seputar kompetitor...")
    csv_path = '/home/andy/VibeCoding/ScrapingLokasi/data_kandidat_kafe.csv'
    df_kandidat = pd.read_csv(csv_path)
    n = len(df_kandidat)
    
    # Mengambil sampel koordinat dari kompetitor nyata (jika kurang dari n, boleh berulang)
    sampel_kompetitor = cafes.sample(n=n, replace=True, random_state=42)
    
    # Memberi efek "Jitter" (acak jarak sedikit) sekitar ~100-300 meter agar tidak numpuk di titik yg persis sama
    # 1 derajat Latitude approx 111km. 0.001 approx 111 meter.
    np.random.seed(42)
    noise_lat = np.random.uniform(-0.002, 0.002, n)
    noise_lon = np.random.uniform(-0.002, 0.002, n)
    
    df_kandidat['Lat'] = sampel_kompetitor.geometry.y.values + noise_lat
    df_kandidat['Lon'] = sampel_kompetitor.geometry.x.values + noise_lon
    
    print("\n[4/5] Melakukan overlay analisis spasial (Buffer 1km)...")
    gdf_kandidat = gpd.GeoDataFrame(
        df_kandidat, 
        geometry=gpd.points_from_xy(df_kandidat.Lon, df_kandidat.Lat),
        crs="EPSG:4326"
    )

    epsg_code = 32749 # UTM Zone 49S
    cafes_utm = cafes.to_crs(epsg=epsg_code)
    pois_utm = pois.to_crs(epsg=epsg_code)
    kandidat_utm = gdf_kandidat.to_crs(epsg=epsg_code)

    radius_meter = 1000 # Jangkauan buffer
    
    for idx, row in kandidat_utm.iterrows():
        buffer_geom = row.geometry.buffer(radius_meter)
        
        kompetitor_terdekat = cafes_utm[cafes_utm.within(buffer_geom)]
        df_kandidat.at[idx, 'C4_Kompetitor'] = len(kompetitor_terdekat)
        
        poi_terdekat = pois_utm[pois_utm.within(buffer_geom)]
        df_kandidat.at[idx, 'C7_Kedekatan_POI'] = len(poi_terdekat)

    df_kandidat.to_csv(csv_path, index=False)
    print("      -> Nilai riil C4 (Kompetitor) dan C7 (POI) telah diperbarui di file CSV!")
    
    print("\n[5/5] Membuat visualisasi peta HTML dengan Marker Bintang...")
    # Pusatkan peta secara dinamis
    center_lat = df_kandidat['Lat'].mean()
    center_lon = df_kandidat['Lon'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
    
    # Plot Kompetitor (Lingkaran Merah)
    for idx, row in cafes.iterrows():
        if row.geometry.geom_type == 'Point':
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=3, color='red', fill=True, fill_opacity=0.6,
                tooltip="Kompetitor/Cafe"
            ).add_to(m)

    # Plot POI (Titik Kecil Biru)
    for idx, row in pois.iterrows():
        if row.geometry.geom_type == 'Point':
            folium.CircleMarker(
                location=[row.geometry.y, row.geometry.x],
                radius=1, color='blue', fill=True, fill_opacity=0.2,
                tooltip="POI (Sekolah/Mall)"
            ).add_to(m)

    # Plot 100 Kandidat (Marker Keren Warna Hijau)
    for idx, row in df_kandidat.iterrows():
        popup_text = f"<b>{row['Nama_Lokasi']}</b><br>" \
                     f"Kode: {row['Kode_Lokasi']}<br>" \
                     f"C4 Kompetitor: {int(row['C4_Kompetitor'])}<br>" \
                     f"C7 POI: {int(row['C7_Kedekatan_POI'])}"
                     
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=popup_text,
            tooltip=f"{row['Kode_Lokasi']} (Kandidat)",
            icon=folium.Icon(color='green', icon='star') # Icon Bintang
        ).add_to(m)

    output_peta = "peta_analisis_osm.html"
    m.save(output_peta)
    print(f"Selesai! Peta kandidat di area kompetitor disimpan sebagai '{output_peta}'")

if __name__ == "__main__":
    run_osm_analysis()
