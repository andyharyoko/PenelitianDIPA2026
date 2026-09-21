# CETAK BIRU (BLUEPRINT) ARSITEKTUR SISTEM DAN SPESIFIKASI ALUR DATA SPASIAL WEBGIS DECISION HUB PEMILIHAN LOKASI KAFE

---

**DOKUMEN SPESIFIKASI TEKNIS REKAYASA PERANGKAT LUNAK**  
**LAMPIRAN PERMOHONAN HAK CIPTA KATEGORI KARYA TULIS (BUKU PANDUAN / CETAK BIRU TEKNIS)**  
*Direktorat Jenderal Kekayaan Intelektual (DJKI) — Kementerian Hukum dan HAM Republik Indonesia*

---

### 📌 IDENTITAS CIPTAAN & TIM PENGUSUL

* **Judul Ciptaan:**  
  **Cetak Biru (Blueprint) Arsitektur Sistem dan Spesifikasi Alur Data Spasial WebGIS Decision Hub Pemilihan Lokasi Kafe**
* **Jenis Ciptaan:** Karya Tulis
* **Sub-Jenis Ciptaan:** Buku Panduan / Petunjuk / Modul Teknis / Monograf
* **Skema Pendanaan:** Hibah Penelitian Internal DIPA Universitas PGRI Ronggolawe (Unirow) Tuban
* **Tahun Anggaran:** 2026
* **Institusi Pengusul / Pemegang Hak Cipta:**  
  Lembaga Penelitian dan Pengabdian kepada Masyarakat (LPPM)  
  Universitas PGRI Ronggolawe (Unirow) Tuban  
  Jl. Manunggal No. 61, Tuban, Jawa Timur 62381, Indonesia

#### 👥 Tim Pencipta:
1. **Andy Haryoko, M.Kom.** *(Ketua Peneliti / Arsitek Perangkat Lunak)*  
   Program Studi Teknik Informatika, Fakultas Teknik, Unirow Tuban (`andyharyoko@gmail.com`)
2. **Suprapto, M.Kom.** *(Anggota Peneliti 1 / Analis Sistem & Algoritma)*  
   Program Studi Teknik Informatika, Fakultas Teknik, Unirow Tuban
3. **Gusti Uripno, M.Pd.** *(Anggota Peneliti 2 / Pemodelan Matematika & Evaluasi)*  
   Program Studi Pendidikan Matematika, FKIP, Unirow Tuban
4. **Winda Agustina** *(Kontributor Mahasiswa / Pengembang Antarmuka & Data)*  
   Program Studi Teknik Informatika, Fakultas Teknik, Unirow Tuban

---

## KATA PENGANTAR

Puji dan syukur kami panjatkan ke hadirat Tuhan Yang Maha Esa atas limpahan rahmat dan karunia-Nya sehingga dokumen **Cetak Biru (Blueprint) Arsitektur Sistem dan Spesifikasi Alur Data Spasial WebGIS Decision Hub Pemilihan Lokasi Kafe** ini dapat diselesaikan dengan baik.

Dokumen ini disusun sebagai dokumentasi teknis formal rekayasa perangkat lunak sekaligus instrumen pencatatan Hak Cipta pada Direktorat Jenderal Kekayaan Intelektual (DJKI) Kemenkumham RI atas luaran penelitian **Hibah Internal DIPA Universitas PGRI Ronggolawe (Unirow) Tuban Tahun Anggaran 2026**.

Sistem pendukung keputusan (*Decision Support System* / DSS) berbasis spasial yang dikembangkan mengintegrasikan teknologi data terbuka OpenStreetMap (OSM), metode pembobotan terstruktur *Analytical Hierarchy Process* (AHP), komparasi multi-metode *Multi-Criteria Decision Making* (MCDM: SAW, TOPSIS, Weighted Product), serta pemodelan rute survei lapangan *Traveling Salesperson Problem* (TSP) berbasis filter *Pareto Optimality*.

Tim peneliti menghaturkan terima kasih dan penghargaan yang tulus kepada:
1. **Lembaga Penelitian dan Pengabdian kepada Masyarakat (LPPM) Unirow Tuban**, atas dukungan pendanaan penuh melalui DIPA 2026.
2. **Rektor dan Para Wakil Rektor Unirow Tuban**, atas arahan dan fasilitas yang diberikan.
3. **Dekan Fakultas Teknik dan Dekan FKIP Unirow Tuban**, atas dukungan sarana laboratorium komputasi.
4. **Segenap Dosen dan Mahasiswa**, yang telah berkontribusi aktif dalam pengujian sistem.

