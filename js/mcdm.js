/**
 * MCDM (Multi-Criteria Decision Making) Engine
 * Menghitung metode SAW, TOPSIS, dan WP menggunakan Bobot Prioritas AHP,
 * serta analisis statistik perbandingan antar metode.
 */

class MCDMEngine {
    constructor(candidates, criteria, ahpWeights) {
        this.candidates = candidates;
        this.criteria = criteria;
        this.weights = ahpWeights; // Array bobot berurutan C1-C7
        this.results = null;
    }

    setWeights(weights) {
        this.weights = weights;
    }

    setCandidates(candidates) {
        this.candidates = candidates;
    }

    /**
     * Menjalankan seluruh komputasi (SAW, TOPSIS, WP, dan Komparasi)
     */
    runAll() {
        if (!this.candidates || this.candidates.length === 0) return null;

        const saw = this.calculateSAW();
        const topsis = this.calculateTOPSIS();
        const wp = this.calculateWP();
        const comparison = this.calculateComparison(saw, topsis, wp);

        // Gabungkan seluruh hasil ranking ke masing-masing objek kandidat
        const mergedCandidates = this.candidates.map((cand, idx) => {
            const sawItem = saw.rankedList.find(item => item.Kode_Lokasi === cand.Kode_Lokasi);
            const topsisItem = topsis.rankedList.find(item => item.Kode_Lokasi === cand.Kode_Lokasi);
            const wpItem = wp.rankedList.find(item => item.Kode_Lokasi === cand.Kode_Lokasi);

            return {
                ...cand,
                Skor_SAW: sawItem.score,
                Rank_SAW: sawItem.rank,
                Skor_TOPSIS: topsisItem.score,
                Rank_TOPSIS: topsisItem.rank,
                Skor_WP: wpItem.score,
                Rank_WP: wpItem.rank,
                Vektor_S_WP: wpItem.vectorS,
                // Hitung konsensus top 10
                isTop10SAW: sawItem.rank <= 10,
                isTop10TOPSIS: topsisItem.rank <= 10,
                isTop10WP: wpItem.rank <= 10,
                top10Count: (sawItem.rank <= 10 ? 1 : 0) + (topsisItem.rank <= 10 ? 1 : 0) + (wpItem.rank <= 10 ? 1 : 0),
                avgRank: (sawItem.rank + topsisItem.rank + wpItem.rank) / 3,
                maxRankDelta: Math.max(
                    Math.abs(sawItem.rank - topsisItem.rank),
                    Math.abs(sawItem.rank - wpItem.rank),
                    Math.abs(topsisItem.rank - wpItem.rank)
                )
            };
        });

        this.results = {
            saw,
            topsis,
            wp,
            comparison,
            mergedCandidates
        };

        return this.results;
    }

    /**
     * 1. METODE SAW (Simple Additive Weighting)
     */
    calculateSAW() {
        const n = this.candidates.length;
        const cols = this.criteria.map(c => c.code);
        const types = this.criteria.map(c => c.type);

        // Cari Nilai Maksimum dan Minimum per Kriteria
        const maxVals = {};
        const minVals = {};
        cols.forEach(col => {
            maxVals[col] = Math.max(...this.candidates.map(c => Number(c[col])));
            minVals[col] = Math.min(...this.candidates.map(c => Number(c[col])));
        });

        // Matriks Normalisasi (R) & Skor Preferensi (V)
        const normalizedMatrix = [];
        const rankedList = this.candidates.map((cand, i) => {
            let score = 0;
            const normRow = {};

            cols.forEach((col, j) => {
                const val = Number(cand[col]);
                let r_ij = 0;
                if (types[j] === 'benefit') {
                    r_ij = maxVals[col] !== 0 ? val / maxVals[col] : 0;
                } else { // cost
                    r_ij = val !== 0 ? minVals[col] / val : 0;
                }
                normRow[col] = r_ij;
                score += r_ij * this.weights[j];
            });

            normalizedMatrix.push(normRow);

            return {
                Kode_Lokasi: cand.Kode_Lokasi,
                Nama_Lokasi: cand.Nama_Lokasi,
                Area: cand.Area,
                Lat: cand.Lat,
                Lon: cand.Lon,
                score: score,
                rawCriteria: { ...cand },
                normCriteria: normRow
            };
        });

        // Urutkan berdasarkan Skor Tertinggi
        rankedList.sort((a, b) => b.score - a.score);
        rankedList.forEach((item, idx) => { item.rank = idx + 1; });

        return {
            name: "Simple Additive Weighting (SAW)",
            rankedList,
            maxVals,
            minVals,
            normalizedMatrix
        };
    }

