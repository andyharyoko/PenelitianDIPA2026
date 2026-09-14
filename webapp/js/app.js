/**
 * MAIN APP CONTROLLER
 * Mengelola navigasi tab, inisialisasi data, interaksi AHP, filter tabel, dan modal radar
 */

class AppController {
    constructor() {
        this.candidates = [];
        this.criteria = CRITERIA_DEFINITIONS;
        this.ahpEngine = null;
        this.mcdmEngine = null;
        this.mapController = null;
        this.chartsController = null;
        this.currentTab = 'overview';
        this.currentRankingMethod = 'all'; // 'all', 'saw', 'topsis', 'wp'
        this.selectedCandidate = null;

        // Sorting & pagination state untuk tabel overview & ranking
        this.overviewSearchQuery = '';
        this.overviewSortCol = 'Kode_Lokasi';
        this.overviewSortAsc = true;

        this.rankingSearchQuery = '';
        this.rankingSortCol = 'Rank_SAW';
        this.rankingSortAsc = true;
    }

    async init() {
        console.log("[App] Inisialisasi Sistem Pendukung Keputusan Lokasi Kafe...");

        // 1. Inisialisasi Sub-Controller
        this.ahpEngine = new AHPEngine(this.criteria);
        this.chartsController = new ChartsController();

        // 2. Load Dataset 200 Kandidat
        try {
            this.candidates = await loadCandidatesData();
            document.getElementById('loading-overlay').style.display = 'none';
        } catch (e) {
            console.error("[App] Gagal memuat data:", e);
            document.getElementById('loading-overlay').innerHTML = `
                <div class="loading-box error">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <h3>Gagal Memuat Dataset</h3>
                    <p>${e.message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Muat Ulang</button>
                </div>
            `;
            return;
        }

        // 3. Inisialisasi MCDM Engine
        const ahpWeights = this.ahpEngine.getWeights();
        this.mcdmEngine = new MCDMEngine(this.candidates, this.criteria, ahpWeights);
        this.mcdmResults = this.mcdmEngine.runAll();

        // 4. Inisialisasi Map Controller (setelah DOM siap)
        this.mapController = new MapController('leaflet-map');
        this.mapController.renderData(this.mcdmResults.mergedCandidates);

        // 5. Render Seluruh Komponen Antarmuka
        this.renderStatsBanner();
        this.renderOverviewTable();
        this.renderAHPSection();
        this.renderRankingTable();
        this.renderComparisonSection();
        this.renderTop10Cards();
        this.setupEventListeners();

        console.log("[App] Aplikasi SPK berhasil dimuat dan siap digunakan.");
    }

    /**
     * Update Banner Statistik Utama di Header
     */
    renderStatsBanner() {
        const res = this.mcdmResults;
        const topSAW = res.saw.rankedList[0];
        const topTOPSIS = res.topsis.rankedList[0];
        const topWP = res.wp.rankedList[0];
        const ahp = this.ahpEngine.getResults();

        document.getElementById('stat-total-candidates').innerText = this.candidates.length;
        document.getElementById('stat-top-saw').innerText = `${topSAW.Kode_Lokasi} (${topSAW.score.toFixed(3)})`;
        document.getElementById('stat-top-topsis').innerText = `${topTOPSIS.Kode_Lokasi} (${topTOPSIS.score.toFixed(3)})`;
        document.getElementById('stat-top-wp').innerText = `${topWP.Kode_Lokasi} (${(topWP.score * 1000).toFixed(2)}‰)`;
        document.getElementById('stat-ahp-cr').innerText = `${(ahp.cr * 100).toFixed(2)}% (${ahp.isConsistent ? 'Konsisten' : 'Revisi'})`;
        document.getElementById('stat-triple-winners').innerText = `${res.comparison.consensusTop10.tripleWinners.length} Lokasi`;
    }

