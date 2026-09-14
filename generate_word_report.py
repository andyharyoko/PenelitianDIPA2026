import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

def create_report():
    # Inisialisasi Dokumen
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
    
    doc.add_paragraph() # Spasi kosong

    # ==========================================
    # Sub-bab 4.1 Hasil yang Dicapai
    # ==========================================
    p_sub1 = doc.add_paragraph()
    r_sub1 = p_sub1.add_run('4.1 Hasil yang Dicapai')
    r_sub1.bold = True
    r_sub1.font.name = 'Times New Roman'
    r_sub1.font.size = Pt(12)

    p_intro = doc.add_paragraph('Berdasarkan tahapan penelitian yang telah dilaksanakan, sistem pendukung keputusan penentuan lokasi strategis kafe di Kabupaten Tuban menggunakan integrasi metode Simple Additive Weighting (SAW) dan Analytical Hierarchy Process - Technique for Others Preference by Similarity to Ideal Solution (AHP-TOPSIS) telah berhasil dikembangkan dan diuji. Hasil akhir dari proses analisis spasial dan komputasi pembobotan dievaluasi untuk memberikan rekomendasi terbaik. Berikut ini adalah visualisasi serta tabel komparasi dari kandidat-kandidat lokasi terbaik yang telah dihasilkan.')
    p_intro.paragraph_format.first_line_indent = Cm(1.27)

    # Sisipkan Gambar 1
    if os.path.exists('Visualisasi_1_Perbandingan_Metode.png'):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture('Visualisasi_1_Perbandingan_Metode.png', width=Cm(13.5))
        
        p_cap1 = doc.add_paragraph('Gambar 4.1 Perbandingan 10 Kandidat Terbaik antara Metode SAW dan AHP-TOPSIS')
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.runs[0].font.size = Pt(11)

    p_desc1 = doc.add_paragraph('Gambar 4.1 mengilustrasikan perbedaan hasil perankingan dari 10 kandidat teratas. Terdapat konsistensi pada beberapa kandidat utama yang menempati posisi puncak, namun perbedaan mekanisme pembobotan pada kedua metode memberikan variasi posisi pada kandidat-kandidat di peringkat selanjutnya.')
    p_desc1.paragraph_format.first_line_indent = Cm(1.27)

    # Sisipkan Gambar 2
    if os.path.exists('Visualisasi_2_Analisis_Kriteria.png'):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture('Visualisasi_2_Analisis_Kriteria.png', width=Cm(13.5))
        
        p_cap2 = doc.add_paragraph('Gambar 4.2 Analisis Kriteria Aksesibilitas (C1) dan Kedekatan POI (C7) pada Top 5 Kandidat')
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.runs[0].font.size = Pt(11)

    # Sisipkan Gambar Slopegraph (Visualisasi 4)
    if os.path.exists('Visualisasi_4_Perubahan_Peringkat.png'):
        doc.add_page_break()
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.add_run().add_picture('Visualisasi_4_Perubahan_Peringkat.png', height=Cm(12))
        
        p_cap4 = doc.add_paragraph('Gambar 4.3 Perubahan Peringkat Kandidat (Metode SAW vs AHP-TOPSIS)')
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.runs[0].font.size = Pt(11)

    p_desc2 = doc.add_paragraph('Untuk memberikan gambaran komparatif yang lebih detail mengenai fluktuasi peringkat antar kedua metode, Tabel 4.1 menyajikan perbandingan data secara langsung untuk 15 kandidat terbaik hasil komputasi SPK.')
    p_desc2.paragraph_format.first_line_indent = Cm(1.27)

    # Sisipkan Tabel
    if os.path.exists('Tabel_Top15_Perbandingan.csv'):
        p_tab_title = doc.add_paragraph('Tabel 4.1 Perbandingan Peringkat Top 15 Kandidat (SAW vs AHP-TOPSIS)')
        p_tab_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_tab_title.runs[0].font.size = Pt(11)

        df = pd.read_csv('Tabel_Top15_Perbandingan.csv')
        # Buat tabel
        table = doc.add_table(rows=1, cols=len(df.columns))
        table.style = 'Table Grid'
        
        # Header Tabel
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(df.columns):
            hdr_cells[i].text = str(column).replace('_', ' ')
            p_hdr = hdr_cells[i].paragraphs[0]
            p_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_hdr.runs[0].font.bold = True
            p_hdr.runs[0].font.name = 'Times New Roman'
            p_hdr.runs[0].font.size = Pt(10)

        # Data Tabel
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
    
    doc.add_paragraph() # Spasi

    # ==========================================
    # Sub-bab 4.2 Rencana Tahapan Berikutnya
    # ==========================================
    p_sub2 = doc.add_paragraph()
    r_sub2 = p_sub2.add_run('4.2 Rencana Tahapan Berikutnya')
    r_sub2.bold = True
    r_sub2.font.name = 'Times New Roman'
    r_sub2.font.size = Pt(12)

    doc.add_paragraph('Berdasarkan hasil yang telah dicapai, serangkaian tahapan selanjutnya yang direncanakan dalam penelitian ini adalah sebagai berikut:')
    
    plans = [
        "Melakukan validasi lapangan (ground truth) secara komprehensif terhadap lokasi-lokasi yang direkomendasikan tertinggi (seperti Kandidat 42 dan Kandidat 77) untuk mengonfirmasi akurasi data sekunder spasial yang diperoleh dari OpenStreetMap.",
        "Mengembangkan prototipe antarmuka sistem pendukung keputusan berbasis WebGIS yang interaktif, sehingga memungkinkan pengguna untuk menyesuaikan bobot kriteria sesuai preferensi mereka secara dinamis.",
        "Melakukan pengujian usabilitas (usability testing) dan evaluasi kepuasan pengguna (user acceptance test) terhadap WebGIS kepada pemangku kepentingan terkait untuk mengukur tingkat efektivitas antarmuka sistem.",
        "Menyusun dan melakukan finalisasi naskah publikasi jurnal berdasarkan temuan analisis perbandingan metode dan hasil pengujian lapangan untuk kemudian di-submit pada jurnal bereputasi tinggi."
    ]

    for plan in plans:
        p_plan = doc.add_paragraph(plan, style='List Number')
        p_plan.paragraph_format.line_spacing = 1.5
        for run in p_plan.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

    # Simpan file
    doc.save('Bab_IV_Hasil_dan_Rencana.docx')
    print("Dokumen Word berhasil dibuat: Bab_IV_Hasil_dan_Rencana.docx")

if __name__ == "__main__":
    create_report()