    /**
     * 2. METODE TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
     */
    calculateTOPSIS() {
        const n = this.candidates.length;
        const cols = this.criteria.map(c => c.code);
        const types = this.criteria.map(c => c.type);

        // 1. Pembagi Normalisasi Vektor Euclidean: sqrt(sum(x_ij^2))
        const denominators = {};
        cols.forEach(col => {
            const sumSq = this.candidates.reduce((acc, c) => acc + Math.pow(Number(c[col]), 2), 0);
            denominators[col] = Math.sqrt(sumSq) || 1e-9;
        });

        // 2. Matriks Ternormalisasi Terbobot (Y)
        const weightedMatrix = [];
        this.candidates.forEach(cand => {
            const rowY = {};
            cols.forEach((col, j) => {
                const r_ij = Number(cand[col]) / denominators[col];
                rowY[col] = r_ij * this.weights[j];
            });
            weightedMatrix.push(rowY);
        });

        // 3. Solusi Ideal Positif (A+) dan Solusi Ideal Negatif (A-)
        const idealPos = {};
        const idealNeg = {};
        cols.forEach((col, j) => {
            const colVals = weightedMatrix.map(row => row[col]);
            if (types[j] === 'benefit') {
                idealPos[col] = Math.max(...colVals);
                idealNeg[col] = Math.min(...colVals);
            } else { // cost
                idealPos[col] = Math.min(...colVals);
                idealNeg[col] = Math.max(...colVals);
            }
        });

        // 4. Jarak Euclidean (D+ & D-) dan Skor Preferensi (C*)
        const rankedList = this.candidates.map((cand, i) => {
            const rowY = weightedMatrix[i];
            let sumDistPosSq = 0;
            let sumDistNegSq = 0;

            cols.forEach(col => {
                sumDistPosSq += Math.pow(rowY[col] - idealPos[col], 2);
                sumDistNegSq += Math.pow(rowY[col] - idealNeg[col], 2);
            });

            const dPos = Math.sqrt(sumDistPosSq);
            const dNeg = Math.sqrt(sumDistNegSq);
            const score = (dPos + dNeg) !== 0 ? dNeg / (dPos + dNeg) : 0;

            return {
                Kode_Lokasi: cand.Kode_Lokasi,
                Nama_Lokasi: cand.Nama_Lokasi,
                Area: cand.Area,
                Lat: cand.Lat,
                Lon: cand.Lon,
                score: score,
                dPos: dPos,
                dNeg: dNeg,
                rawCriteria: { ...cand },
                weightedRow: rowY
            };
        });

        // Urutkan berdasarkan Skor Tertinggi
        rankedList.sort((a, b) => b.score - a.score);
        rankedList.forEach((item, idx) => { item.rank = idx + 1; });

        return {
            name: "TOPSIS (AHP-TOPSIS)",
            rankedList,
            denominators,
            idealPos,
            idealNeg,
            weightedMatrix
        };
    }

    /**
     * 3. METODE WP (Weighted Product)
     */
    calculateWP() {
        const cols = this.criteria.map(c => c.code);
        const types = this.criteria.map(c => c.type);

        // Normalisasi Bobot Kriteria agar Total = 1
        const totalWeight = this.weights.reduce((acc, w) => acc + w, 0);
        const normWeights = this.weights.map(w => w / (totalWeight || 1));

        // Tentukan Pangkat Kriteria (+w untuk benefit, -w untuk cost)
        const powers = types.map((t, idx) => t === 'benefit' ? normWeights[idx] : -normWeights[idx]);

        // Hitung Vektor S_i = prod( x_ij ^ powers_j )
        const vectorSList = [];
        let totalS = 0;

        this.candidates.forEach(cand => {
            let s_i = 1.0;
            cols.forEach((col, j) => {
                const val = Math.max(1e-6, Number(cand[col]));
                s_i *= Math.pow(val, powers[j]);
            });
            vectorSList.push(s_i);
            totalS += s_i;
        });

        // Hitung Nilai Vektor Preferensi Relatif V_i = S_i / sum(S)
        const rankedList = this.candidates.map((cand, i) => {
            const s_i = vectorSList[i];
            const v_i = totalS !== 0 ? s_i / totalS : 0;

            return {
                Kode_Lokasi: cand.Kode_Lokasi,
                Nama_Lokasi: cand.Nama_Lokasi,
                Area: cand.Area,
                Lat: cand.Lat,
                Lon: cand.Lon,
                score: v_i,
                vectorS: s_i,
                rawCriteria: { ...cand }
            };
        });

        // Urutkan berdasarkan Skor Vektor V Tertinggi
        rankedList.sort((a, b) => b.score - a.score);
        rankedList.forEach((item, idx) => { item.rank = idx + 1; });

        return {
            name: "Weighted Product (WP)",
            rankedList,
            normWeights,
            powers,
            totalS
        };
    }

