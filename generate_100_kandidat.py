import pandas as pd
import numpy as np

n = 100
np.random.seed(42)

# Koordinat pusat (Sekitar Alun-Alun Tuban)
center_lat, center_lon = -6.8944, 112.0658 

# Menyebar 100 titik di radius sekitar 2-3 KM dari pusat kota Tuban
lats = np.random.uniform(center_lat - 0.02, center_lat + 0.02, n)
lons = np.random.uniform(center_lon - 0.03, center_lon + 0.03, n)

data = {
    'Kode_Lokasi': [f'K{str(i).zfill(3)}' for i in range(1, n+1)],
    'Nama_Lokasi': [f'Kandidat {i}' for i in range(1, n+1)],
    'Lat': lats,
    'Lon': lons,
    'C1_Aksesibilitas': np.random.randint(4, 11, n),
    'C2_Kepadatan_Penduduk': np.random.randint(3000, 15000, n),
    'C3_Infrastruktur': np.random.randint(4, 11, n),
    'C4_Kompetisi': np.zeros(n), # Akan diisi dari data nyata OSM
    'C5_Biaya_Sewa': np.random.randint(10, 60, n),
    'C6_Demografi_Usia_Produktif': np.random.randint(25, 70, n),
    'C7_Kedekatan_POI': np.zeros(n) # Akan diisi dari data nyata OSM
}

df = pd.DataFrame(data)
df.to_csv('/home/andy/VibeCoding/ScrapingLokasi/data_kandidat_kafe.csv', index=False)
print("Berhasil memperbarui 100 data kandidat dengan Koordinat (Lat, Lon)!")
