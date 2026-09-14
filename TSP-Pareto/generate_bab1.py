import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_bab1():
    doc = Document()

    # Pengaturan Format Kertas A4 & Margin (Kiri 4cm, Atas/Kanan/Bawah 3cm)
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.left_margin = Cm(4)
        section.right_margin = Cm(3)
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(3)

    # Pengaturan Format Huruf & Spasi (Times New Roman 12, Spasi 1.5)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    style.paragraph_format.line_spacing = 1.5

    # Judul Bab
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run('BAB I\nPENDAHULUAN')
    r_title.bold = True
    
    doc.add_paragraph()

    # 1.1 Latar Belakang Masalah
    doc.add_paragraph('1.1 Latar Belakang Masalah', style='Normal').runs[0].bold = True
    p1 = doc.add_paragraph('Pertumbuhan pesat sektor industri kreatif dan Food & Beverage (F&B), khususnya bisnis restoran dan kafe, memberikan kontribusi signifikan terhadap perekonomian lokal. Namun, penentuan lokasi bisnis (site selection) yang tidak strategis masih menjadi faktor penyebab utama kegagalan finansial akibat tingginya biaya investasi awal (sunk cost) dan rendahnya rasio pengembalian modal (Alwedyan, 2024). Selama ini, sebagian besar pelaku usaha masih mengandalkan intuisi subjektif atau survei lapangan manual yang sangat memakan waktu, mahal secara logistik, dan rentan terhadap bias persepsi.')
    p1.paragraph_format.first_line_indent = Cm(1.27)

    p2 = doc.add_paragraph('Di era transformasi digital, tingginya kompetisi tata letak restoran memicu fenomena "foodification" ruang perkotaan, di mana ketersediaan data spasial terbuka berskala masif menawarkan peluang besar untuk melakukan pemetaan prospek lokasi secara kuantitatif (Hidalgo-Giralt, 2024). Penggunaan kerangka Sistem Informasi Geografis (SIG) yang diintegrasikan dengan algoritma pembobotan konvensional terhadap ratusan kandidat data spasial mentah sering kali memicu inefisiensi komputasi dan rentan menghasilkan anomali pemeringkatan (rank reversal). Selain itu, sistem penunjang keputusan yang hanya berhenti pada rekomendasi layar dinilai kurang komprehensif tanpa pemodelan rute logistik untuk survei fisik (ground truth) di lapangan (Kim et al., 2025).')
    p2.paragraph_format.first_line_indent = Cm(1.27)
    
    p3 = doc.add_paragraph('Menyikapi permasalahan tersebut, penelitian ini mengusulkan sebuah pendekatan algoritmik terintegrasi. Tahapan awal menggunakan prinsip Pareto Optimality digunakan untuk mengeliminasi kandidat lokasi terdominasi. Selanjutnya, kandidat optimal dievaluasi komparasinya menggunakan metode Simple Additive Weighting (SAW) dan Analytical Hierarchy Process - Technique for Others Preference by Similarity to Ideal Solution (AHP-TOPSIS). Untuk menyempurnakan aspek kepraktisan, penelitian ini juga mengadopsi pemodelan Traveling Salesperson Problem (TSP) guna mendesain panduan rute validasi lapangan secara efisien.')
    p3.paragraph_format.first_line_indent = Cm(1.27)

    doc.add_paragraph()

    # 1.2 Rumusan Masalah
    doc.add_paragraph('1.2 Rumusan Masalah dan Tujuan Khusus Penelitian', style='Normal').runs[0].bold = True
    p4 = doc.add_paragraph('Berdasarkan latar belakang yang telah diuraikan, maka rumusan masalah dalam penelitian ini adalah sebagai berikut:')
    p4.paragraph_format.first_line_indent = Cm(1.27)
    
    rumusan = [
        "Bagaimana efektivitas algoritma Pareto Optimality dalam melakukan filtering untuk membuang kandidat lokasi spasial yang terdominasi sebelum proses pembobotan dilakukan?",
        "Bagaimana perbandingan tingkat konsistensi dan stabilitas peringkat (ranking) yang dihasilkan oleh metode SAW dan AHP-TOPSIS pada sekumpulan alternatif lokasi Pareto Optimal?",
        "Bagaimana pemodelan algoritma Traveling Salesperson Problem (TSP) dapat diintegrasikan untuk merancang rute terpendek dalam kegiatan verifikasi data lapangan (ground truth)?"
    ]
    for r in rumusan:
        doc.add_paragraph(r, style='List Number')

    doc.add_paragraph()
    p5 = doc.add_paragraph('Sejalan dengan rumusan masalah tersebut, tujuan khusus dari penelitian ini meliputi:')
    p5.paragraph_format.first_line_indent = Cm(1.27)
    
    tujuan = [
        "Mengimplementasikan dan mengukur reduksi dimensi komputasi menggunakan penyaringan Pareto Optimality pada data spasial mentah.",
        "Menganalisis fluktuasi dan karakteristik pengambilan keputusan spasial secara komparatif antara metode kompensatori (SAW) dan jarak ideal (AHP-TOPSIS).",
        "Menghasilkan rute perjalanan lapangan (closed-loop routing) yang teroptimasi secara logistik menggunakan kalkulasi TSP guna mendukung validasi operasional yang efisien."
    ]
    for t in tujuan:
        doc.add_paragraph(t, style='List Number')

    doc.add_paragraph()

    # 1.3 Urgensi (Keutamaan) Penelitian
    doc.add_paragraph('1.3 Urgensi (Keutamaan) Penelitian', style='Normal').runs[0].bold = True
    p6 = doc.add_paragraph('Penelitian ini memiliki urgensi yang sangat krusial baik dari sisi akademis maupun sosio-ekonomi. Secara teoretis/akademis, penelitian ini mengisi kesenjangan metodologi pada riset tata ruang bisnis dengan membuktikan bahwa prapemrosesan filter Pareto mampu mengeliminasi noise data secara absolut. Integrasi inovatif ini membawa kebaruan (novelty) yang secara pragmatis menjembatani kesenjangan antara simulasi komputasi digital (MCDM) dengan efisiensi eksekusi logistik di dunia nyata (TSP).')
    p6.paragraph_format.first_line_indent = Cm(1.27)

    p7 = doc.add_paragraph('Secara sosio-ekonomi, hasil penelitian ini akan memberikan landasan investasi yang berbasis data (data-driven) bagi pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) serta investor. Dengan menggantikan tebakan subjektif dengan perhitungan matematis yang komprehensif, penelitian ini secara langsung berperan dalam menekan risiko kerugian modal (capital loss) pada sektor industri komersial skala kecil hingga menengah.')
    p7.paragraph_format.first_line_indent = Cm(1.27)

    # Tambahan Daftar Pustaka untuk Bab 1
    doc.add_page_break()
    p_ref_title = doc.add_paragraph()
    p_ref_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ref_title = p_ref_title.add_run('DAFTAR PUSTAKA BAB I')
    r_ref_title.bold = True
    
    doc.add_paragraph('Alwedyan, M. (2024). Optimal location selection of a casual-dining restaurant using a multi-criteria decision-making (MCDM) approach. International Review for Spatial Planning and Sustainable Development, 12(1), 156. https://doi.org/10.14246/irspsd.12.1_156')
    doc.add_paragraph('Hidalgo-Giralt, C. (2024). Foodification in Madrid: spatial location strategies of restaurant groups. Boletín de la Asociación de Geógrafos Españoles. https://doi.org/10.21138/bage.3748')
    doc.add_paragraph('Kim, W., Kim, H., & Chun, Y. (2025). A spatially informed solving approach for the Traveling Salesman Problem. The Professional Geographer, 77(6), 690-703. https://doi.org/10.1080/00330124.2025.2565474')

    doc.save('Bab_I_Pendahuluan.docx')
    print("Dokumen Bab I berhasil dibuat dengan sitasi APA 7.")

if __name__ == "__main__":
    create_bab1()