    /**
     * 1. TAB OVERVIEW DATASET 200 KANDIDAT
     */
    renderOverviewTable() {
        const tbody = document.getElementById('overview-table-body');
        if (!tbody) return;

        let data = [...this.candidates];

        // Search filter
        if (this.overviewSearchQuery) {
            const q = this.overviewSearchQuery.toLowerCase();
            data = data.filter(c =>
                c.Kode_Lokasi.toLowerCase().includes(q) ||
                c.Nama_Lokasi.toLowerCase().includes(q) ||
                c.Area.toLowerCase().includes(q)
            );
        }

        // Sorting
        data.sort((a, b) => {
            let valA = a[this.overviewSortCol];
            let valB = b[this.overviewSortCol];
            if (typeof valA === 'string') {
                return this.overviewSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return this.overviewSortAsc ? valA - valB : valB - valA;
        });

        document.getElementById('overview-count-label').innerText = `Menampilkan ${data.length} dari ${this.candidates.length} kandidat`;

        let html = '';
        data.forEach(c => {
            html += `
                <tr>
                    <td><span class="badge badge-code">${c.Kode_Lokasi}</span></td>
                    <td class="font-medium">${c.Nama_Lokasi}</td>
                    <td><span class="badge badge-area">${c.Area}</span></td>
                    <td>${Number(c.Lat).toFixed(4)}, ${Number(c.Lon).toFixed(4)}</td>
                    <td class="text-center font-bold text-indigo">${c.C1_Aksesibilitas}</td>
                    <td class="text-center">${c.C2_Kepadatan_Penduduk.toLocaleString()}</td>
                    <td class="text-center">${c.C3_Infrastruktur}</td>
                    <td class="text-center font-bold text-cost">${c.C4_Kompetitor}</td>
                    <td class="text-center font-bold text-cost">Rp ${c.C5_Biaya_Sewa} Jt</td>
                    <td class="text-center">${c.C6_Demografi_Usia_Produktif}%</td>
                    <td class="text-center font-bold text-emerald">${c.C7_Kedekatan_POI}</td>
                    <td class="text-center">
                        <button class="btn-sm btn-outline" onclick="window.app.showCandidateModal('${c.Kode_Lokasi}')">
                            <i class="fa-solid fa-chart-pie"></i> Detail
                        </button>
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html || `<tr><td colspan="12" class="text-center py-4 text-muted">Tidak ada data yang cocok dengan pencarian.</td></tr>`;
    }

    /**
     * 2. TAB AHP & MATRIKS KONSISTENSI
     */
    renderAHPSection() {
        const ahp = this.ahpEngine.getResults();

        // 1. Header Metrics Card
        document.getElementById('ahp-lambda-max').innerText = ahp.lambdaMax.toFixed(5);
        document.getElementById('ahp-ci').innerText = ahp.ci.toFixed(5);
        document.getElementById('ahp-ri').innerText = ahp.ri.toFixed(2);
        
        const crEl = document.getElementById('ahp-cr-badge');
        crEl.innerText = `CR = ${(ahp.cr * 100).toFixed(3)}% (${ahp.isConsistent ? 'KONSISTEN < 10%' : 'TIDAK KONSISTEN'})`;
        crEl.className = `status-badge ${ahp.isConsistent ? 'consistent' : 'inconsistent'}`;

        // 2. Matriks Perbandingan Berpasangan Table
        const matrixThead = document.getElementById('ahp-matrix-thead');
        const matrixTbody = document.getElementById('ahp-matrix-tbody');

        let theadHtml = `<tr><th>Kriteria</th>`;
        this.criteria.forEach(c => {
            theadHtml += `<th title="${c.name}">${c.label}</th>`;
        });
        theadHtml += `<th>Bobot (w)</th><th>%</th></tr>`;
        matrixThead.innerHTML = theadHtml;

        let tbodyHtml = '';
        for (let i = 0; i < ahp.n; i++) {
            tbodyHtml += `<tr><td class="row-header"><b>${this.criteria[i].label}</b></td>`;
            for (let j = 0; j < ahp.n; j++) {
                const val = ahp.matrix[i][j];
                const formatted = AHPEngine.formatSaatyValue(val);
                if (i === j) {
                    tbodyHtml += `<td class="cell-diag">1</td>`;
                } else if (i < j) {
                    tbodyHtml += `
                        <td class="cell-editable">
                            <select class="saaty-select" onchange="window.app.handleMatrixChange(${i}, ${j}, this.value)">
                                <option value="1" ${Math.abs(val - 1) < 0.05 ? 'selected' : ''}>1</option>
                                <option value="2" ${Math.abs(val - 2) < 0.05 ? 'selected' : ''}>2</option>
                                <option value="3" ${Math.abs(val - 3) < 0.05 ? 'selected' : ''}>3</option>
                                <option value="4" ${Math.abs(val - 4) < 0.05 ? 'selected' : ''}>4</option>
                                <option value="5" ${Math.abs(val - 5) < 0.05 ? 'selected' : ''}>5</option>
                                <option value="6" ${Math.abs(val - 6) < 0.05 ? 'selected' : ''}>6</option>
                                <option value="7" ${Math.abs(val - 7) < 0.05 ? 'selected' : ''}>7</option>
                                <option value="8" ${Math.abs(val - 8) < 0.05 ? 'selected' : ''}>8</option>
                                <option value="9" ${Math.abs(val - 9) < 0.05 ? 'selected' : ''}>9</option>
                                <option value="0.5" ${Math.abs(val - 0.5) < 0.05 ? 'selected' : ''}>1/2</option>
                                <option value="0.3333" ${Math.abs(val - 1/3) < 0.05 ? 'selected' : ''}>1/3</option>
                                <option value="0.25" ${Math.abs(val - 0.25) < 0.05 ? 'selected' : ''}>1/4</option>
                                <option value="0.2" ${Math.abs(val - 0.2) < 0.05 ? 'selected' : ''}>1/5</option>
                                <option value="0.1667" ${Math.abs(val - 1/6) < 0.05 ? 'selected' : ''}>1/6</option>
                                <option value="0.1429" ${Math.abs(val - 1/7) < 0.05 ? 'selected' : ''}>1/7</option>
                                <option value="0.125" ${Math.abs(val - 1/8) < 0.05 ? 'selected' : ''}>1/8</option>
                                <option value="0.1111" ${Math.abs(val - 1/9) < 0.05 ? 'selected' : ''}>1/9</option>
                            </select>
                        </td>
                    `;
                } else {
                    tbodyHtml += `<td class="cell-reciprocal">${formatted}</td>`;
                }
            }
            tbodyHtml += `
                <td class="cell-weight font-bold">${ahp.weights[i].toFixed(4)}</td>
                <td class="cell-weight-pct">${(ahp.weights[i] * 100).toFixed(2)}%</td>
            </tr>`;
        }
        matrixTbody.innerHTML = tbodyHtml;

        // 3. Render Bobot Bar Kriteria
        const weightsContainer = document.getElementById('ahp-weights-bars');
        let barsHtml = '';
        ahp.criteriaWeights.forEach(cw => {
            const isCost = cw.type === 'cost';
            barsHtml += `
                <div class="weight-bar-item">
                    <div class="weight-bar-header">
                        <span class="weight-name">
                            <b>${cw.label}</b> (${cw.name})
                            <span class="badge-type ${isCost ? 'cost' : 'benefit'}">${cw.type.toUpperCase()}</span>
                        </span>
                        <span class="weight-val"><b>${cw.weightPercentage.toFixed(2)}%</b> (w = ${cw.weight.toFixed(4)})</span>
                    </div>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill ${isCost ? 'fill-cost' : 'fill-benefit'}" style="width: ${Math.min(100, cw.weightPercentage * 3.5)}%"></div>
                    </div>
                </div>
            `;
        });
        weightsContainer.innerHTML = barsHtml;
    }

    /**
     * Handler saat nilai matriks AHP diubah oleh user
     */
    handleMatrixChange(row, col, value) {
        this.ahpEngine.updateCell(row, col, parseFloat(value));
        const newWeights = this.ahpEngine.getWeights();

        // Hitung ulang seluruh metode MCDM
        this.mcdmEngine.setWeights(newWeights);
        this.mcdmResults = this.mcdmEngine.runAll();

        // Refresh seluruh view terkait
        this.renderStatsBanner();
        this.renderAHPSection();
        this.renderRankingTable();
        this.renderComparisonSection();
        this.renderTop10Cards();
        this.mapController.renderData(this.mcdmResults.mergedCandidates);

        // Jika tab aktif saat ini adalah komparasi atau top10, perbarui grafiknya
        if (this.currentTab === 'top10') {
            this.chartsController.renderTop10BarChart(
                'chart-top10-comparison',
                this.mcdmResults.saw.rankedList,
                this.mcdmResults.topsis.rankedList,
                this.mcdmResults.wp.rankedList
            );
        } else if (this.currentTab === 'comparison') {
            this.updateComparisonCharts();
        }
    }

    resetAHPMatrix() {
        this.ahpEngine.resetToDefault();
        const newWeights = this.ahpEngine.getWeights();
        this.mcdmEngine.setWeights(newWeights);
        this.mcdmResults = this.mcdmEngine.runAll();

        this.renderStatsBanner();
        this.renderAHPSection();
        this.renderRankingTable();
        this.renderComparisonSection();
        this.renderTop10Cards();
        this.mapController.renderData(this.mcdmResults.mergedCandidates);
    }

    /**
     * 3. TAB HASIL PERANGKINGAN (SAW, TOPSIS, WP)
     */
    renderRankingTable() {
        const tbody = document.getElementById('ranking-table-body');
        if (!tbody) return;

        let data = [...this.mcdmResults.mergedCandidates];

        // Filter search
        if (this.rankingSearchQuery) {
            const q = this.rankingSearchQuery.toLowerCase();
            data = data.filter(c =>
                c.Kode_Lokasi.toLowerCase().includes(q) ||
                c.Nama_Lokasi.toLowerCase().includes(q) ||
                c.Area.toLowerCase().includes(q)
            );
        }

        // Sorting
        data.sort((a, b) => {
            let valA = a[this.rankingSortCol];
            let valB = b[this.rankingSortCol];
            if (typeof valA === 'string') {
                return this.rankingSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
            }
            return this.rankingSortAsc ? valA - valB : valB - valA;
        });

        document.getElementById('ranking-count-label').innerText = `Menampilkan ${data.length} dari ${this.candidates.length} kandidat`;

        let html = '';
        data.forEach(c => {
            const isTop10SAW = c.Rank_SAW <= 10;
            const isTop10TOPSIS = c.Rank_TOPSIS <= 10;
            const isTop10WP = c.Rank_WP <= 10;

            let consensusBadge = '';
            if (c.top10Count === 3) {
                consensusBadge = `<span class="badge badge-consensus-triple" title="Top 10 di semua 3 metode!"><i class="fa-solid fa-crown"></i> Triple #10</span>`;
            } else if (c.top10Count === 2) {
                consensusBadge = `<span class="badge badge-consensus-double" title="Top 10 di 2 metode"><i class="fa-solid fa-star"></i> Double #10</span>`;
            }

            html += `
                <tr>
                    <td><span class="badge badge-code">${c.Kode_Lokasi}</span></td>
                    <td class="font-medium">${c.Nama_Lokasi}</td>
                    <td><span class="badge badge-area">${c.Area}</span></td>
                    
                    <!-- SAW -->
                    <td class="text-center ${isTop10SAW ? 'bg-rank-top' : ''}">
                        <span class="rank-pill rank-saw">#${c.Rank_SAW}</span>
                    </td>
                    <td class="text-center font-mono">${c.Skor_SAW.toFixed(4)}</td>

                    <!-- TOPSIS -->
                    <td class="text-center ${isTop10TOPSIS ? 'bg-rank-top' : ''}">
                        <span class="rank-pill rank-topsis">#${c.Rank_TOPSIS}</span>
                    </td>
                    <td class="text-center font-mono">${c.Skor_TOPSIS.toFixed(4)}</td>

                    <!-- WP -->
                    <td class="text-center ${isTop10WP ? 'bg-rank-top' : ''}">
                        <span class="rank-pill rank-wp">#${c.Rank_WP}</span>
                    </td>
                    <td class="text-center font-mono">${(c.Skor_WP * 1000).toFixed(3)}‰</td>

                    <td class="text-center">${consensusBadge || '<span class="text-muted">-</span>'}</td>
                    <td class="text-center">
                        <button class="btn-sm btn-outline" onclick="window.app.showCandidateModal('${c.Kode_Lokasi}')">
                            <i class="fa-solid fa-chart-pie"></i>
                        </button>
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html || `<tr><td colspan="11" class="text-center py-4 text-muted">Tidak ada data yang cocok.</td></tr>`;
    }

    /**
     * 4. TAB KOMPARASI METODE
     */
    renderComparisonSection() {
        const comp = this.mcdmResults.comparison;

        // Spearman Rank Correlations
        document.getElementById('corr-spearman-saw-topsis').innerText = comp.spearman.saw_topsis.toFixed(4);
        document.getElementById('corr-spearman-saw-wp').innerText = comp.spearman.saw_wp.toFixed(4);
        document.getElementById('corr-spearman-topsis-wp').innerText = comp.spearman.topsis_wp.toFixed(4);

        // Pearson Score Correlations
        document.getElementById('corr-pearson-saw-topsis').innerText = comp.pearson.saw_topsis.toFixed(4);
        document.getElementById('corr-pearson-saw-wp').innerText = comp.pearson.saw_wp.toFixed(4);
        document.getElementById('corr-pearson-topsis-wp').innerText = comp.pearson.topsis_wp.toFixed(4);

        // Consensus summary badges
        const tripleListEl = document.getElementById('consensus-triple-list');
        let tripleHtml = '';
        comp.consensusTop10.tripleWinners.forEach(code => {
            const cand = this.candidates.find(c => c.Kode_Lokasi === code);
            const m = this.mcdmResults.mergedCandidates.find(c => c.Kode_Lokasi === code);
            tripleHtml += `
                <div class="consensus-winner-card" onclick="window.app.showCandidateModal('${code}')">
                    <div class="winner-head">
                        <span class="badge badge-code">${code}</span>
                        <span class="crown-icon"><i class="fa-solid fa-crown"></i></span>
                    </div>
                    <h4>${cand.Nama_Lokasi}</h4>
                    <div class="ranks-row">
                        <span class="rank-saw">SAW #${m.Rank_SAW}</span>
                        <span class="rank-topsis">TOPSIS #${m.Rank_TOPSIS}</span>
                        <span class="rank-wp">WP #${m.Rank_WP}</span>
                    </div>
                </div>
            `;
        });
        tripleListEl.innerHTML = tripleHtml || '<p class="text-muted">Tidak ada kandidat triple winner.</p>';

        this.updateComparisonCharts();
    }

    updateComparisonCharts() {
        this.chartsController.renderBumpChart('chart-bump', this.mcdmResults.mergedCandidates);
        this.chartsController.renderScatterCorrelation(
            'chart-scatter',
            this.mcdmResults.mergedCandidates,
            document.getElementById('scatter-type-select') ? document.getElementById('scatter-type-select').value : 'saw_topsis'
        );
    }

    /**
     * 5. TAB TOP 10 REKOMENDASI SPASIAL & KARTU KOMPARASI
     */
    renderTop10Cards() {
        const sawTop10 = this.mcdmResults.saw.rankedList.slice(0, 10);
        const topsisTop10 = this.mcdmResults.topsis.rankedList.slice(0, 10);
        const wpTop10 = this.mcdmResults.wp.rankedList.slice(0, 10);

        const renderList = (list, containerId, methodClass, scoreFormatter) => {
            const container = document.getElementById(containerId);
            if (!container) return;

            let html = '';
            list.forEach(item => {
                const cand = this.mcdmResults.mergedCandidates.find(c => c.Kode_Lokasi === item.Kode_Lokasi);
                html += `
                    <div class="top10-item-card ${cand.top10Count >= 2 ? 'consensus-card' : ''}" onclick="window.app.focusCandidateOnMap(${cand.Lat}, ${cand.Lon}, '${cand.Kode_Lokasi}')">
                        <div class="top10-rank-badge ${methodClass}">${item.rank}</div>
                        <div class="top10-info">
                            <div class="top10-header">
                                <span class="top10-code">${item.Kode_Lokasi}</span>
                                <span class="top10-score">${scoreFormatter(item.score)}</span>
                            </div>
                            <div class="top10-name">${item.Nama_Lokasi}</div>
                            <div class="top10-meta">
                                <span><i class="fa-solid fa-shop"></i> C4: ${cand.C4_Kompetitor}</span>
                                <span><i class="fa-solid fa-location-dot"></i> C7: ${cand.C7_Kedekatan_POI}</span>
                                <span><i class="fa-solid fa-coins"></i> Rp ${cand.C5_Biaya_Sewa}Jt</span>
                            </div>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        };

        renderList(sawTop10, 'top10-saw-container', 'badge-saw', s => `Skor: ${s.toFixed(4)}`);
        renderList(topsisTop10, 'top10-topsis-container', 'badge-topsis', s => `C*: ${s.toFixed(4)}`);
        renderList(wpTop10, 'top10-wp-container', 'badge-wp', s => `V: ${(s * 1000).toFixed(2)}‰`);

        // Render Bar Chart Komparasi Top 10
        this.chartsController.renderTop10BarChart(
            'chart-top10-comparison',
            this.mcdmResults.saw.rankedList,
            this.mcdmResults.topsis.rankedList,
            this.mcdmResults.wp.rankedList
        );
    }

    focusCandidateOnMap(lat, lon, code) {
        // Pindah ke tab peta jika belum
        this.switchTab('top10');
        this.mapController.focusCandidate(lat, lon, 16);
    }

    /**
     * MODAL DETAIL KANDIDAT & RADAR CHART
     */
    showCandidateModal(code) {
        const cand = this.mcdmResults.mergedCandidates.find(c => c.Kode_Lokasi === code);
        if (!cand) return;

        this.selectedCandidate = cand;

        document.getElementById('modal-candidate-code').innerText = cand.Kode_Lokasi;
        document.getElementById('modal-candidate-name').innerText = cand.Nama_Lokasi;
        document.getElementById('modal-candidate-area').innerText = cand.Area;
        document.getElementById('modal-candidate-coords').innerText = `${Number(cand.Lat).toFixed(6)}, ${Number(cand.Lon).toFixed(6)}`;

        // Ranks
        document.getElementById('modal-rank-saw').innerText = `#${cand.Rank_SAW} (${cand.Skor_SAW.toFixed(4)})`;
        document.getElementById('modal-rank-topsis').innerText = `#${cand.Rank_TOPSIS} (${cand.Skor_TOPSIS.toFixed(4)})`;
        document.getElementById('modal-rank-wp').innerText = `#${cand.Rank_WP} (${(cand.Skor_WP * 1000).toFixed(3)}‰)`;

        // Criteria Table
        const tbody = document.getElementById('modal-criteria-tbody');
        let html = '';
        this.criteria.forEach(c => {
            const isCost = c.type === 'cost';
            html += `
                <tr>
                    <td><b>${c.label}</b></td>
                    <td>${c.name}</td>
                    <td><span class="badge-type ${isCost ? 'cost' : 'benefit'}">${c.type.toUpperCase()}</span></td>
                    <td class="text-center font-bold">${cand[c.code]}</td>
                    <td class="text-center text-muted">${c.unit}</td>
                </tr>
            `;
        });
        tbody.innerHTML = html;

        // Tampilkan Modal
        const modal = document.getElementById('candidate-modal');
        modal.classList.add('active');

        // Render Radar Chart
        setTimeout(() => {
            this.chartsController.renderRadarProfile(
                'chart-radar-modal',
                cand,
                this.candidates,
                this.criteria
            );
        }, 100);
    }

    closeModal() {
        const modal = document.getElementById('candidate-modal');
        modal.classList.remove('active');
    }

    /**
     * Tab Routing
     */
    switchTab(tabName) {
        this.currentTab = tabName;

        // Update nav links
        document.querySelectorAll('.nav-tab').forEach(el => {
            el.classList.toggle('active', el.dataset.tab === tabName);
        });

        // Update tab contents
        document.querySelectorAll('.tab-pane').forEach(el => {
            el.classList.toggle('active', el.id === `tab-${tabName}`);
        });

        // Handle tab-specific redraws
        if (tabName === 'top10') {
            this.mapController.invalidateSize();
            this.chartsController.renderTop10BarChart(
                'chart-top10-comparison',
                this.mcdmResults.saw.rankedList,
                this.mcdmResults.topsis.rankedList,
                this.mcdmResults.wp.rankedList
            );
        } else if (tabName === 'comparison') {
            setTimeout(() => this.updateComparisonCharts(), 100);
        }
    }

    /**
     * Export Hasil MCDM ke CSV / JSON
     */
    exportData(format = 'csv') {
        const data = this.mcdmResults.mergedCandidates;
        if (format === 'json') {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `hasil_spk_200_kafe_tuban.json`;
            a.click();
        } else {
            // CSV
            const headers = [
                'Kode_Lokasi', 'Nama_Lokasi', 'Area', 'Lat', 'Lon',
                'C1_Aksesibilitas', 'C2_Kepadatan_Penduduk', 'C3_Infrastruktur',
                'C4_Kompetitor', 'C5_Biaya_Sewa', 'C6_Demografi_Usia_Produktif', 'C7_Kedekatan_POI',
                'Skor_SAW', 'Rank_SAW', 'Skor_TOPSIS', 'Rank_TOPSIS', 'Skor_WP', 'Rank_WP'
            ];
            const rows = data.map(row => headers.map(h => `"${row[h]}"`).join(','));
            const csvContent = [headers.join(','), ...rows].join('\n');

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `hasil_spk_200_kafe_tuban.csv`;
            a.click();
        }
    }

    /**
     * Map Layer Controls (200 Kandidat, 178 Kafe OSM, 528 POI OSM, Top 10)
     */
    handleLayerToggle(layerKey, isChecked) {
        if (this.mapController) {
            this.mapController.toggleLayer(layerKey, isChecked);
        }
    }

    applyMapPreset(presetName) {
        if (this.mapController) {
            this.mapController.applyPreset(presetName);

            // Update status tombol preset aktif
            document.querySelectorAll('.btn-preset').forEach(btn => {
                btn.classList.remove('active');
            });
            const activeBtn = Array.from(document.querySelectorAll('.btn-preset')).find(b => b.getAttribute('onclick')?.includes(presetName));
            if (activeBtn) activeBtn.classList.add('active');
        }
    }

    /**
     * Setup Event Listeners
     */
    setupEventListeners() {
        // Tab Navigation
        document.querySelectorAll('.nav-tab').forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchTab(btn.dataset.tab);
            });
        });

        // Overview Search
        const searchInput = document.getElementById('overview-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.overviewSearchQuery = e.target.value;
                this.renderOverviewTable();
            });
        }

        // Ranking Search
        const rankSearchInput = document.getElementById('ranking-search');
        if (rankSearchInput) {
            rankSearchInput.addEventListener('input', (e) => {
                this.rankingSearchQuery = e.target.value;
                this.renderRankingTable();
            });
        }

        // Scatter type change
        const scatterSelect = document.getElementById('scatter-type-select');
        if (scatterSelect) {
            scatterSelect.addEventListener('change', (e) => {
                this.chartsController.renderScatterCorrelation(
                    'chart-scatter',
                    this.mcdmResults.mergedCandidates,
                    e.target.value
                );
            });
        }

        // Map Top 10 filter buttons (All, SAW, TOPSIS, WP, Consensus)
        document.querySelectorAll('.btn-map-filter').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.btn-map-filter').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                if (this.mapController) {
                    this.mapController.layerState.top10 = true;
                    this.mapController.layerState.top10Type = btn.dataset.filter;
                    this.mapController.syncMapLayers();
                }
            });
        });

        // Theme Toggle (Dark / Light)
        const themeBtn = document.getElementById('theme-toggle-btn');
        if (themeBtn) {
            themeBtn.addEventListener('click', () => {
                document.body.classList.toggle('dark-mode');
                const isDark = document.body.classList.contains('dark-mode');
                themeBtn.innerHTML = isDark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
                localStorage.setItem('spk_theme', isDark ? 'dark' : 'light');
            });

            // Restore saved theme
            if (localStorage.getItem('spk_theme') === 'dark') {
                document.body.classList.add('dark-mode');
                themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
            }
        }

        // Modal Close on backdrop click
        const modal = document.getElementById('candidate-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) this.closeModal();
            });
        }
    }
}

// Inisialisasi saat window load
window.addEventListener('DOMContentLoaded', () => {
    window.app = new AppController();
    window.app.init();
});
