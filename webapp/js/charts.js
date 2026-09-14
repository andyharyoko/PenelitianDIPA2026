/**
 * CHARTS CONTROLLER (Chart.js)
 * Visualisasi Data SPK: Radar Kriteria, Bar Chart Komparasi Top 10,
 * Scatter Correlation, dan Bump Chart Perubahan Peringkat.
 */

class ChartsController {
    constructor() {
        this.radarChart = null;
        this.barChart = null;
        this.scatterChart = null;
        this.bumpChart = null;
    }

    /**
     * Inisialisasi atau update Bar Chart komparasi Top 10 antar metode
     */
    renderTop10BarChart(canvasId, sawList, topsisList, wpList) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (this.barChart) {
            this.barChart.destroy();
        }

        // Ambil himpunan kode lokasi unik dari Top 5 masing-masing metode
        const top5Codes = Array.from(new Set([
            ...sawList.slice(0, 5).map(x => x.Kode_Lokasi),
            ...topsisList.slice(0, 5).map(x => x.Kode_Lokasi),
            ...wpList.slice(0, 5).map(x => x.Kode_Lokasi)
        ]));

        const labels = top5Codes.map(code => {
            const found = sawList.find(x => x.Kode_Lokasi === code) || topsisList.find(x => x.Kode_Lokasi === code);
            return `${code} (${found.Area})`;
        });

        // Skor dinormalisasi ke skala 0 - 100% untuk komparabilitas visual
        const sawScores = top5Codes.map(code => {
            const item = sawList.find(x => x.Kode_Lokasi === code);
            return item ? (item.score * 100).toFixed(1) : 0;
        });

        const topsisScores = top5Codes.map(code => {
            const item = topsisList.find(x => x.Kode_Lokasi === code);
            return item ? (item.score * 100).toFixed(1) : 0;
        });

        // WP skor biasanya kecil (vektor V sum=1 across 200 items -> avg 0.005),
        // dinormalisasikan relatif terhadap max WP agar sebanding
        const maxWP = Math.max(...wpList.map(x => x.score));
        const wpScores = top5Codes.map(code => {
            const item = wpList.find(x => x.Kode_Lokasi === code);
            return item ? ((item.score / maxWP) * 100).toFixed(1) : 0;
        });

