"""
Script untuk membuat struktur direktori project MatrixTransform2D
Jalankan file ini dengan: python setup_project.py
"""

import os

def create_directory_structure():
    """Membuat struktur direktori untuk project"""
    print("=" * 60)
    print("MatrixTransform2D - Project Setup")
    print("=" * 60)
    print()
    
    directories = [
        'src',
        'examples',
        'tests',
        'assets'
    ]
    
    files = {
        'src/__init__.py': '# Source code utama aplikasi MatrixTransform2D',
        'src/main.py': '# Entry point aplikasi\n# Import dan jalankan aplikasi dari sini',
        'src/matrix.py': '# Implementasi transformasi matriks (Translasi, Rotasi, Skala)',
        'src/graphics.py': '# Class untuk rendering objek 2D',
        'src/ui.py': '# User interface dan kontrol aplikasi',
        'examples/__init__.py': '# Contoh penggunaan',
        'tests/__init__.py': '# Unit tests',
        'tests/test_matrix.py': '# Test untuk transformasi matriks'
    }
    
    print("📁 Membuat struktur direktori...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   ⚠️  Already exists: {directory}/")
    
    print()
    print("📄 Membuat file template...")
    for file_path, content in files.items():
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Created: {file_path}")
        else:
            print(f"   ⚠️  Already exists: {file_path}")
    
    print()
    print("=" * 60)
    print("✅ Struktur project berhasil dibuat!")
    print("=" * 60)
    print()
    print("Struktur project:")
    print("MatrixTransform2D/")
    for directory in directories:
        print(f"├── {directory}/")
    print("└── ...")
    print()
    print("Selanjutnya:")
    print("1. Jalankan 'python install.py' untuk install package")
    print("2. Mulai coding di folder src/")

if __name__ == "__main__":
    create_directory_structure()

