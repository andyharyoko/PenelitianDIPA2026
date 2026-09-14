/**
 * DATA DEFINITIONS & CANDIDATE LOADER
 * Geo-Decision Support System: Optimasi Pemilihan Lokasi Kafe di Tuban
 */

const CRITERIA_DEFINITIONS = [
    {
        code: 'C1_Aksesibilitas',
        label: 'C1 - Aksesibilitas',
        name: 'Aksesibilitas Jalan & Transportasi',
        type: 'benefit',
        unit: 'Skala 1-10',
        desc: 'Kemudahan akses jalan utama, lebar jalan, dan kemudahan parkir bagi pengunjung.'
    },
    {
        code: 'C2_Kepadatan_Penduduk',
        label: 'C2 - Kepadatan Penduduk',
        name: 'Kepadatan Penduduk Sekitar',
        type: 'benefit',
        unit: 'jiwa/km²',
        desc: 'Tingkat konsentrasi penduduk di sekitar lokasi sebagai potensi basis pelanggan.'
    },
    {
        code: 'C3_Infrastruktur',
        label: 'C3 - Infrastruktur',
        name: 'Kesiapan Infrastruktur',
        type: 'benefit',
        unit: 'Skala 1-10',
        desc: 'Ketersediaan jaringan listrik stabil, air bersih, sanitasi, dan sinyal internet broadband.'
    },
    {
        code: 'C4_Kompetitor',
        label: 'C4 - Kompetisi',
        name: 'Jumlah Kafe & Restoran (Radius 1km OSM)',
        type: 'cost',
        unit: 'Unit usaha',
        desc: 'Kepadatan kafe dan restoran pesaing dalam radius 1.000m dari OpenStreetMap. Semakin tinggi semakin jenuh.'
    },
    {
        code: 'C5_Biaya_Sewa',
        label: 'C5 - Biaya Sewa',
        name: 'Estimasi Biaya Sewa Lahan/Bangunan',
        type: 'cost',
        unit: 'Juta Rp/thn',
        desc: 'Beban operasional tahunan sewa lokasi. Nilai lebih rendah lebih menguntungkan.'
    },
    {
        code: 'C6_Demografi_Usia_Produktif',
        label: 'C6 - Usia Produktif',
        name: 'Persentase Usia Produktif',
        type: 'benefit',
        unit: '% (15-35 thn)',
        desc: 'Persentase populasi usia muda/produktif (pelajar, mahasiswa, pekerja muda) yang menjadi target kafe.'
    },
    {
        code: 'C7_Kedekatan_POI',
        label: 'C7 - Kedekatan POI',
        name: 'Fasilitas Minat / POI (Radius 1km OSM)',
        type: 'benefit',
        unit: 'Titik POI',
        desc: 'Jumlah fasilitas penunjang (kampus, sekolah, perbankan, perkantoran, pusat perbelanjaan) dari OSM.'
    }
];

// Saaty Random Consistency Index (RI)
const SAATY_RI = {
    1: 0.0,
    2: 0.0,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49
};

// Default Pairwise Comparison Matrix (Skala Saaty 1-9)
// C1, C2, C3, C4, C5, C6, C7
const DEFAULT_AHP_MATRIX = [
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], // C1
    [2.0, 1.0, 2.0, 1.0, 1/2, 2.0, 1/2], // C2
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], // C3
    [2.0, 1.0, 2.0, 1.0, 1/2, 2.0, 1/2], // C4
    [3.0, 2.0, 3.0, 2.0, 1.0, 3.0, 1.0], // C5
    [1.0, 1/2, 1.0, 1/2, 1/3, 1.0, 1/3], // C6
    [3.0, 2.0, 3.0, 2.0, 1.0, 3.0, 1.0]  // C7
];

let rawCandidatesData = [];

/**
 * Memuat data 200 kandidat dari file JSON dengan graceful fallback
 */
async function loadCandidatesData() {
    try {
        const res = await fetch('data/kandidat_200.json');
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        rawCandidatesData = await res.json();
        console.log(`[DataLoader] Berhasil memuat ${rawCandidatesData.length} kandidat dari JSON.`);
        return rawCandidatesData;
    } catch (err) {
        console.warn(`[DataLoader] Gagal memuat data/kandidat_200.json secara langsung (${err.message}). Mencoba fallback...`);
        if (window.EMBEDDED_CANDIDATES && window.EMBEDDED_CANDIDATES.length > 0) {
            rawCandidatesData = window.EMBEDDED_CANDIDATES;
            console.log(`[DataLoader] Fallback loaded: ${rawCandidatesData.length} kandidat.`);
            return rawCandidatesData;
        }
        throw err;
    }
}