        this.barChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'SAW (Skor %)',
                        data: sawScores,
                        backgroundColor: 'rgba(79, 70, 229, 0.85)',
                        borderColor: '#4f46e5',
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: 'TOPSIS (Preferensi %)',
                        data: topsisScores,
                        backgroundColor: 'rgba(245, 158, 11, 0.85)',
                        borderColor: '#f59e0b',
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: 'WP (Indeks Relatif %)',
                        data: wpScores,
                        backgroundColor: 'rgba(16, 185, 129, 0.85)',
                        borderColor: '#10b981',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { family: 'Inter', size: 12, weight: '600' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%`
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Inter', size: 11 } }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: { display: true, text: 'Skor Relatif (0 - 100%)', font: { family: 'Inter', weight: 'bold' } },
                        grid: { color: 'rgba(203, 213, 225, 0.4)' }
                    }
                }
            }
        });
    }

    /**
     * Render Radar Chart Profil 7 Kriteria untuk Kandidat Tertentu
     */
    renderRadarProfile(canvasId, candidate, allCandidates, criteriaDefs) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (this.radarChart) {
            this.radarChart.destroy();
        }

        // Hitung rata-rata tiap kriteria dari seluruh 200 kandidat untuk pembanding
        const avgCriteria = {};
        const maxCriteria = {};
        criteriaDefs.forEach(c => {
            const sum = allCandidates.reduce((acc, row) => acc + Number(row[c.code]), 0);
            avgCriteria[c.code] = sum / allCandidates.length;
            maxCriteria[c.code] = Math.max(...allCandidates.map(row => Number(row[c.code])));
        });

        // Normalisasi ke persentase 0 - 100% terhadap nilai maksimum kriteria
        const labels = criteriaDefs.map(c => c.label);
        const candidateNormValues = criteriaDefs.map(c => {
            const val = Number(candidate[c.code]);
            const max = maxCriteria[c.code];
            // Untuk cost (C4, C5), nilai lebih kecil berarti performa lebih baik (dibalik 1 - ratio)
            if (c.type === 'cost') {
                const min = Math.min(...allCandidates.map(row => Number(row[c.code])));
                return Number(((min / Math.max(1, val)) * 100).toFixed(1));
            }
            return Number(((val / Math.max(1, max)) * 100).toFixed(1));
        });

        const avgNormValues = criteriaDefs.map(c => {
            const avg = avgCriteria[c.code];
            const max = maxCriteria[c.code];
            if (c.type === 'cost') {
                const min = Math.min(...allCandidates.map(row => Number(row[c.code])));
                return Number(((min / Math.max(1, avg)) * 100).toFixed(1));
            }
            return Number(((avg / Math.max(1, max)) * 100).toFixed(1));
        });

        this.radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: `${candidate.Kode_Lokasi} (${candidate.Area})`,
                        data: candidateNormValues,
                        backgroundColor: 'rgba(79, 70, 229, 0.25)',
                        borderColor: '#4f46e5',
                        borderWidth: 2.5,
                        pointBackgroundColor: '#4f46e5',
                        pointBorderColor: '#fff',
                        pointRadius: 4
                    },
                    {
                        label: 'Rata-Rata 200 Kandidat',
                        data: avgNormValues,
                        backgroundColor: 'rgba(148, 163, 184, 0.15)',
                        borderColor: '#94a3b8',
                        borderWidth: 1.5,
                        borderDash: [4, 4],
                        pointRadius: 3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { font: { family: 'Inter', size: 12, weight: '600' } }
                    }
                },
                scales: {
                    r: {
                        angleLines: { color: 'rgba(203, 213, 225, 0.6)' },
                        grid: { color: 'rgba(203, 213, 225, 0.6)' },
                        pointLabels: {
                            font: { family: 'Inter', size: 11, weight: 'bold' }
                        },
                        suggestedMin: 0,
                        suggestedMax: 100,
                        ticks: { stepSize: 20, font: { size: 9 } }
                    }
                }
            }
        });
    }

    /**
     * Render Scatter Correlation Plot (SAW vs TOPSIS / SAW vs WP / TOPSIS vs WP)
     */
    renderScatterCorrelation(canvasId, mergedCandidates, type = 'saw_topsis') {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (this.scatterChart) {
            this.scatterChart.destroy();
        }

        let xLabel = 'Skor SAW';
        let yLabel = 'Skor TOPSIS';
        let pointColor = '#4f46e5';

        const dataPoints = mergedCandidates.map(c => {
            let x = c.Skor_SAW;
            let y = c.Skor_TOPSIS;

            if (type === 'saw_wp') {
                x = c.Skor_SAW;
                y = c.Skor_WP * 1000;
                xLabel = 'Skor SAW';
                yLabel = 'Skor WP (x1000)';
                pointColor = '#10b981';
            } else if (type === 'topsis_wp') {
                x = c.Skor_TOPSIS;
                y = c.Skor_WP * 1000;
                xLabel = 'Skor TOPSIS';
                yLabel = 'Skor WP (x1000)';
                pointColor = '#f59e0b';
            }

            return {
                x: Number(x.toFixed(4)),
                y: Number(y.toFixed(4)),
                candidate: c
            };
        });

        this.scatterChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: `Korelasi ${xLabel} vs ${yLabel}`,
                    data: dataPoints,
                    backgroundColor: pointColor,
                    borderColor: '#ffffff',
                    borderWidth: 1,
                    pointRadius: 5,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (ctx) => {
                                const c = ctx.raw.candidate;
                                return `${c.Kode_Lokasi} - ${c.Nama_Lokasi}: (X=${ctx.raw.x}, Y=${ctx.raw.y})`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: { display: true, text: xLabel, font: { family: 'Inter', weight: 'bold' } },
                        grid: { color: 'rgba(203, 213, 225, 0.4)' }
                    },
                    y: {
                        title: { display: true, text: yLabel, font: { family: 'Inter', weight: 'bold' } },
                        grid: { color: 'rgba(203, 213, 225, 0.4)' }
                    }
                }
            }
        });
    }

    /**
     * Render Bump Chart / Slopegraph Pergeseran Peringkat Top 15
     */
    renderBumpChart(canvasId, mergedCandidates) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return;

        if (this.bumpChart) {
            this.bumpChart.destroy();
        }

        // Ambil Top 15 dari salah satu metode
        const top15 = mergedCandidates
            .filter(c => c.Rank_SAW <= 12 || c.Rank_TOPSIS <= 12 || c.Rank_WP <= 12)
            .slice(0, 12);

        const colors = [
            '#4f46e5', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6',
            '#06b6d4', '#ec4899', '#f97316', '#84cc16', '#64748b',
            '#14b8a6', '#6366f1'
        ];

        const datasets = top15.map((c, idx) => {
            const col = colors[idx % colors.length];
            return {
                label: `${c.Kode_Lokasi} (${c.Nama_Lokasi.split('(')[0].trim()})`,
                data: [c.Rank_SAW, c.Rank_TOPSIS, c.Rank_WP],
                borderColor: col,
                backgroundColor: col,
                fill: false,
                tension: 0.2,
                borderWidth: 2.5,
                pointRadius: 5,
                pointHoverRadius: 8
            };
        });

        this.bumpChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Metode SAW', 'Metode TOPSIS', 'Metode WP'],
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { boxWidth: 12, font: { family: 'Inter', size: 10 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => `${ctx.dataset.label}: Rank #${ctx.raw}`
                        }
                    }
                },
                scales: {
                    y: {
                        reverse: true, // Rank 1 di paling atas!
                        title: { display: true, text: 'Peringkat (Lebih ke atas = Lebih unggul)', font: { family: 'Inter', weight: 'bold' } },
                        ticks: { stepSize: 5 },
                        grid: { color: 'rgba(203, 213, 225, 0.4)' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Inter', size: 12, weight: 'bold' } }
                    }
                }
            }
        });
    }
}
