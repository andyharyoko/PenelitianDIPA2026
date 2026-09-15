# Optimasi Pemilihan Lokasi Kafe Menggunakan Data Spasial OSM & Multi-Criteria Decision Making (MCDM)
### Penelitian Hibah DIPA 2026 
### Luaran 
### Jurnal Sinta 2 Riemann : Pareto-TSP Decision Support Framework for Cafe Location Selection in Tuban Regency (https://journal.sanagustin.ac.id/index.php/reimann/article/view/210)
### SemnasPPM : On riview
### HaKI : Akan di Proses Direncanakan adalah Aplikasi ini atau Arsitektur Sistem 
(https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_architecture.html)
(https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_dataflow.html)

### 🌐 **Aplikasi Web Live (GitHub Pages):** [https://andyharyoko.github.io/PenelitianDIPA2026/](https://andyharyoko.github.io/PenelitianDIPA2026/)

Repositori ini berisi kode sumber komputasi spasial, algoritma Sistem Pendukung Keputusan (SPK/DSS), pemodelan rute *Traveling Salesperson Problem* (TSP), serta aplikasi web interaktif (*WebGIS Decision Hub*) untuk optimasi penentuan lokasi strategis kafe di Kabupaten Tuban, Jawa Timur.

---

## 👥 Tim Peneliti
- **Andy Haryoko** (*andyharyoko@gmail.com*)
- **Suprapto**
- **Gusti Uripno**

**Program Studi Teknik Informatika, Fakultas Teknik, Universitas PGRI Ronggolawe (Unirow) Tuban**
**Program Studi Pendidikan Matematika, Fakultas Keguruan dan Ilmu Pengetahuan, Universitas PGRI Ronggolawe (Unirow) Tuban**
---

## 🌟 Fitur Utama & Pipeline Metodologi

1. **Ekstraksi Data Geospasial Riil (OpenStreetMap / OSM):**
   - 200 Titik Kandidat Lokasi Kafe di koridor strategis perkotaan Tuban.
   - 178 Titik Kafe & Restoran Pesaing (Kriteria C4 - Kompetisi).
   - 528 Titik Point of Interest / POI (Kriteria C7 - Kedekatan Fasilitas: sekolah, kampus, bank, mall, rumah sakit, perkantoran).
   - Analisis *Spatial Overlay Buffer* 1.000 meter (UTM Zone 49S: EPSG 32749).

2. **Pembobotan Analytical Hierarchy Process (AHP):**
   - Matriks Perbandingan Berpasangan $7 \times 7$ Skala Saaty (1-9).
   - Uji Rasio Konsistensi: $\lambda_{\max} = 7.02029$, $CI = 0.00338$, $RI = 1.32$, **$CR = 0.00256$ (0.256% < 10% - Sangat Konsisten)**.

3. **Komparasi 3 Metode Multi-Criteria Decision Making (MCDM):**
   - **Simple Additive Weighting (SAW)**: Normalisasi linier benefit/cost.
   - **TOPSIS (AHP-TOPSIS)**: Solusi ideal positif/negatif & kedekatan relatif jarak Euclidean ($C^*$).
   - **Weighted Product (WP)**: Perkalian berpangkat nilai kriteria (+w benefit, -w cost).

4. **Optimasi Rute Ground Truth (TSP) & Pareto Filtering (`TSP-Pareto/`):**
   - Penyaringan Pareto Optimality mereduksi kandidat non-dominated.
   - Optimasi rute tertutup survei lapangan sepanjang **195,44 km** menghubungkan seluruh lokasi optimal.

5. **Aplikasi Web Interaktif (`webapp/`):**
   - Single Page Application berbasis Leaflet.js & Chart.js.
   - Peta interaktif multi-layer menampilkan seluruh 906 titik spasial (200 kandidat + 178 kafe OSM + 528 POI OSM).
   - Fitur buffer lingkaran 1.000m interaktif saat memilih kandidat.
   - Editor matriks AHP interaktif (re-kalkulasi instan nilai CR dan pemeringkatan).
   - Komparasi Top 10 berdampingan, Bump Chart pergeseran ranking, Scatter Plot korelasi, dan Radar Chart profil 7 kriteria.

---

## 📁 Struktur Direktori

```
├── webapp/                             # Aplikasi Web SPK Interaktif
│   ├── index.html                      # Antarmuka utama aplikasi
│   ├── css/                            # Styling desain sistem modern (Dark/Light mode)
│   ├── js/                             # Logika matematika (AHP, MCDM, Leaflet Map, Charts)
│   ├── data/                           # Dataset 200 kandidat, 178 kafe, 528 POI (JSON & CSV)
│   └── scripts/                        # Skrip Python pembuatan dataset & benchmark MCDM
├── TSP-Pareto/                         # Penelitian Lanjutan Pareto & TSP
│   ├── run_pareto_tsp_spk.py           # Pipeline komputasi Pareto + TSP + MCDM
│   ├── generate_pareto_charts.py       # Pembuat grafik komparasi Pareto
│   ├── peta_rute_tsp_pareto.html       # Peta navigasi rute survei TSP
│   └── *.docx                          # Draf laporan kemajuan DIPA 2026 (Bab I, II, IV)
├── data_kandidat_kafe.csv              # Dataset mentah 100 kandidat awal
├── osm_analysis.py                     # Ekstraksi dan buffer OSMnx Tuban
├── spk_saw.py                          # Algoritma dasar SAW
├── spk_ahp_topsis.py                   # Algoritma dasar AHP-TOPSIS
├── generate_method_comparison.py       # Visualisasi slopegraph & korelasi
├── Draft_JATI_Optimasi_Lokasi_Kafe.docx # Naskah publikasi jurnal JATI
└── README.md
```

---

## 🚀 Cara Menjalankan WebApp

### Menjalankan Web Server Lokal:
```bash
cd webapp
python3 -m http.server 8085
```
Buka browser di: **http://localhost:8085/**

Aplikasi juga mendukung pembukaan langsung secara offline tanpa server melalui berkas `webapp/index.html`.
