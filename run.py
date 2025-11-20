"""
File untuk menjalankan aplikasi MatrixTransform2D
Jalankan dengan: python run.py
"""

import sys
import os

# Add src directory ke Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import dan jalankan aplikasi
from src.main import main

if __name__ == "__main__":
    main()