    /**
     * 4. KOMPARASI HASIL TIGA METODE (Statistik & Analisis Korelasi)
     */
    calculateComparison(saw, topsis, wp) {
        const n = this.candidates.length;

        // Buat map ranking untuk akses O(1)
        const rankMapSAW = {};
        const rankMapTOPSIS = {};
        const rankMapWP = {};
        const scoreMapSAW = {};
        const scoreMapTOPSIS = {};
        const scoreMapWP = {};

        saw.rankedList.forEach(item => {
            rankMapSAW[item.Kode_Lokasi] = item.rank;
            scoreMapSAW[item.Kode_Lokasi] = item.score;
        });
        topsis.rankedList.forEach(item => {
            rankMapTOPSIS[item.Kode_Lokasi] = item.rank;
            scoreMapTOPSIS[item.Kode_Lokasi] = item.score;
        });
        wp.rankedList.forEach(item => {
            rankMapWP[item.Kode_Lokasi] = item.rank;
            scoreMapWP[item.Kode_Lokasi] = item.score;
        });

        // Hitung Korelasi Spearman Rank (rho = 1 - (6 * sum(d^2)) / (n * (n^2 - 1)))
        const spearman = (mapA, mapB) => {
            let sumD2 = 0;
            this.candidates.forEach(cand => {
                const d = mapA[cand.Kode_Lokasi] - mapB[cand.Kode_Lokasi];
                sumD2 += d * d;
            });
            return 1 - ((6 * sumD2) / (n * (n * n - 1)));
        };

        // Hitung Korelasi Pearson Skor
        const pearson = (mapA, mapB) => {
            const arrA = this.candidates.map(c => mapA[c.Kode_Lokasi]);
            const arrB = this.candidates.map(c => mapB[c.Kode_Lokasi]);
            const meanA = arrA.reduce((a, b) => a + b, 0) / n;
            const meanB = arrB.reduce((a, b) => a + b, 0) / n;

            let num = 0, denA = 0, denB = 0;
            for (let i = 0; i < n; i++) {
                const diffA = arrA[i] - meanA;
                const diffB = arrB[i] - meanB;
                num += diffA * diffB;
                denA += diffA * diffA;
                denB += diffB * diffB;
            }
            return (denA > 0 && denB > 0) ? num / Math.sqrt(denA * denB) : 0;
        };

        const spearmanSAW_TOPSIS = spearman(rankMapSAW, rankMapTOPSIS);
        const spearmanSAW_WP = spearman(rankMapSAW, rankMapWP);
        const spearmanTOPSIS_WP = spearman(rankMapTOPSIS, rankMapWP);

        const pearsonSAW_TOPSIS = pearson(scoreMapSAW, scoreMapTOPSIS);
        const pearsonSAW_WP = pearson(scoreMapSAW, scoreMapWP);
        const pearsonTOPSIS_WP = pearson(scoreMapTOPSIS, scoreMapWP);

        // Analisis Konsensus Top 10
        const top10SAW = saw.rankedList.slice(0, 10).map(x => x.Kode_Lokasi);
        const top10TOPSIS = topsis.rankedList.slice(0, 10).map(x => x.Kode_Lokasi);
        const top10WP = wp.rankedList.slice(0, 10).map(x => x.Kode_Lokasi);

        // Triple Winner (Masuk Top 10 di ketiganya)
        const tripleWinners = top10SAW.filter(code => top10TOPSIS.includes(code) && top10WP.includes(code));

        // Double Winner (Masuk minimal di 2 metode)
        const allTop10 = new Set([...top10SAW, ...top10TOPSIS, ...top10WP]);
        const doubleWinners = Array.from(allTop10).filter(code => {
            const count = (top10SAW.includes(code) ? 1 : 0) + 
                          (top10TOPSIS.includes(code) ? 1 : 0) + 
                          (top10WP.includes(code) ? 1 : 0);
            return count === 2;
        });

        // Top 10 unik per metode
        const uniqueSAW = top10SAW.filter(c => !top10TOPSIS.includes(c) && !top10WP.includes(c));
        const uniqueTOPSIS = top10TOPSIS.filter(c => !top10SAW.includes(c) && !top10WP.includes(c));
        const uniqueWP = top10WP.filter(c => !top10SAW.includes(c) && !top10TOPSIS.includes(c));

        return {
            spearman: {
                saw_topsis: spearmanSAW_TOPSIS,
                saw_wp: spearmanSAW_WP,
                topsis_wp: spearmanTOPSIS_WP
            },
            pearson: {
                saw_topsis: pearsonSAW_TOPSIS,
                saw_wp: pearsonSAW_WP,
                topsis_wp: pearsonTOPSIS_WP
            },
            consensusTop10: {
                tripleWinners,
                doubleWinners,
                uniqueSAW,
                uniqueTOPSIS,
                uniqueWP,
                totalDistinctInTop10: allTop10.size
            }
        };
    }
}
