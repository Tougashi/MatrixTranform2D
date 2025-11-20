"""
Script untuk menginstall semua package yang diperlukan untuk MatrixTransform2D
Jalankan file ini dengan: python install.py
"""

import subprocess
import sys
import os

def install_packages():
    """Install semua package dari requirements.txt"""
    print("=" * 60)
    print("MatrixTransform2D - Package Installation")
    print("=" * 60)
    print()
    
    # Cek apakah requirements.txt ada
    if not os.path.exists('requirements.txt'):
        print("❌ Error: requirements.txt tidak ditemukan!")
        print("Pastikan file requirements.txt ada di direktori yang sama.")
        return False
    
    print("📦 Membaca requirements.txt...")
    print()
    
    try:
        # Install package menggunakan pip
        print("🔧 Menginstall package...")
        print("-" * 60)
        
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            check=True,
            capture_output=False
        )
        
        print()
        print("=" * 60)
        print("✅ Semua package berhasil diinstall!")
        print("=" * 60)
        print()
        print("Package yang terinstall:")
        print("- pygame: Framework untuk 2D graphics")
        print("- numpy: Library untuk operasi matriks")
        print("- scipy: Library untuk fungsi matematika")
        print("- Pillow: Library untuk image processing")
        print("- pytest: Framework untuk testing")
        print()
        print("🚀 Sekarang Anda bisa mulai mengembangkan aplikasi!")
        return True
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ Error saat menginstall package!")
        print(f"Error: {e}")
        print()
        print("Coba jalankan secara manual:")
        print("  pip install -r requirements.txt")
        return False
    except Exception as e:
        print()
        print(f"❌ Error tidak terduga: {e}")
        return False

if __name__ == "__main__":
    success = install_packages()
    sys.exit(0 if success else 1)

