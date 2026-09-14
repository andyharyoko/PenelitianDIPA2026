/**
 * MAP CONTROLLER (Leaflet.js)
 * Visualisasi Spasial Komprehensif:
 * 1. 200 Kandidat Lokasi Kafe (dengan buffer radius 1.000 meter)
 * 2. 178 Titik Kafe & Restoran Riil dari OpenStreetMap (OSM)
 * 3. 528 Titik POI (Fasilitas Pendidikan, Kesehatan, Mall, Perbankan, Kantor) dari OSM
 * 4. Peringkat 10 Lokasi Terbaik (SAW, TOPSIS, WP, Konsensus)
 */

class MapController {
    constructor(mapContainerId = 'leaflet-map') {
        this.containerId = mapContainerId;
        this.map = null;
        this.layers = {
            candidates200: L.layerGroup(),
            osmCafes: L.layerGroup(),
            osmPois: L.layerGroup(),
            top10SAW: L.layerGroup(),
            top10TOPSIS: L.layerGroup(),
            top10WP: L.layerGroup(),
            consensus: L.layerGroup(),
            bufferGroup: L.layerGroup()
        };

        // State filter toggle layer
        this.layerState = {
            candidates200: true,
            osmCafes: true,
            osmPois: true,
            top10: true,
            top10Type: 'all' // 'all', 'saw', 'topsis', 'wp', 'consensus'
        };

        this.initMap();
    }

