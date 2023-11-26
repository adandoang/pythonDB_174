# Import modul sqlite3 dan modul tkinter
import sqlite3
from tkinter import *

# Fungsi untuk memprediksi fakultas berdasarkan nilai mata pelajaran tertinggi
def prediksi_fakultas(nilai_mapel):
    mapel_tertinggi = max(nilai_mapel, key=nilai_mapel.get)

    if mapel_tertinggi == 'biologi':
        return "Kedokteran"
    elif mapel_tertinggi in ['fisika', 'geografi']:
        return "Teknik"
    elif mapel_tertinggi in ['b_inggris', 'b_indonesia', 'b_arab']:
        return "Bahasa"
    elif mapel_tertinggi in ['ekonomi', 'ips']:
        return "Management"
    elif mapel_tertinggi == 'pkn':
        return "Hukum"
    elif mapel_tertinggi == 'pai':
        return "Agama"
    else:
        return "Tidak dapat memprediksi"

# Fungsi untuk menyimpan data ke SQLite
def simpan_data(nama_siswa, nilai_mapel):
    # Membuka koneksi ke database SQLite
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            b_inggris INTEGER,
            pai INTEGER,
            ekonomi INTEGER,
            ips INTEGER,
            geografi INTEGER,
            b_indonesia INTEGER,
            pkn INTEGER,
            b_arab INTEGER,
            prediksi_fakultas TEXT
        )
    ''')

    # Menyisipkan data ke dalam tabel
    cursor.execute('''
        INSERT INTO nilai_siswa (
            nama_siswa, 
            biologi, 
            fisika, 
            b_inggris, 
            pai, 
            ekonomi, 
            ips, 
            geografi, 
            b_indonesia, 
            pkn, 
            b_arab, 
            prediksi_fakultas
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        nama_siswa, 
        nilai_mapel['biologi'], 
        nilai_mapel['fisika'], 
        nilai_mapel['b_inggris'], 
        nilai_mapel['pai'], 
        nilai_mapel['ekonomi'], 
        nilai_mapel['ips'], 
        nilai_mapel['geografi'], 
        nilai_mapel['b_indonesia'], 
        nilai_mapel['pkn'], 
        nilai_mapel['b_arab'],
        prediksi_fakultas(nilai_mapel)
    ))

    # Menyimpan perubahan ke dalam database
    conn.commit()

    # Menutup koneksi ke database
    conn.close()

# Fungsi yang dijalankan saat tombol Submit ditekan
def submit_nilai():
    # Mengambil data dari inputan pengguna (nama siswa)
    nama_siswa = entry_nama.get()

    # Membuat dictionary untuk menyimpan nilai mata pelajaran dari slider
    nilai_mapel = {
        'biologi': slider_biologi.get(),
        'fisika': slider_fisika.get(),
        'b_inggris': slider_b_inggris.get(),
        'pai': slider_pai.get(),
        'ekonomi': slider_ekonomi.get(),
        'ips': slider_ips.get(),
        'geografi': slider_geografi.get(),
        'b_indonesia': slider_b_indonesia.get(),
        'pkn': slider_pkn.get(),
        'b_arab': slider_b_arab.get()
    }

    # Menyimpan data ke SQLite dan menampilkan hasil prediksi di label
    simpan_data(nama_siswa, nilai_mapel)
    label_hasil.config(text=f"Hasil prediksi: {prediksi_fakultas(nilai_mapel)}")

# Membuat GUI dengan Tkinter
root = Tk()
root.title("Input Nilai Siswa")

# Label dan Entry untuk Nama Siswa
Label(root, text="Nama Siswa:").grid(row=0, column=0, padx=10, pady=5)
entry_nama = Entry(root)
entry_nama.grid(row=0, column=1, padx=10, pady=5)

# Slider untuk setiap mata pelajaran
mapel_labels = ['Biologi', 'Fisika', 'B. Inggris', 'PAI', 'Ekonomi', 'IPS', 'Geografi', 'B. Indonesia', 'PKN', 'B. Arab']
mapel_keys = ['biologi', 'fisika', 'b_inggris', 'pai', 'ekonomi', 'ips', 'geografi', 'b_indonesia', 'pkn', 'b_arab']

# Loop untuk membuat label dan slider untuk setiap mata pelajaran
for i, mapel_label in enumerate(mapel_labels):
    Label(root, text=f"Nilai {mapel_label}:").grid(row=i+1, column=0, padx=10, pady=5)
    slider = Scale(root, from_=0, to=100, orient=HORIZONTAL)
    slider.grid(row=i+1, column=1, padx=10, pady=5)
    globals()[f'slider_{mapel_keys[i]}'] = slider

# Tombol Submit
Button(root, text="Submit", command=submit_nilai).grid(row=len(mapel_labels)+1, column=0, columnspan=2, pady=10)

# Menambahkan label untuk menampilkan hasil prediksi
label_hasil = Label(root, text="")
label_hasil.grid(row=len(mapel_labels)+2, column=0, columnspan=2, pady=10)

# Memulai loop utama Tkinter
root.mainloop()
