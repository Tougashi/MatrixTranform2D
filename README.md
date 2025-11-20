# MatrixTransform2D

Aplikasi Desain Grafis 2D Sederhana dengan Implementasi Transformasi Matriks (Translasi, Rotasi, Skala) untuk Manipulasi Objek.

## 📋 Deskripsi

MatrixTransform2D adalah aplikasi desktop sederhana yang memungkinkan pengguna untuk:
- Membuat dan memanipulasi objek 2D (garis, bentuk geometri)
- Melakukan transformasi matriks: Translasi, Rotasi, dan Skala
- Visualisasi langsung dari transformasi yang diterapkan
- Melihat representasi matriks transformasi

## 🛠️ Teknologi yang Digunakan

- **Python 3.8+**: Bahasa pemrograman utama
- **Pygame**: Framework untuk rendering grafik 2D dan interaksi pengguna
- **NumPy**: Library untuk operasi matriks dan komputasi numerik
- **SciPy**: Library tambahan untuk fungsi matematika
- **Pillow**: Library untuk manipulasi gambar (opsional)

## 📦 Instalasi

### Langkah 1: Install Package

Jalankan file `install.py` untuk menginstall semua package yang diperlukan:

```bash
python install.py
```

Atau install manual menggunakan pip:

```bash
pip install -r requirements.txt
```

### Langkah 2: Verifikasi Instalasi

Pastikan semua package terinstall dengan benar:

```bash
python -c "import pygame, numpy, scipy, PIL; print('Semua package terinstall!')"
```

## 📁 Struktur Project (Direkomendasikan)

```
MatrixTransform2D/
├── requirements.txt          # Daftar package yang diperlukan
├── install.py               # Script untuk install package
├── README.md                # Dokumentasi project
├── src/                     # Source code utama
│   ├── __init__.py
│   ├── main.py             # Entry point aplikasi
│   ├── matrix.py           # Implementasi transformasi matriks
│   ├── graphics.py         # Class untuk rendering objek
│   └── ui.py               # User interface
├── examples/                # Contoh penggunaan
└── tests/                   # Unit tests
```

## 🚀 Memulai Pengembangan

### Konsep Dasar yang Akan Diimplementasikan:

1. **Transformasi Matriks**
   - Matriks Translasi (Translation Matrix)
   - Matriks Rotasi (Rotation Matrix)
   - Matriks Skala (Scaling Matrix)
   - Kombinasi transformasi (Matrix Multiplication)

2. **Graphics Pipeline**
   - Sistem koordinat 2D
   - Rendering objek (points, lines, shapes)
   - Transformasi objek secara real-time

3. **User Interface**
   - Canvas untuk menggambar
   - Kontrol untuk translasi, rotasi, skala
   - Visualisasi matriks transformasi

## 📚 Referensi

- [Pygame Documentation](https://www.pygame.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matrix Transformations in 2D](https://en.wikipedia.org/wiki/Transformation_matrix)

## 👨‍💻 Pengembangan

Proyek ini akan dikembangkan secara bertahap. File instalasi ini adalah langkah awal untuk setup environment pengembangan.

## 📝 Lisensi

Tersedia untuk penggunaan pribadi dan pembelajaran.

