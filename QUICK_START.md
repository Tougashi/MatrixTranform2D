# ⚡ Quick Start - MatrixTransform2D

## 🚀 Menjalankan Aplikasi (3 Langkah)

### 1. Install Package (Jika Belum)
```bash
python install.py
```

### 2. Jalankan Aplikasi
```bash
python run.py
```

### 3. Gunakan Aplikasi
- **Klik** pada objek untuk memilih
- **Gunakan slider** di panel kanan untuk transformasi
- **TAB** untuk beralih antar objek
- **ESC** untuk keluar

## 📁 Struktur Project

```
MatrixTransform2D/
├── run.py                 # ⭐ JALANKAN INI untuk memulai aplikasi
├── src/
│   ├── main.py           # Entry point aplikasi
│   ├── matrix.py         # Transformasi matriks
│   ├── graphics.py       # Rendering objek 2D
│   └── ui.py             # User interface
├── examples/
│   └── demo.py           # Contoh penggunaan API
├── tests/
│   └── test_matrix.py    # Unit tests
├── requirements.txt      # Package dependencies
└── install.py           # Script install package
```

## 🎮 Kontrol Cepat

### Keyboard
- `TAB` - Pilih objek berikutnya
- `R` - Reset transformasi
- `Arrow Keys` - Pindahkan kamera
- `ESC` - Keluar

### Mouse
- `Click` - Pilih objek
- `Drag Slider` - Ubah transformasi

### Panel Kontrol
- **Translate X/Y** - Geser objek
- **Rotate** - Putar objek
- **Scale X/Y** - Skala objek
- **Reset** - Reset semua
- **Center** - Reset translasi

## 🎯 Fitur Utama

✅ **Transformasi Matriks Lengkap**
- Translasi (Translation)
- Rotasi (Rotation)
- Skala (Scaling)
- Kombinasi transformasi

✅ **Multiple Objects**
- 4 objek default (Rectangle, Triangle, Circle, Pentagon)
- Pilih dan transformasi objek satu per satu

✅ **Visual Feedback**
- Grid untuk koordinat
- Axes untuk origin
- Highlight objek terpilih
- Center point ditampilkan

✅ **Real-time Preview**
- Lihat transformasi secara langsung
- Update nilai matriks secara real-time

## 📚 File Penting

| File | Deskripsi |
|------|-----------|
| `run.py` | ⭐ **Jalankan ini untuk memulai aplikasi** |
| `src/main.py` | Main application class |
| `src/matrix.py` | Implementasi transformasi matriks |
| `src/graphics.py` | Class untuk rendering objek 2D |
| `src/ui.py` | User interface components |
| `examples/demo.py` | Contoh penggunaan API |
| `tests/test_matrix.py` | Unit tests |

## 🐛 Troubleshooting

**Error: ModuleNotFoundError**
```bash
python install.py
```

**Aplikasi tidak jalan**
```bash
# Pastikan Python 3.8+
python --version

# Pastikan package terinstall
pip list | grep pygame
pip list | grep numpy
```

## 📖 Dokumentasi Lengkap

- **CARA_MENJALANKAN.md** - Panduan lengkap penggunaan
- **PANDUAN_MULAI.md** - Panduan setup dan development
- **README.md** - Dokumentasi project

## 💡 Contoh Code

### Menggunakan API
```python
from src.matrix import TransformationMatrix
from src.graphics import Rectangle

# Buat objek
rect = Rectangle(0, 0, 100, 50)

# Buat transformasi
matrix = TransformationMatrix()
matrix.translate(50, 50)
matrix.rotate(45)
matrix.scale(1.5, 1.5)

# Terapkan transformasi
rect.apply_transform(matrix)
```

### Menjalankan Demo
```bash
python examples/demo.py
```

### Menjalankan Tests
```bash
pytest tests/test_matrix.py
```

---

**Selamat mencoba! 🎨**

Untuk informasi lebih lengkap, lihat **CARA_MENJALANKAN.md**

