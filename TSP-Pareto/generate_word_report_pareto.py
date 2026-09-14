import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_report():
    doc = Document()

    # 1. Mengatur Format Kertas dan Margin
    # Kertas A4: 21 cm x 29.7 cm
    # Margin: Kiri 4 cm, Atas 3 cm, Kanan 3 cm, Bawah 3 cm
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(4)
        section.right_margin = Cm(3)
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(3)

    # 2. Mengatur Format Huruf Default (Times New Roman, 12pt, Spasi 1.5)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = 1.5

    # 3. Membuat Judul Bab
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run('BAB IV\nHASIL YANG DICAPAI DAN RENCANA TAHAPAN BERIKUTNYA')
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(12)
    
    doc.add_paragraph()

    # ==========================================
    # Sub-bab 4.1 Hasil yang Dicapai
    # ==========================================
    p_sub1 = doc.add_paragraph()
    r_sub1 = p_sub1.add_run('4.1 Hasil yang Dicapai')
    r_sub1.bold = True
    r_sub1.font.name = 'Times New Roman'

    p_intro = doc.add_paragraph('Berdasarkan tahapan penelitian yang telah dilaksanakan, evaluasi pemilihan lokasi kafe di Kabupaten Tuban dilakukan melalui tiga pendekatan algoritmik terintegrasi. Tahap pertama adalah screening kandidat menggunakan prinsip Pareto Optimality, tahap kedua adalah penentuan rute survei lapangan dengan Traveling Salesperson Problem (TSP), dan tahap terakhir adalah perankingan menggunakan metode Simple Additive Weighting (SAW) serta Analytical Hierarchy Process - Technique for Others Preference by Similarity to Ideal Solution (AHP-TOPSIS).')
    p_intro.paragraph_format.first_line_indent = Cm(1.27)

    # Penjelasan Temuan Pareto dan TSP
    p_pareto = doc.add_paragraph('Proses penyaringan awal dengan algoritma Pareto berhasil mereduksi kompleksitas evaluasi dengan membuang kandidat-kandidat yang terdominasi secara absolut. Dari 100 titik lokasi awal yang diekstrak menggunakan OpenStreetMap, tersaring sebanyak 82 lokasi kandidat Pareto Optimal. Selanjutnya, hasil simulasi jalur terpendek (TSP) untuk ground truth di lapangan yang menghubungkan ke-82 lokasi optimal tersebut menghasilkan rute perjalanan tertutup dengan estimasi total jarak tempuh sejauh 195,44 km.')
    p_pareto.paragraph_format.first_line_indent = Cm(1.27)

    p_lanjut = doc.add_paragraph('Berdasarkan 82 kandidat Pareto tersebut, dilakukan komputasi preferensi akhir (SPK). Berikut ini disajikan komparasi visual dan tabel peringkat dari kandidat lokasi terbaik antara penggunaan metode SAW dan AHP-TOPSIS.')
    p_lanjut.paragraph_format.first_line_indent = Cm(1.27)

    # Sisipkan Gambar 1
    if os.path.exists('Visualisasi_1_Perbandingan_Metode_Pareto.png'):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture('Visualisasi_1_Perbandingan_Metode_Pareto.png', width=Cm(13.5))
        p_cap1 = doc.add_paragraph('Gambar 4.1 Perbandingan 10 Kandidat Terbaik antara Metode SAW dan AHP-TOPSIS (Pasca-Pareto)')
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.runs[0].font.size = Pt(11)

    # Sisipkan Gambar 2
    if os.path.exists('Visualisasi_2_Analisis_Kriteria_Pareto.png'):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture('Visualisasi_2_Analisis_Kriteria_Pareto.png', width=Cm(13.5))
        p_cap2 = doc.add_paragraph('Gambar 4.2 Analisis Kriteria Aksesibilitas (C1) dan Kedekatan POI (C7) pada Top 5 Kandidat Pareto')
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.runs[0].font.size = Pt(11)

    # Sisipkan Gambar Slopegraph
    if os.path.exists('Visualisasi_4_Perubahan_Peringkat_Pareto.png'):
        doc.add_page_break()
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.add_run().add_picture('Visualisasi_4_Perubahan_Peringkat_Pareto.png', height=Cm(12))
        p_cap4 = doc.add_paragraph('Gambar 4.3 Perubahan Peringkat Kandidat Pareto (Metode SAW vs AHP-TOPSIS)')
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.runs[0].font.size = Pt(11)

    p_desc2 = doc.add_paragraph('Untuk mengonfirmasi dinamika peringkat secara kuantitatif, Tabel 4.1 menyajikan komparasi peringkat untuk top 15 kandidat.')
    p_desc2.paragraph_format.first_line_indent = Cm(1.27)

    # Sisipkan Tabel Top 15
    if os.path.exists('Tabel_Top15_Perbandingan_Pareto.csv'):
        p_tab_title = doc.add_paragraph('Tabel 4.1 Perbandingan Peringkat Top 15 Kandidat (SAW vs AHP-TOPSIS)')
        p_tab_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_tab_title.runs[0].font.size = Pt(11)

        df = pd.read_csv('Tabel_Top15_Perbandingan_Pareto.csv')
        table = doc.add_table(rows=1, cols=len(df.columns))
        table.style = 'Table Grid'
        
        # Header
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(df.columns):
            hdr_cells[i].text = str(column).replace('_', ' ')
            p_hdr = hdr_cells[i].paragraphs[0]
            p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_hdr.runs[0].font.bold = True
            p_hdr.runs[0].font.name = 'Times New Roman'
            p_hdr.runs[0].font.size = Pt(10)

        # Body
        for index, row in df.iterrows():
            row_cells = table.add_row().cells
            for i, val in enumerate(row):
                if isinstance(val, float):
                    row_cells[i].text = f"{val:.3f}"
                else:
                    row_cells[i].text = str(val)
                p_cell = row_cells[i].paragraphs[0]
                p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cell.runs[0].font.name = 'Times New Roman'
                p_cell.runs[0].font.size = Pt(10)
    
    doc.add_paragraph()

    # ==========================================
    # Sub-bab 4.2 Rencana Tahapan Berikutnya
    # ==========================================
    p_sub2 = doc.add_paragraph()
    r_sub2 = p_sub2.add_run('4.2 Rencana Tahapan Berikutnya')
    r_sub2.bold = True
    r_sub2.font.name = 'Times New Roman'
    r_sub2.font.size = Pt(12)

    doc.add_paragraph('Berdasarkan hasil evaluasi model yang mengintegrasikan algoritma Pareto Optimality, perhitungan TSP, dan perankingan SPK, tahapan selanjutnya yang direncanakan adalah sebagai berikut:')
    
    plans = [
        "Melakukan validasi lapangan (ground truth) secara komprehensif mengikuti rute panduan TSP sejauh 195,44 km yang telah dihasilkan. Validasi akan diprioritaskan pada kandidat-kandidat juara (seperti Kandidat 42) untuk memverifikasi akurasi data sekunder spasial dari OpenStreetMap.",
        "Mengembangkan prototipe antarmuka sistem pendukung keputusan berbasis WebGIS yang interaktif, sehingga memungkinkan pengguna atau investor meninjau langsung rute perjalanan TSP serta profil rinci 82 lokasi Pareto tersebut di peta nyata.",
        "Melakukan pengujian usabilitas (usability testing) terhadap antarmuka fungsional WebGIS kepada pemangku kepentingan (stakeholders) guna mengukur efektivitas dan tingkat penerimaan user.",
        "Menyusun dan menyerahkan (submit) naskah publikasi jurnal akhir yang mendemonstrasikan keunggulan teknis inovasi perpaduan antara penyaringan Pareto, TSP, dan metode komparasi SAW/AHP-TOPSIS dalam pengambilan keputusan penempatan lokasi bisnis."
    ]

    for plan in plans:
        p_plan = doc.add_paragraph(plan, style='List Number')
        p_plan.paragraph_format.line_spacing = 1.5
        for run in p_plan.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

    doc.save('Bab_IV_Hasil_dan_Rencana_Pareto_TSP.docx')
    print("Dokumen Word berhasil dibuat: Bab_IV_Hasil_dan_Rencana_Pareto_TSP.docx")

if __name__ == "__main__":
    create_report()
