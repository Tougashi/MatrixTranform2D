# 📖 Panduan Memulai - MatrixTransform2D

## 🎯 Langkah-langkah Setup Project

### Langkah 1: Install Package

Jalankan script installasi untuk menginstall semua package yang diperlukan:

```bash
python install.py
```

Script ini akan menginstall:
- **pygame** - Framework untuk 2D graphics
- **numpy** - Library untuk operasi matriks
- **scipy** - Library untuk fungsi matematika
- **Pillow** - Library untuk image processing
- **pytest** - Framework untuk testing

### Langkah 2: Setup Struktur Project (Opsional)

Jika ingin membuat struktur direktori otomatis, jalankan:

```bash
python setup_project.py
```

Atau buat manual dengan struktur berikut:

```
MatrixTransform2D/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── matrix.py
│   ├── graphics.py
│   └── ui.py
├── examples/
├── tests/
└── assets/
```

### Langkah 3: Verifikasi Instalasi

Pastikan semua package terinstall dengan benar:

```bash
python -c "import pygame, numpy, scipy; print('✅ Semua package terinstall!')"
```

## 📚 Package yang Digunakan dan Fungsinya

### 1. **Pygame** (`pygame`)
   - **Fungsi**: Framework utama untuk rendering grafik 2D
   - **Digunakan untuk**: 
     - Window/Display management
     - Event handling (mouse, keyboard)
     - Drawing shapes dan lines
     - Real-time rendering

### 2. **NumPy** (`numpy`)
   - **Fungsi**: Library untuk operasi matriks dan array
   - **Digunakan untuk**:
     - Menghitung matriks transformasi
     - Operasi vektor
     - Matrix multiplication untuk kombinasi transformasi
     - Manipulasi koordinat

### 3. **SciPy** (`scipy`)
   - **Fungsi**: Library untuk fungsi matematika lanjutan
   - **Digunakan untuk**:
     - Fungsi trigonometri yang lebih akurat
     - Operasi matematika kompleks

### 4. **Pillow** (`Pillow`)
   - **Fungsi**: Library untuk image processing
   - **Digunakan untuk**:
     - Loading/saving gambar (opsional)
     - Manipulasi gambar jika diperlukan

## 🚀 Langkah Selanjutnya: Mulai Coding

### Konsep yang Akan Diimplementasikan

#### 1. **Transformasi Matriks 2D**

**Translasi (Translation)**
```
Matriks: [1  0  tx]
         [0  1  ty]
         [0  0  1 ]
```

**Rotasi (Rotation)**
```
Matriks: [cos(θ)  -sin(θ)  0]
         [sin(θ)   cos(θ)  0]
         [  0        0     1]
```

**Skala (Scaling)**
```
Matriks: [sx  0   0]
         [0   sy  0]
         [0   0   1]
```

#### 2. **Alur Kerja Aplikasi**

1. Inisialisasi Pygame window
2. Buat objek 2D (shape/line)
3. Terapkan transformasi matriks
4. Render objek yang sudah ditransformasi
5. Handle user input untuk mengubah transformasi

### Contoh Struktur Code Minimal

**src/main.py**
```python
import pygame
import numpy as np
from matrix import TransformationMatrix

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("MatrixTransform2D")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        # Rendering code di sini
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

**src/matrix.py**
```python
import numpy as np

class TransformationMatrix:
    def __init__(self):
        self.matrix = np.eye(3)  # Identity matrix
    
    def translate(self, tx, ty):
        # Implementasi translasi
        pass
    
    def rotate(self, angle):
        # Implementasi rotasi
        pass
    
    def scale(self, sx, sy):
        # Implementasi skala
        pass
```

## 💡 Tips Pengembangan

1. **Mulai dari yang sederhana**: Buat window Pygame dulu, lalu tambahkan objek statis
2. **Test matriks terlebih dahulu**: Buat test case untuk memastikan transformasi matriks benar
3. **Gunakan NumPy**: Manfaatkan numpy untuk operasi matriks yang lebih efisien
4. **Incremental development**: Buat fitur satu per satu (translasi → rotasi → skala)

## 🔍 Troubleshooting

**Error: ModuleNotFoundError**
- Pastikan sudah menjalankan `python install.py`
- Cek apakah virtual environment aktif (jika menggunakan)

**Error: pygame tidak terdeteksi**
- Coba install ulang: `pip install pygame --upgrade`
- Pastikan Python version 3.8+

**Import Error**
- Pastikan struktur folder sudah benar
- Cek apakah `__init__.py` ada di setiap folder

## 📖 Resources Belajar

- [Pygame Tutorial](https://www.pygame.org/docs/tut/PygameIntro.html)
- [NumPy Matrix Operations](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [2D Transformation Matrices](https://www.tutorialspoint.com/computer_graphics/2d_transformation.htm)

## ✅ Checklist Persiapan

- [ ] Package sudah diinstall (`python install.py`)
- [ ] Struktur project sudah dibuat
- [ ] Python version 3.8+ terinstall
- [ ] IDE/Editor siap digunakan
- [ ] Siap untuk mulai coding! 🚀

Selamat coding! 🎉

