# 🚀 Cara Menjalankan Aplikasi MatrixTransform2D

## 📋 Prasyarat

Pastikan sudah menginstall:
- Python 3.8 atau lebih baru
- Semua package dari `requirements.txt` sudah terinstall

## 🏃 Menjalankan Aplikasi

### Cara 1: Menggunakan run.py (Paling Mudah)

```bash
python run.py
```

### Cara 2: Langsung dari module

```bash
python -m src.main
```

### Cara 3: Menggunakan Python Interactive

```python
from src.main import main
main()
```

## 🎮 Cara Menggunakan Aplikasi

### Kontrol Keyboard

- **TAB** - Beralih antar objek (shape)
- **R** - Reset transformasi objek yang dipilih
- **Arrow Keys** - Pindahkan kamera (scrolling)
  - ⬅️ LEFT - Geser ke kiri
  - ➡️ RIGHT - Geser ke kanan
  - ⬆️ UP - Geser ke atas
  - ⬇️ DOWN - Geser ke bawah
- **ESC** - Keluar dari aplikasi

### Kontrol Mouse

- **Left Click** pada objek - Pilih objek
- **Left Click** pada slider - Atur nilai transformasi
- **Drag** pada slider - Mengubah nilai transformasi secara real-time

### Panel Kontrol (Kanan)

Aplikasi memiliki panel kontrol di sebelah kanan dengan slider untuk:

1. **Translate X** - Geser objek horizontal (-200 sampai 200)
2. **Translate Y** - Geser objek vertikal (-200 sampai 200)
3. **Rotate (deg)** - Putar objek (-180° sampai 180°)
4. **Scale X** - Skala horizontal (0.1 sampai 3.0)
5. **Scale Y** - Skala vertikal (0.1 sampai 3.0)

**Tombol:**
- **Reset** - Reset semua transformasi ke default
- **Center** - Reset translasi ke center (translasi X dan Y = 0)

### Objek Default

Aplikasi dimulai dengan 4 objek default:
1. **Rectangle** (Biru) - Di center
2. **Triangle** (Orange) - Di bawah rectangle
3. **Circle** (Hijau muda) - Di atas center
4. **Pentagon** (Merah muda) - Di atas circle

## 📊 Transformasi Matriks

Aplikasi menggunakan matriks transformasi 3x3 untuk operasi 2D:

### Matriks Translasi
```
[1  0  tx]
[0  1  ty]
[0  0  1 ]
```

### Matriks Rotasi
```
[cos(θ)  -sin(θ)  0]
[sin(θ)   cos(θ)  0]
[  0        0     1]
```

### Matriks Skala
```
[sx  0   0]
[0   sy  0]
[0   0   1]
```

## 🎯 Fitur

- ✅ Transformasi Real-time - Lihat perubahan secara langsung
- ✅ Multiple Objects - Bekerja dengan banyak objek
- ✅ Visual Feedback - Objek terpilih ditandai dengan border merah
- ✅ Grid & Axes - Panduan visual untuk koordinat
- ✅ Matrix Display - Lihat nilai matriks transformasi
- ✅ Center Point - Lihat center point setiap objek

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

Pastikan sudah install semua package:
```bash
python install.py
```

atau:
```bash
pip install -r requirements.txt
```

### Error: pygame tidak terdeteksi

Coba install ulang pygame:
```bash
pip install pygame --upgrade
```

### Window tidak muncul

Pastikan:
- Tidak ada error di console
- Python version 3.8+
- Semua package terinstall dengan benar

### Slider tidak responsif

Pastikan:
- Mouse cursor ada di area slider
- Click dan drag pada knob slider
- Window aplikasi dalam fokus

## 💡 Tips

1. **Pilih objek terlebih dahulu** sebelum menggunakan slider
2. **Gunakan TAB** untuk beralih antar objek dengan cepat
3. **Reset** jika transformasi menjadi terlalu kompleks
4. **Gunakan Arrow Keys** untuk melihat objek yang berada di luar viewport
5. **Perhatikan center point** (titik merah) untuk memahami pivot transformasi

## 📝 Catatan

- Transformasi diterapkan dalam urutan: **Scale → Rotate → Translate**
- Center point objek ditampilkan sebagai titik merah kecil
- Objek yang dipilih ditandai dengan border merah
- Grid membantu visualisasi koordinat dan jarak

---

**Selamat mencoba aplikasi MatrixTransform2D! 🎨**