Semoga cetak biru ini dapat menjadi rujukan ilmiah dan standar teknis pengembangan perangkat lunak berbasis sistem informasi geografis dan pendukung keputusan di masa mendatang.

Tuban, September 2026  
**Tim Peneliti & Pengembang WebGIS Decision Hub**

---

## DAFTAR ISI

1. [BAB I: PENDAHULUAN & GAMBARAN UMUM SISTEM](#bab-i-pendahuluan--gambaran-umum-sistem)
   - 1.1 Latar Belakang & Urgensi Rekayasa Sistem
   - 1.2 Tujuan dan Manfaat Cetak Biru (Blueprint)
   - 1.3 Ruang Lingkup Sistem & Karakteristik Data
   - 1.4 Profil Pengguna Sasaran (Target Audience)
2. [BAB II: LANDASAN METODOLOGI & MODEL KOMPUTASI MATEMATIS](#bab-ii-landasan-metodologi--model-komputasi-matematis)
   - 2.1 Akuisisi Spasial OpenStreetMap (OSM) & Analisis Buffer UTM Zone 49S
   - 2.2 Taksonomi 7 Kriteria Evaluasi SPK
   - 2.3 Metode Analytical Hierarchy Process (AHP) & Rasio Konsistensi
   - 2.4 Multi-Criteria Decision Making (SAW, TOPSIS, Weighted Product)
   - 2.5 Filter Pareto Optimality & Rute Survei Lapangan TSP
3. [BAB III: CETAK BIRU ARSITEKTUR SISTEM (SYSTEM ARCHITECTURE BLUEPRINT)](#bab-iii-cetak-biru-arsitektur-sistem-system-architecture-blueprint)
   - 3.1 Tinjauan Arsitektur Berlapis (Multi-Layer Architecture)
   - 3.2 Presentation Layer (UI/UX Glassmorphism & Theme Engine)
   - 3.3 Interactive Spatial Map Layer (Leaflet.js & Buffer Ring)
   - 3.4 Analytical & Computation Engine (Client-Side Vanilla JS)
   - 3.5 Data Visualization Layer (Chart.js Engine)
   - 3.6 Karakteristik Non-Fungsional (Zero-Latency & High Portability)
4. [BAB IV: SPESIFIKASI ALUR DATA SISTEM (DATA FLOW PIPELINE)](#bab-iv-spesifikasi-alur-data-sistem-data-flow-pipeline)
   - 4.1 Diagram Konteks Alur Data (Level 0)
   - 4.2 Pipeline 1: Ekstraksi & Preprocessing Data Spasial OSM
   - 4.3 Pipeline 2: Dinamika Matriks Pembobotan AHP Real-Time
   - 4.4 Pipeline 3: Komputasi Normalisasi & Perankingan Multi-MCDM
   - 4.5 Pipeline 4: Rekomendasi Pareto & Perencanaan Rute Validasi TSP
5. [BAB V: SPESIFIKASI TEKNIS & LINGKUNGAN PENGEMBANGAN](#bab-v-spesifikasi-teknis--lingkungan-pengembangan)
   - 5.1 Kebutuhan Perangkat Lunak & Pustaka Dependensi
   - 5.2 Kebutuhan Perangkat Keras Minimum
   - 5.3 Prosedur Deployment & Pengujian Sistem
6. [BAB VI: KESIMPULAN & ARAHAN PENGEMBANGAN](#bab-vi-kesimpulan--arahan-pengembangan)
7. [DAFTAR PUSTAKA](#daftar-pustaka)
8. [LAMPIRAN VISUAL DOKUMENTASI ARSITEKTUR & DATAFLOW](#lampiran-visual-dokumentasi-arsitektur--dataflow)

---

## BAB I: PENDAHULUAN & GAMBARAN UMUM SISTEM

### 1.1 Latar Belakang & Urgensi Rekayasa Sistem
Pertumbuhan industri kreatif dan sektor *Food & Beverage* (F&B), khususnya usaha kafe di Kabupaten Tuban, mengalami akselerasi signifikan dalam beberapa tahun terakhir. Namun, fenomena tingginya angka penutupan usaha kafe baru kerap terjadi dalam rentang waktu kurang dari 12 bulan setelah peresmian. Salah satu faktor kegagalan paling dominan adalah **kesalahan dalam pemilihan lokasi bisnis**.

Secara konvensional, pelaku usaha menentukan lokasi hanya mengandalkan intuisi subjektif, ketersediaan lahan milik keluarga, atau sekadar tren sesaat tanpa didukung oleh analisis spasial dan multikriteria yang terukur. Di sisi lain, data geospasial berskala masif telah tersedia secara terbuka melalui platform *OpenStreetMap* (OSM), yang memuat persebaran kompetitor, jaringan jalan, dan fasilitas publik penarik massa (*Point of Interest* / POI).

Kesenjangan utama dalam penelitian terdahulu adalah:
1. Analisis Sistem Informasi Geografis (SIG) dan Sistem Pendukung Keputusan (SPK) umumnya disajikan dalam bentuk laporan statis tanpa antarmuka interaktif yang mudah dimodifikasi oleh pemangku kepentingan.
2. Tidak adanya modul komparasi lintas metode untuk memitigasi bias algoritma tunggal.
3. Ketiadaan perencanaan validasi lapangan (*ground truth*) yang efisien, sehingga hasil perankingan seringkali sulit diverifikasi secara fisik di lapangan.

Menjawab tantangan tersebut, penelitian Hibah DIPA Unirow 2026 merekayasa sistem **WebGIS Decision Hub**, yaitu platform berbasis web modern yang mengintegrasikan ekstraksi data spasial OSM, pembobotan dinamis AHP, perankingan multi-MCDM (SAW, TOPSIS, WP), serta penyaringan rute *Pareto-TSP*.

### 1.2 Tujuan dan Manfaat Cetak Biru (Blueprint)
Dokumen cetak biru ini bertujuan untuk:
1. Mendokumentasikan secara formal arsitektur perangkat lunak berlapis (*multi-layer architecture*) dan spesifikasi aliran data (*data flow pipeline*) sistem WebGIS Decision Hub.
2. Menjadi acuan teknis bagi pengembang perangkat lunak, analis data spasial, dan akademisi dalam mengimplementasikan sistem pendukung keputusan spasial serupa.
3. Menjadi dasar bukti orisinalitas dalam perolehan perlindungan **Hak Cipta (HaKI)** pada Direktorat Jenderal Kekayaan Intelektual (DJKI) Kemenkumham RI.

### 1.3 Ruang Lingkup Sistem & Karakteristik Data
Ruang lingkup sistem mencakup kawasan perkotaan dan koridor strategis Kabupaten Tuban, Jawa Timur dengan volume data sebagai berikut:
- **200 Titik Kandidat Lokasi Kafe:** Titik-titik potensial yang tersebar di sepanjang koridor arteri, kolektor, dan lokal primer perkotaan Tuban.
- **178 Titik Kafe & Restoran Pesaing Eksisting:** Data spasial aktual dari OSM sebagai parameter kriteria kompetisi (C4).
- **528 Titik Point of Interest (POI):** Fasilitas pendorong bangkitan pengunjung (sekolah, perguruan tinggi, perbankan, perkantoran, rumah sakit, dan pusat perbelanjaan) sebagai parameter kriteria fasilitas (C7).
- **Radius Buffer Spasial:** Lingkaran jangkauan 1.000 meter berbasis proyeksi *Universal Transverse Mercator* (UTM Zone 49S / EPSG 32749).

### 1.4 Profil Pengguna Sasaran (Target Audience)
Sistem dirancang untuk melayani empat kelompok pengguna:
1. **Calon Investor & Pengusaha Kafe:** Untuk mengevaluasi kelayakan lokasi dan meminimalkan risiko modal.
2. **Pemerintah Daerah & Perencana Tata Ruang:** Sebagai instrumen penataan zonasi usaha dan pengendalian kepadatan fasilitas komersial.
3. **Tim Surveyor Lapangan:** Untuk memandu rute inspeksi fisik lokasi terpilih secara optimal.
4. **Peneliti & Mahasiswa:** Sebagai sarana eksperimen komparasi algoritma MCDM secara transparan.

---

## BAB II: LANDASAN METODOLOGI & MODEL KOMPUTASI MATEMATIS

### 2.1 Akuisisi Spasial OpenStreetMap (OSM) & Analisis Buffer
Data geospasial diekstraksi dari basis data OpenStreetMap menggunakan pustaka OSMnx / Overpass API. Untuk memastikan akurasi perhitungan jarak geodesik, seluruh koordinat lintang-bujur (*WGS 84 / EPSG 4326*) ditransformasikan ke sistem koordinat proyeksi planar **UTM Zone 49S (EPSG 32749)**. 

Setiap kandidat lokasi $i$ dianalisis menggunakan fungsi penyangga (*spatial buffer*) lingkaran beradius $R = 1.000\text{ meter}$:
$$\text{Buffer}(i) = \{ p \in \mathbb{R}^2 \mid d(p, c_i) \le 1000 \}$$
di mana $c_i$ adalah koordinat centroid lokasi kandidat dan $d(p, c_i)$ adalah jarak Euclidean pada bidang proyeksi.

### 2.2 Taksonomi 7 Kriteria Evaluasi SPK
Kriteria evaluasi disusun berdasarkan tinjauan literatur industri perhotelan dan tata ruang komersial:

| Kode | Nama Kriteria | Tipe Sifat | Satuan Ukur | Deskripsi Singkat |
| :---: | :--- | :---: | :---: | :--- |
| **C1** | Aksesibilitas Jalan | *Benefit* | Skala 1–5 | Hierarki dan lebar jalan di depan kandidat lokasi |
| **C2** | Kepadatan Penduduk Sekitar | *Benefit* | Jiwa/km² | Estimasi populasi dalam radius buffer 1.000m |
| **C3** | Biaya Sewa / Nilai Lahan | *Cost* | Juta Rp/Thn | Estimasi pengeluaran sewa lahan per tahun |
| **C4** | Jarak ke Kompetitor Terdekat | *Cost* | Meter | Jarak minimum menuju kafe pesaing OSM terdekat |
| **C5** | Ketersediaan Lahan Parkir | *Benefit* | Skala 1–5 | Estimasi kapasitas parkir roda 2 dan roda 4 |
| **C6** | Visibilitas Lokasi | *Benefit* | Skala 1–5 | Kemudahan pandang lokasi dari arah lalu lintas utama |
| **C7** | Kedekatan Fasilitas Publik (POI) | *Benefit* | Jumlah Titik | Akumulasi fasilitas pendorong dalam radius 1.000m |

### 2.3 Metode Analytical Hierarchy Process (AHP) & Rasio Konsistensi
AHP digunakan untuk menentukan bobot kepentingan relatif antar kriteria ($w_j$). Pengambil keputusan menyusun matriks perbandingan berpasangan $A = [a_{jk}]_{7 \times 7}$ menggunakan Skala Saaty (1–9).

Vektor bobot prioritas dihitung menggunakan metode normalisasi kolom dan rata-rata baris:
$$w_j = \frac{1}{n} \sum_{k=1}^n \frac{a_{jk}}{\sum_{i=1}^n a_{ik}}$$

Uji konsistensi logis dilakukan melalui perhitungan nilai eigen maksimum ($\lambda_{\max}$), *Consistency Index* ($CI$), dan *Consistency Ratio* ($CR$):
$$\lambda_{\max} = \frac{1}{n} \sum_{j=1}^n \frac{(A w)_j}{w_j}$$
$$CI = \frac{\lambda_{\max} - n}{n - 1}, \quad CR = \frac{CI}{RI}$$
Untuk matriks $n = 7$, nilai *Random Index* ($RI$) adalah 1.32. Sistem menetapkan batas toleransi $CR < 0.10$ (10%). Pada konfigurasi *baseline* penelitian ini diperoleh:
$$\lambda_{\max} = 7.02029, \quad CI = 0.00338, \quad CR = 0.00256 \text{ (0.256\% } \ll 10\%)$$
Nilai ini membuktikan tingkat konsistensi penilaian yang sangat tinggi.

### 2.4 Multi-Criteria Decision Making (MCDM)

#### A. Simple Additive Weighting (SAW)
Metode penjumlahan terbobot dengan normalisasi matriks keputusan $X = [x_{ij}]$:
$$r_{ij} = \begin{cases} \dfrac{x_{ij}}{\max_k x_{kj}}, & \text{jika kriteria } j \text{ adalah } \textit{benefit} \\[8pt] \dfrac{\min_k x_{kj}}{x_{ij}}, & \text{jika kriteria } j \text{ adalah } \textit{cost} \end{cases}$$
Skor preferensi akhir alternatif $i$:
$$V_i^{\text{SAW}} = \sum_{j=1}^n w_j \cdot r_{ij}$$

#### B. TOPSIS (AHP-TOPSIS)
Mengukur kedekatan relatif terhadap solusi ideal positif ($A^+$) dan solusi ideal negatif ($A^-$):
1. Matriks normalisasi terbobot: $v_{ij} = w_j \cdot \dfrac{x_{ij}}{\sqrt{\sum_{k=1}^m x_{kj}^2}}$
2. Jarak Euclidean solusi:
   $$D_i^+ = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^+)^2}, \quad D_i^- = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^-)^2}$$
3. Kedekatan relatif preferensi:
   $$C_i^* = \frac{D_i^-}{D_i^+ + D_i^-}, \quad 0 \le C_i^* \le 1$$

#### C. Weighted Product (WP)
Menggunakan perkalian berpangkat dengan bobot ternormalisasi ($\sum w_j = 1$):
$$S_i = \prod_{j=1}^n x_{ij}^{w_j \cdot \text{sign}(j)}, \quad \text{sign}(j) = \begin{cases} +1, & \textit{benefit} \\ -1, & \textit{cost} \end{cases}$$
$$V_i^{\text{WP}} = \frac{S_i}{\sum_{k=1}^m S_k}$$

### 2.5 Filter Pareto Optimality & Rute Survei Lapangan TSP
Untuk mereduksi alternatif yang terdominasi sebelum verifikasi fisik, diterapkan prinsip **Pareto Optimality**:
Alternatif $A$ mendominasi alternatif $B$ jika dan hanya jika:
$$\forall j \in \{1,\dots,n\}, \quad f_j(A) \ge f_j(B) \quad \land \quad \exists j \in \{1,\dots,n\}, \quad f_j(A) > f_j(B)$$
Alternatif yang masuk dalam *Pareto Frontier* (*non-dominated*) dipilih sebagai titik kunjungan survei lapangan.

Rute inspeksi fisik dimodelkan sebagai permasalahan *Traveling Salesperson Problem* (TSP) rute tertutup terpendek:
$$\min \sum_{i=1}^K \sum_{j=1}^K d_{ij} \cdot x_{ij}$$
Hasil komputasi algoritma *nearest neighbor* dan perbaikan heuristik menghasilkan rute survei sepanjang **195,44 km** yang mengoptimalkan alokasi logistik dan waktu tim peneliti.

---

## BAB III: CETAK BIRU ARSITEKTUR SISTEM (SYSTEM ARCHITECTURE BLUEPRINT)

Arsitektur WebGIS Decision Hub dirancang dengan prinsip **pemisahan perhatian (*Separation of Concerns*)** dan **komputasi sisi klien murni (*Zero-Latency Client-Side Architecture*)**. Seluruh perhitungan matematis yang rumit dieksekusi di peramban pengguna tanpa bergantung pada server API.

```
+---------------------------------------------------------------------------------------+
|                         WEBGIS DECISION HUB — LAYERED ARCHITECTURE                    |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  [ LAYER 1: PRESENTATION & UI/UX LAYER ]                                              |
|  * Semantic HTML5 Markup                                                              |
|  * CSS3 Glassmorphism Modern UI (Backdrop Filters, Dynamic Gradients, Dark/Light Mode)|
|  * Responsive Navigation & Tab Controller (Map View, AHP Matrix, MCDM Ranking)        |
|                                                                                       |
+---------------------------------------------------------------------------------------+
|                                          |                                            |
|                                          v                                            |
+---------------------------------------------------------------------------------------+
|  [ LAYER 2: INTERACTIVE SPATIAL MAP LAYER (Leaflet.js Engine) ]                       |
|  * Base Map Tiles: OpenStreetMap Standard & CartoDB Dark/Voyager                      |
|  * Multi-Layer Spatial Overlays:                                                      |
|    - 200 Kandidat Lokasi (Dynamic Color-Coded Markers by Rank)                        |
|    - 178 Kafe Eksisting Pesaing (Red Circle Markers)                                  |
|    - 528 Point of Interest Strategis (Green Diamond Markers)                          |
|  * Interactive Spatial Buffer Ring (1.000 Meter Dynamic Radius on Click)              |
|  * Popup Geometris & Info Box Kriteria Spasial                                        |
+---------------------------------------------------------------------------------------+
|                                          |                                            |
|                                          v                                            |
+---------------------------------------------------------------------------------------+
|  [ LAYER 3: ANALYTICAL & COMPUTATION ENGINE (Vanilla JavaScript Core) ]                |
|  * AHP Module (ahp.js):                                                               |
|    - 7x7 Pairwise Matrix Handler, Eigenvector Solver, Lambda Max, CI, CR Checker      |
|  * MCDM Module (mcdm.js):                                                             |
|    - SAW Processor: Linear Max/Min Normalization & Summation                          |
|    - TOPSIS Processor: Vector Normalization, Euclidean Ideal Distance, Relative Closeness|
|    - WP Processor: Power Product Exponentiation & Relative S/V Ratio                  |
|  * Pareto & TSP Module:                                                               |
|    - Non-Dominated Filtering & Coordinate Waypoint Mapping                            |
+---------------------------------------------------------------------------------------+
|                                          |                                            |
|                                          v                                            |
+---------------------------------------------------------------------------------------+
|  [ LAYER 4: DATA VISUALIZATION LAYER (Chart.js Engine) ]                              |
|  * Bump Chart: Visualisasi Pergeseran Peringkat (Ranking Fluctuation: SAW vs TOPSIS)  |
|  * Scatter Plot: Korelasi Biaya Sewa (C3) vs Kedekatan POI (C7)                       |
|  * Radar Chart: Profil Kekuatan 7 Kriteria Kandidat Terpilih                          |
|  * Bar Chart: Komparasi Distribusi Skor Top 10 Lintas Algoritma                       |
+---------------------------------------------------------------------------------------+
```

### 3.1 Tinjauan Arsitektur Berlapis (Multi-Layer Architecture)
Sistem membagi beban kerja menjadi 4 layer utama:
1. **Presentation Layer:** Mengelola antarmuka visual, tema warna, kontrol form, dan penerimaan aksi pengguna.
2. **Interactive Spatial Map Layer:** Mengelola visualisasi peta spasial, *toggling layer*, dan interaksi buffer geometris.
3. **Analytical & Computation Engine:** Jantung matematis sistem yang mengeksekusi algoritma AHP, SAW, TOPSIS, WP, dan Pareto.
4. **Data Visualization Layer:** Mengonversi data numerik tabel menjadi grafik analitik interaktif.

### 3.2 Presentation Layer (UI/UX Glassmorphism & Theme Engine)
Antarmuka dibangun dengan pendekatan *Glassmorphism* menggunakan properti CSS modern:
- `backdrop-filter: blur(12px)` untuk memberikan efek kedalaman visual yang elegan.
- CSS Custom Variables (`--bg-primary`, `--accent-color`, `--surface-card`) yang mendukung *Theme Engine* dinamis (Light Mode & Dark Mode).
- Tata letak responsif (*Mobile, Tablet, Desktop*) berbasis CSS Grid dan Flexbox.

### 3.3 Interactive Spatial Map Layer (Leaflet.js)
Modul peta (`webapp/js/map.js`) bertanggung jawab atas rendering spasial:
- Menggunakan pustaka *Leaflet.js* versi 1.9+.
- Penanda kandidat lokasi diberi kode warna dinamis berdasarkan peringkat kelayakan (Hijau = Sangat Direkomendasikan, Kuning = Sedang, Merah = Kurang Direkomendasikan).
- Saat pengguna mengeklik salah satu penanda lokasi, sistem secara otomatis menggambar lingkaran buffer beradius 1.000m dan memunculkan panel rincian 7 kriteria.

### 3.4 Analytical & Computation Engine
Komponen ini diimplementasikan menggunakan Vanilla JavaScript (ES6+) murni:
- Berkas `ahp.js`: Menangani matriks perbandingan berpasangan, verifikasi simetri ($a_{kj} = 1/a_{jk}$), ekstraksi bobot prioritas, dan uji konsistensi.
- Berkas `mcdm.js`: Menjalankan perhitungan normalisasi SAW, perhitungan solusi ideal TOPSIS, dan perkalian eksponensial WP dalam satu siklus komputasi berkecepatan tinggi (< 5 milidetik).

### 3.5 Data Visualization Layer (Chart.js)
Modul visualisasi (`webapp/js/charts.js`) mengintegrasikan *Chart.js* untuk menghasilkan:
- **Bump Chart:** Menampilkan jalur pergeseran posisi ranking kandidat antara metode SAW dan TOPSIS.
- **Scatter Plot:** Memetakan posisi 200 kandidat pada kuadran biaya sewa vs potensi fasilitas pendukung.
- **Radar Chart:** Memvisualisasikan kekuatan relatif suatu kandidat pada seluruh 7 dimensi kriteria secara simultan.

### 3.6 Karakteristik Non-Fungsional (Zero-Latency & High Portability)
1. **Zero-Latency:** Tidak ada panggilan *network request* ke backend saat pengguna memodifikasi bobot AHP. Perhitungan dilakukan seketika di memori peramban.
2. **High Portability:** Aplikasi bersifat *standalone* tanpa memerlukan database server eksternal, sehingga dapat dijalankan langsung melalui web server statis (seperti GitHub Pages) maupun secara luring (*offline*).
3. **Keamanan & Privasi:** Tidak ada data preferensi pengguna yang dikirim ke server pihak ketiga.

---

## BAB IV: SPESIFIKASI ALUR DATA SISTEM (DATA FLOW PIPELINE)

### 4.1 Diagram Konteks Alur Data (Level 0)
Diagram konteks menggambarkan interaksi antara entitas eksternal (Pengguna & OpenStreetMap) dengan sistem WebGIS Decision Hub:

```
[ OpenStreetMap (OSM) ] 
       │
       │ (Ekstraksi Koordinat & Atribut Spasial)
       ▼
+─────────────────────────────────────────────────────────────+
|                                                             |
|             WEBGIS DECISION HUB (SYSTEM ENGINE)             |
|                                                             |
+─────────────────────────────────────────────────────────────+
       ▲                                               │
       │ (Input Preferensi AHP & Filter)              │ (Peta Spasial, Ranking,
       │                                               │  Visualisasi & Rute TSP)
       │                                               ▼
[ Calon Investor / Pengambil Keputusan ]    [ Tim Surveyor Lapangan ]
```

### 4.2 Pipeline 1: Ekstraksi & Preprocessing Data Spasial OSM
1. **Input:** File konfigurasi kueri Overpass API untuk wilayah Kabupaten Tuban (tag `amenity=cafe|restaurant`, `amenity=school|university|bank|hospital|townhall`).
2. **Proses:**
   - Pembersihan data titik duplikat (*deduplication*).
   - Proyeksi koordinat geodetik ke UTM Zone 49S.
   - Perhitungan matriks jarak spasial (*nearest neighbor distance* ke kafe terdekat) dan *spatial intersection count* (jumlah POI dalam buffer 1.000m).
3. **Output:** Berkas dataset terstruktur `candidates_embedded.js` dan `osm_layers_embedded.js`.

### 4.3 Pipeline 2: Dinamika Matriks Pembobotan AHP Real-Time
1. **Input:** Skala Saaty (1–9) yang dipilih pengguna pada tabel matriks perbandingan berpasangan.
2. **Proses:**
   - Pembentukan matriks perbandingan resiprokal $A$.
   - Normalisasi kolom dan perhitungan vektor eigen rata-rata baris ($w_j$).
   - Perhitungan rasio konsistensi $CR$. Jika $CR \ge 0.10$, sistem memicu indikator peringatan inkonsistensi (*warning alert*).
3. **Output:** Vektor bobot kriteria terverifikasi $W = [w_1, w_2, \dots, w_7]$.

### 4.4 Pipeline 3: Komputasi Normalisasi & Perankingan Multi-MCDM
1. **Input:** Matriks keputusan 200 kandidat $\times$ 7 kriteria dan vektor bobot $W$.
2. **Proses:**
   - Eksekusi paralel sub-modul SAW, TOPSIS, dan Weighted Product.
   - Pengurutan (*sorting*) nilai preferensi dari nilai tertinggi ke terendah.
   - Identifikasi konsensus peringkat antar metode.
3. **Output:** Tabel perankingan komparatif Top 10, Top 15, dan pemetaan skor seluruh 200 kandidat.

### 4.5 Pipeline 4: Rekomendasi Pareto & Perencanaan Rute Validasi TSP
1. **Input:** Koordinat spasial dan skor kriteria Top kandidat.
2. **Proses:**
   - Evaluasi dominasi kriteria untuk menyaring kandidat *non-dominated* (Pareto Frontier).
   - Perhitungan matriks jarak antar titik terpilih.
   - Penyusunan rute sirkuit terpendek menggunakan TSP solver.
3. **Output:** Rute navigasi survei lapangan 195,44 km yang dirender pada layer peta navigasi.

---

## BAB V: SPESIFIKASI TEKNIS & LINGKUNGAN PENGEMBANGAN

### 5.1 Kebutuhan Perangkat Lunak & Pustaka Dependensi
1. **Bahasa Pemrograman & Markup:**
   - HTML5 Semantik (W3C Standard)
   - CSS3 (Custom Properties, Flexbox, Grid, Backdrop-Filter)
   - JavaScript (ECMAScript 2020+)
   - Python 3.10+ (untuk skrip analisis spasial awal dan solver TSP)
2. **Pustaka Pihak Ketiga (Front-End):**
   - Leaflet.js v1.9.4 (Peta Spasial Interaktif)
   - Chart.js v4.4.1 (Visualisasi Grafik Analitik)
3. **Generator Diagram Arsitektur:**
   - Archify Engine v2.17.0 (untuk pembuatan diagram arsitektur dan dataflow interaktif mandiri)

### 5.2 Kebutuhan Perangkat Keras Minimum
- **Perangkat Klien (Pengguna Akhir):**
  - Prosesor: Dual Core 1.8 GHz atau lebih tinggi.
  - Memori RAM: Minimal 2 GB (Direkomendasikan 4 GB).
  - Layar: Resolusi minimal 1366 $\times$ 768 piksel (Mendukung tampilan *mobile responsif*).
  - Peramban Web: Google Chrome, Mozilla Firefox, Microsoft Edge, atau Safari versi terbaru dengan dukungan JavaScript aktif.

### 5.3 Prosedur Deployment & Pengujian Sistem
- **Deployment Produksi:** Diterapkan melalui GitHub Pages dengan SSL/TLS otomatis (*HTTPS*) pada URL:  
  `https://andyharyoko.github.io/PenelitianDIPA2026/`
- **Pengujian Fungsional (Black-Box Testing):**
  - Uji akurasi kalkulator AHP terhadap tabel Saaty standar: **Tervalidasi 100% Akurat**.
  - Uji konsistensi perhitungan ranking SAW, TOPSIS, dan WP terhadap perhitungan manual spreadsheet: **Deviasi < 0,0001%**.
  - Uji responsivitas UI dan rendering 906 titik spasial: **Waktu muat rata-rata < 1,2 detik**.

---

## BAB VI: KESIMPULAN & ARAHAN PENGEMBANGAN

Cetak biru arsitektur sistem dan spesifikasi alur data ini telah merumuskan secara komprehensif rancang bangun platform **WebGIS Decision Hub**. Integrasi data spasial terbuka OpenStreetMap, pembobotan dinamis AHP, komparasi multi-metode MCDM, dan optimasi rute validasi TSP berhasil diwujudkan dalam arsitektur perangkat lunak yang elegan, cepat (*zero latency*), dan mudah diakses.

Arahan pengembangan pada iterasi sistem selanjutnya meliputi:
1. Penambahan integrasi data lalu lintas dinamis (*real-time traffic data*) berbasis sensor IoT / API pihak ketiga.
2. Fitur ekspor laporan otomatis dalam format PDF berstandar perbankan untuk mempermudah pengajuan proposal modal usaha bagi UMKM.
3. Pengembangan algoritma optimasi rute multi-kendaraan (*Vehicle Routing Problem* / VRP) untuk tim survei yang beranggotakan lebih dari satu kelompok.

---

## DAFTAR PUSTAKA

1. Haryoko, A., Uripno, G., & Syahrial, M. F. (2026). Pareto-TSP Decision Support Framework for Cafe Location Selection in Tuban Regency. *Riemann: Research of Mathematics and Mathematics Education*, 8(2), 720–734.
2. Saaty, T. L. (2008). Decision making with the analytic hierarchy process. *International Journal of Services Sciences*, 1(1), 83–98.
3. Hwang, C. L., & Yoon, K. (1981). *Multiple Attribute Decision Making: Methods and Applications*. Springer-Verlag, Berlin/New York.
4. Boeing, G. (2017). OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks. *Computers, Environment and Urban Systems*, 65, 126–139.
5. Malczewski, J. (2006). GIS-based multicriteria decision analysis: a survey of the literature. *International Journal of Geographical Information Science*, 20(7), 703–726.
6. Pressman, R. S., & Maxim, B. R. (2020). *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill Education.

---

## LAMPIRAN VISUAL DOKUMENTASI ARSITEKTUR & DATAFLOW

1. **Diagram Arsitektur Sistem WebGIS (Archify):**  
   Tautan Publik: [https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_architecture.html](https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_architecture.html)  
   Berkas Sumber: `webapp/diagrams/webapp_architecture.html`

2. **Diagram Pipeline Alur Data Spasial & Keputusan (Archify):**  
   Tautan Publik: [https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_dataflow.html](https://andyharyoko.github.io/PenelitianDIPA2026/diagrams/webapp_dataflow.html)  
   Berkas Sumber: `webapp/diagrams/webapp_dataflow.html`

3. **Repositori Publik & Kode Sumber Sistem:**  
   GitHub: [https://github.com/andyharyoko/PenelitianDIPA2026](https://github.com/andyharyoko/PenelitianDIPA2026)

---
*Dokumen ini merupakan bagian dari luaran wajib Penelitian Hibah DIPA Universitas PGRI Ronggolawe (Unirow) Tuban Tahun Anggaran 2026.*