    initMap() {
        const centerTuban = [-6.8950, 112.0500];

        this.map = L.map(this.containerId, {
            center: centerTuban,
            zoom: 13,
            zoomControl: true,
            scrollWheelZoom: true
        });

        // Basemaps
        const osmStandard = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        });

        const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: 'Tiles &copy; Esri'
        });

        osmStandard.addTo(this.map);

        const baseMaps = {
            "OpenStreetMap Standar (Aktif)": osmStandard,
            "Citra Satelit Esri": esriSatellite
        };

        L.control.layers(baseMaps, null, { position: 'topright' }).addTo(this.map);

        // Tambahkan buffer layer group ke map
        this.map.addLayer(this.layers.bufferGroup);
    }

    /**
     * Membuat SVG custom marker pin dengan nomor peringkat
     */
    createCustomMarkerIcon(number, color, isConsensus = false) {
        const iconHtml = `
            <div class="custom-pin-wrapper ${isConsensus ? 'consensus-pin' : ''}">
                <div class="custom-pin" style="background-color: ${color};">
                    <span class="pin-number">${isConsensus ? '★' : number}</span>
                </div>
                <div class="pin-pulse" style="background-color: ${color};"></div>
            </div>
        `;

        return L.divIcon({
            className: 'custom-leaflet-marker',
            html: iconHtml,
            iconSize: [32, 42],
            iconAnchor: [16, 40],
            popupAnchor: [0, -38]
        });
    }

    /**
     * Gambar buffer lingkaran 1.000m di sekitar kandidat untuk memvisualisasikan C4 dan C7
     */
    drawCandidateBuffer(lat, lon, candidate) {
        this.layers.bufferGroup.clearLayers();

        const circle = L.circle([lat, lon], {
            radius: 1000,
            color: '#4f46e5',
            weight: 2,
            dashArray: '6, 6',
            fillColor: '#4f46e5',
            fillOpacity: 0.08
        });

        circle.bindTooltip(`<b>Buffer 1 km:</b> ${candidate.Nama_Lokasi}<br>Kompetitor: ${candidate.C4_Kompetitor} | POI: ${candidate.C7_Kedekatan_POI}`, {
            sticky: true
        });

        this.layers.bufferGroup.addLayer(circle);
    }

    /**
     * Render data 200 kandidat, Top 10, dan layer OSM riil
     */
    renderData(mergedCandidates) {
        // Bersihkan layer kandidat
        this.layers.candidates200.clearLayers();
        this.layers.top10SAW.clearLayers();
        this.layers.top10TOPSIS.clearLayers();
        this.layers.top10WP.clearLayers();
        this.layers.consensus.clearLayers();

        const colorSAW = '#4f46e5';     // Indigo
        const colorTOPSIS = '#f59e0b';  // Amber Gold
        const colorWP = '#10b981';      // Emerald Green
        const colorConsensus = '#8b5cf6'; // Royal Purple

        mergedCandidates.forEach(c => {
            const lat = Number(c.Lat);
            const lon = Number(c.Lon);
            if (isNaN(lat) || isNaN(lon)) return;

            const popupContent = this.generatePopupContent(c);

            // 1. Layer 200 Kandidat (Circle Marker Halus Warna Hijau Zamrud)
            const circle = L.circleMarker([lat, lon], {
                radius: 6,
                fillColor: '#10b981',
                color: '#ffffff',
                weight: 2,
                opacity: 0.9,
                fillOpacity: 0.75
            }).bindPopup(popupContent);

            circle.on('click', () => {
                this.drawCandidateBuffer(lat, lon, c);
            });

            circle.bindTooltip(`<b>${c.Kode_Lokasi}</b> - ${c.Nama_Lokasi}<br><span style="font-size:0.75rem; color:#64748b;">Klik untuk tampilkan buffer 1km</span>`);
            this.layers.candidates200.addLayer(circle);

            // 2. Layer Top 10 SAW
            if (c.Rank_SAW <= 10) {
                const icon = this.createCustomMarkerIcon(c.Rank_SAW, colorSAW);
                const marker = L.marker([lat, lon], { icon }).bindPopup(popupContent);
                marker.on('click', () => this.drawCandidateBuffer(lat, lon, c));
                this.layers.top10SAW.addLayer(marker);
            }

            // 3. Layer Top 10 TOPSIS
            if (c.Rank_TOPSIS <= 10) {
                const icon = this.createCustomMarkerIcon(c.Rank_TOPSIS, colorTOPSIS);
                const marker = L.marker([lat, lon], { icon }).bindPopup(popupContent);
                marker.on('click', () => this.drawCandidateBuffer(lat, lon, c));
                this.layers.top10TOPSIS.addLayer(marker);
            }

            // 4. Layer Top 10 WP
            if (c.Rank_WP <= 10) {
                const icon = this.createCustomMarkerIcon(c.Rank_WP, colorWP);
                const marker = L.marker([lat, lon], { icon }).bindPopup(popupContent);
                marker.on('click', () => this.drawCandidateBuffer(lat, lon, c));
                this.layers.top10WP.addLayer(marker);
            }

            // 5. Layer Consensus (Triple / Double Winner)
            if (c.top10Count >= 2) {
                const icon = this.createCustomMarkerIcon(c.Rank_SAW, colorConsensus, true);
                const marker = L.marker([lat, lon], { icon }).bindPopup(popupContent);
                marker.on('click', () => this.drawCandidateBuffer(lat, lon, c));
                this.layers.consensus.addLayer(marker);
            }
        });

        // Muat layer OSM (178 Kafe dan 528 POI)
        this.renderOSMLayers();
        this.syncMapLayers();
    }

    /**
     * Render layer data spasial OpenStreetMap (178 Kafe/Restoran dan 528 POI)
     */
    renderOSMLayers() {
        this.layers.osmCafes.clearLayers();
        this.layers.osmPois.clearLayers();

        // 1. Kafe & Restoran Nyata (178 titik)
        const cafes = window.OSM_CAFES || [];
        cafes.forEach(cafe => {
            const lat = Number(cafe.lat);
            const lon = Number(cafe.lon);
            if (isNaN(lat) || isNaN(lon)) return;

            const popup = `
                <div class="map-popup-card osm-popup">
                    <div class="popup-header">
                        <span class="badge" style="background:#fee2e2; color:#ef4444; font-weight:700;">
                            <i class="fa-solid fa-mug-saucer"></i> Kafe / Resto Riil (OSM)
                        </span>
                        <h4 class="popup-title" style="margin-top:4px;">${cafe.name}</h4>
                        <span class="popup-area"><i class="fa-solid fa-tag"></i> Tipe: ${cafe.type}</span>
                    </div>
                    <p style="font-size:0.8rem; color:var(--text-secondary); margin:4px 0;">
                        Kompetitor riil dari OpenStreetMap Kabupaten Tuban yang dihitung pada kriteria <b>C4 (Kompetitor)</b>.
                    </p>
                    <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">
                        Koordinat: ${lat.toFixed(5)}, ${lon.toFixed(5)}
                    </div>
                </div>
            `;

            const marker = L.circleMarker([lat, lon], {
                radius: 4.5,
                fillColor: '#ef4444', // Merah Ruby
                color: '#ffffff',
                weight: 1.5,
                opacity: 0.9,
                fillOpacity: 0.75
            }).bindPopup(popup).bindTooltip(`<b>[Kafe/Resto OSM]</b> ${cafe.name}`);

            this.layers.osmCafes.addLayer(marker);
        });

        // 2. POI / Fasilitas Umum Nyata (528 titik)
        const pois = window.OSM_POIS || [];
        pois.forEach(poi => {
            const lat = Number(poi.lat);
            const lon = Number(poi.lon);
            if (isNaN(lat) || isNaN(lon)) return;

            const popup = `
                <div class="map-popup-card osm-popup">
                    <div class="popup-header">
                        <span class="badge" style="background:#e0f2fe; color:#0284c7; font-weight:700;">
                            <i class="fa-solid fa-building-columns"></i> POI Penunjang (OSM)
                        </span>
                        <h4 class="popup-title" style="margin-top:4px;">${poi.name}</h4>
                        <span class="popup-area"><i class="fa-solid fa-layer-group"></i> Kategori: ${poi.category}</span>
                    </div>
                    <p style="font-size:0.8rem; color:var(--text-secondary); margin:4px 0;">
                        Fasilitas minat (sekolah, kampus, bank, mall, kantor) dari OSM Tuban yang dihitung pada kriteria <b>C7 (Kedekatan POI)</b>.
                    </p>
                    <div style="font-size:0.7rem; color:var(--text-muted); font-family:var(--font-mono); margin-top:4px;">
                        Koordinat: ${lat.toFixed(5)}, ${lon.toFixed(5)}
                    </div>
                </div>
            `;

            const marker = L.circleMarker([lat, lon], {
                radius: 3.5,
                fillColor: '#0284c7', // Biru Cyan
                color: '#ffffff',
                weight: 1.2,
                opacity: 0.85,
                fillOpacity: 0.65
            }).bindPopup(popup).bindTooltip(`<b>[POI OSM]</b> ${poi.name} (${poi.category})`);

            this.layers.osmPois.addLayer(marker);
        });

        console.log(`[Map] OSM Layers rendered: ${cafes.length} Kafe & Resto, ${pois.length} POI.`);
    }

    /**
     * Sinkronisasi layer pada map berdasarkan status checklist pengguna
     */
    syncMapLayers() {
        // 1. Layer 200 Kandidat
        if (this.layerState.candidates200) {
            if (!this.map.hasLayer(this.layers.candidates200)) this.map.addLayer(this.layers.candidates200);
        } else {
            if (this.map.hasLayer(this.layers.candidates200)) this.map.removeLayer(this.layers.candidates200);
        }

        // 2. Layer 178 Kafe & Resto OSM
        if (this.layerState.osmCafes) {
            if (!this.map.hasLayer(this.layers.osmCafes)) this.map.addLayer(this.layers.osmCafes);
        } else {
            if (this.map.hasLayer(this.layers.osmCafes)) this.map.removeLayer(this.layers.osmCafes);
        }

        // 3. Layer 528 POI OSM
        if (this.layerState.osmPois) {
            if (!this.map.hasLayer(this.layers.osmPois)) this.map.addLayer(this.layers.osmPois);
        } else {
            if (this.map.hasLayer(this.layers.osmPois)) this.map.removeLayer(this.layers.osmPois);
        }

        // 4. Layer Top 10 Markers
        const top10Layers = [this.layers.top10SAW, this.layers.top10TOPSIS, this.layers.top10WP, this.layers.consensus];
        top10Layers.forEach(l => {
            if (this.map.hasLayer(l)) this.map.removeLayer(l);
        });

        if (this.layerState.top10) {
            const type = this.layerState.top10Type;
            if (type === 'all') {
                this.map.addLayer(this.layers.top10SAW);
                this.map.addLayer(this.layers.top10TOPSIS);
                this.map.addLayer(this.layers.top10WP);
            } else if (type === 'saw') {
                this.map.addLayer(this.layers.top10SAW);
            } else if (type === 'topsis') {
                this.map.addLayer(this.layers.top10TOPSIS);
            } else if (type === 'wp') {
                this.map.addLayer(this.layers.top10WP);
            } else if (type === 'consensus') {
                this.map.addLayer(this.layers.consensus);
            }
        }
    }

    /**
     * Toggle layer spesifik (on/off)
     */
    toggleLayer(layerKey, isEnabled) {
        if (this.layerState.hasOwnProperty(layerKey)) {
            this.layerState[layerKey] = isEnabled;
            this.syncMapLayers();
        }
    }

    /**
     * Terapkan preset filter (Semua, Kandidat vs Kafe, Kandidat vs POI, dll)
     */
    applyPreset(presetName) {
        if (presetName === 'all') {
            this.layerState.candidates200 = true;
            this.layerState.osmCafes = true;
            this.layerState.osmPois = true;
            this.layerState.top10 = true;
            this.layerState.top10Type = 'all';
        } else if (presetName === 'candidates_cafes') {
            this.layerState.candidates200 = true;
            this.layerState.osmCafes = true;
            this.layerState.osmPois = false;
            this.layerState.top10 = false;
        } else if (presetName === 'candidates_pois') {
            this.layerState.candidates200 = true;
            this.layerState.osmCafes = false;
            this.layerState.osmPois = true;
            this.layerState.top10 = false;
        } else if (presetName === 'candidates_only') {
            this.layerState.candidates200 = true;
            this.layerState.osmCafes = false;
            this.layerState.osmPois = false;
            this.layerState.top10 = false;
        } else if (presetName === 'cafes_only') {
            this.layerState.candidates200 = false;
            this.layerState.osmCafes = true;
            this.layerState.osmPois = false;
            this.layerState.top10 = false;
        } else if (presetName === 'pois_only') {
            this.layerState.candidates200 = false;
            this.layerState.osmCafes = false;
            this.layerState.osmPois = true;
            this.layerState.top10 = false;
        } else if (presetName === 'top10_only') {
            this.layerState.candidates200 = true;
            this.layerState.osmCafes = true;
            this.layerState.osmPois = false;
            this.layerState.top10 = true;
            this.layerState.top10Type = 'all';
        }

        this.syncCheckboxesUI();
        this.syncMapLayers();
    }

    syncCheckboxesUI() {
        const cCand = document.getElementById('chk-layer-candidates');
        const cCafe = document.getElementById('chk-layer-cafes');
        const cPoi = document.getElementById('chk-layer-pois');
        const cTop = document.getElementById('chk-layer-top10');

        if (cCand) cCand.checked = this.layerState.candidates200;
        if (cCafe) cCafe.checked = this.layerState.osmCafes;
        if (cPoi) cPoi.checked = this.layerState.osmPois;
        if (cTop) cTop.checked = this.layerState.top10;
    }

    /**
     * Template Popup Interaktif Leaflet untuk Kandidat
     */
    generatePopupContent(c) {
        const gmapsLink = `https://www.google.com/maps?q=${c.Lat},${c.Lon}`;

        let consensusBadge = '';
        if (c.top10Count === 3) {
            consensusBadge = `<div class="popup-consensus-badge triple"><i class="fa-solid fa-crown"></i> Triple Winner (Top 10 di 3 Metode)</div>`;
        } else if (c.top10Count === 2) {
            consensusBadge = `<div class="popup-consensus-badge double"><i class="fa-solid fa-star"></i> Double Winner (Top 10 di 2 Metode)</div>`;
        }

        return `
            <div class="map-popup-card">
                <div class="popup-header">
                    <span class="popup-code">${c.Kode_Lokasi}</span>
                    <h4 class="popup-title">${c.Nama_Lokasi}</h4>
                    <span class="popup-area"><i class="fa-solid fa-location-dot"></i> ${c.Area}</span>
                </div>
                ${consensusBadge}
                <div class="popup-ranks-grid">
                    <div class="rank-badge-item saw">
                        <span class="rank-name">SAW</span>
                        <span class="rank-val">#${c.Rank_SAW}</span>
                        <span class="score-val">${c.Skor_SAW.toFixed(3)}</span>
                    </div>
                    <div class="rank-badge-item topsis">
                        <span class="rank-name">TOPSIS</span>
                        <span class="rank-val">#${c.Rank_TOPSIS}</span>
                        <span class="score-val">${c.Skor_TOPSIS.toFixed(3)}</span>
                    </div>
                    <div class="rank-badge-item wp">
                        <span class="rank-name">WP</span>
                        <span class="rank-val">#${c.Rank_WP}</span>
                        <span class="score-val">${(c.Skor_WP * 1000).toFixed(2)}‰</span>
                    </div>
                </div>
                <div class="popup-criteria-list">
                    <div class="crit-row"><span><i class="fa-solid fa-circle text-cost"></i> C4 Kompetitor (OSM 1km):</span> <b>${c.C4_Kompetitor} unit</b></div>
                    <div class="crit-row"><span><i class="fa-solid fa-circle text-emerald"></i> C7 Kedekatan POI (OSM 1km):</span> <b>${c.C7_Kedekatan_POI} POI</b></div>
                    <div class="crit-row"><span><i class="fa-solid fa-coins"></i> C5 Biaya Sewa:</span> <b>Rp ${c.C5_Biaya_Sewa} Jt/thn</b></div>
                    <div class="crit-row"><span><i class="fa-solid fa-road"></i> C1 Aksesibilitas:</span> <b>${c.C1_Aksesibilitas} / 10</b></div>
                </div>
                <div class="popup-actions">
                    <button class="btn-popup-radar" onclick="window.app.showCandidateModal('${c.Kode_Lokasi}')">
                        <i class="fa-solid fa-chart-pie"></i> Radar Kriteria
                    </button>
                    <a href="${gmapsLink}" target="_blank" class="btn-popup-gmaps" title="Buka di Google Maps">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
            </div>
        `;
    }

    focusCandidate(lat, lon, zoom = 14.5) {
        const cand = window.app.mcdmResults.mergedCandidates.find(c => Math.abs(c.Lat - lat) < 0.0001 && Math.abs(c.Lon - lon) < 0.0001);
        if (cand) {
            this.drawCandidateBuffer(lat, lon, cand);
        }

        this.map.flyTo([lat, lon], zoom, {
            animate: true,
            duration: 1.2
        });
    }

    invalidateSize() {
        if (this.map) {
            setTimeout(() => this.map.invalidateSize(), 300);
        }
    }
}
