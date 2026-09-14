/**
 * AHP (Analytical Hierarchy Process) Engine
 * Perhitungan Matriks Perbandingan Berpasangan, Eigenvector, Lambda Max, CI, dan CR
 */

class AHPEngine {
    constructor(criteria = CRITERIA_DEFINITIONS, initialMatrix = DEFAULT_AHP_MATRIX) {
        this.criteria = criteria;
        this.n = criteria.length;
        this.riValue = SAATY_RI[this.n] || 1.32;
        // Salin matriks awal secara mendalam
        this.matrix = initialMatrix.map(row => [...row]);
        this.results = null;
        this.calculate();
    }

    /**
     * Format nilai Saaty ke bentuk pecahan umum untuk tampilan tabel (misal 1/3, 1/2)
     */
    static formatSaatyValue(val) {
        const tol = 0.02;
        if (Math.abs(val - 1) < tol) return "1";
        if (Math.abs(val - 2) < tol) return "2";
        if (Math.abs(val - 3) < tol) return "3";
        if (Math.abs(val - 4) < tol) return "4";
        if (Math.abs(val - 5) < tol) return "5";
        if (Math.abs(val - 6) < tol) return "6";
        if (Math.abs(val - 7) < tol) return "7";
        if (Math.abs(val - 8) < tol) return "8";
        if (Math.abs(val - 9) < tol) return "9";
        if (Math.abs(val - 0.5) < tol) return "1/2";
        if (Math.abs(val - 1/3) < tol) return "1/3";
        if (Math.abs(val - 1/4) < tol) return "1/4";
        if (Math.abs(val - 1/5) < tol) return "1/5";
        if (Math.abs(val - 1/6) < tol) return "1/6";
        if (Math.abs(val - 1/7) < tol) return "1/7";
        if (Math.abs(val - 1/8) < tol) return "1/8";
        if (Math.abs(val - 1/9) < tol) return "1/9";
        return val.toFixed(3);
    }

    /**
     * Update nilai perbandingan sel (row i, col j).
     * Otomatis mengupdate sel kebalikannya (row j, col i = 1 / val).
     */
    updateCell(row, col, value) {
        if (row === col) {
            this.matrix[row][col] = 1.0;
            return;
        }
        const val = parseFloat(value);
        if (isNaN(val) || val <= 0) return;

        this.matrix[row][col] = val;
        this.matrix[col][row] = 1.0 / val;
        this.calculate();
    }

    /**
     * Melakukan seluruh rangkaian komputasi AHP
     */
    calculate() {
        const n = this.n;

        // 1. Hitung jumlah tiap kolom
        const colSums = new Array(n).fill(0);
        for (let j = 0; j < n; j++) {
            for (let i = 0; i < n; i++) {
                colSums[j] += this.matrix[i][j];
            }
        }

        // 2. Normalisasi matriks perbandingan kolom (N_ij = A_ij / colSum_j)
        const normMatrix = [];
        for (let i = 0; i < n; i++) {
            const row = [];
            for (let j = 0; j < n; j++) {
                row.push(this.matrix[i][j] / colSums[j]);
            }
            normMatrix.push(row);
        }

        // 3. Hitung Prioritas Bobot (Eigenvector w_i = rata-rata baris normMatrix)
        const weights = new Array(n).fill(0);
        for (let i = 0; i < n; i++) {
            const sumRow = normMatrix[i].reduce((acc, val) => acc + val, 0);
            weights[i] = sumRow / n;
        }

        // 4. Perkalian Matriks A * w (Weighted Sum Vector)
        const Aw = new Array(n).fill(0);
        for (let i = 0; i < n; i++) {
            for (let j = 0; j < n; j++) {
                Aw[i] += this.matrix[i][j] * weights[j];
            }
        }

        // 5. Hitung Vektor Rasio Konsistensi per Baris: Aw_i / w_i
        const consistencyVector = [];
        for (let i = 0; i < n; i++) {
            consistencyVector.push(Aw[i] / weights[i]);
        }

        // 6. Hitung Lambda Max (rata-rata dari consistency vector)
        const lambdaMax = consistencyVector.reduce((acc, v) => acc + v, 0) / n;

        // 7. Consistency Index (CI) = (lambda_max - n) / (n - 1)
        const ci = (lambdaMax - n) / (n - 1);

        // 8. Consistency Ratio (CR) = CI / RI
        const cr = ci / this.riValue;

        // 9. Status Konsistensi (Threshold Saaty: CR <= 0.10 atau 10%)
        const isConsistent = cr <= 0.10;

        this.results = {
            n,
            matrix: this.matrix,
            colSums,
            normMatrix,
            weights,
            Aw,
            consistencyVector,
            lambdaMax,
            ci,
            ri: this.riValue,
            cr,
            isConsistent,
            criteriaWeights: this.criteria.map((c, idx) => ({
                code: c.code,
                name: c.name,
                label: c.label,
                type: c.type,
                weight: weights[idx],
                weightPercentage: weights[idx] * 100
            }))
        };

        return this.results;
    }

    getResults() {
        return this.results;
    }

    getWeights() {
        return this.results.weights;
    }

    resetToDefault() {
        this.matrix = DEFAULT_AHP_MATRIX.map(row => [...row]);
        return this.calculate();
    }
}
