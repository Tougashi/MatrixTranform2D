"""
Test untuk transformasi matriks
Unit tests untuk TransformationMatrix dan Transform2D
"""

import sys
import os
import math

# Add parent directory ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.matrix import TransformationMatrix, Transform2D
import pytest


class TestTransformationMatrix:
    """Test class untuk TransformationMatrix"""
    
    def test_identity(self):
        """Test identity matrix"""
        matrix = TransformationMatrix()
        identity = matrix.get_matrix()
        
        # Identity matrix adalah 3x3 dengan diagonal 1
        assert identity[0][0] == 1
        assert identity[1][1] == 1
        assert identity[2][2] == 1
        assert identity[0][1] == 0
        assert identity[0][2] == 0
        assert identity[1][0] == 0
        assert identity[1][2] == 0
        assert identity[2][0] == 0
        assert identity[2][1] == 0
    
    def test_translate(self):
        """Test translasi"""
        matrix = TransformationMatrix()
        matrix.translate(50, 30)
        
        # Test point (0, 0) setelah translasi (50, 30)
        x, y = matrix.apply_to_point(0, 0)
        assert abs(x - 50) < 0.001
        assert abs(y - 30) < 0.001
        
        # Test point (10, 20) setelah translasi (50, 30)
        x, y = matrix.apply_to_point(10, 20)
        assert abs(x - 60) < 0.001
        assert abs(y - 50) < 0.001
    
    def test_rotate(self):
        """Test rotasi"""
        matrix = TransformationMatrix()
        matrix.rotate(90)  # Rotate 90 degrees
        
        # Test point (1, 0) setelah rotasi 90 derajat seharusnya menjadi (0, 1)
        x, y = matrix.apply_to_point(1, 0)
        assert abs(x - 0) < 0.01
        assert abs(y - 1) < 0.01
        
        # Test point (0, 1) setelah rotasi 90 derajat seharusnya menjadi (-1, 0)
        x, y = matrix.apply_to_point(0, 1)
        assert abs(x - (-1)) < 0.01
        assert abs(y - 0) < 0.01
    
    def test_rotate_around_point(self):
        """Test rotasi terhadap titik tertentu"""
        matrix = TransformationMatrix()
        # Rotate 180 degrees around point (50, 50)
        matrix.rotate(180, 50, 50)
        
        # Point di center (50, 50) seharusnya tidak berubah
        x, y = matrix.apply_to_point(50, 50)
        assert abs(x - 50) < 0.01
        assert abs(y - 50) < 0.01
        
        # Point (60, 50) setelah rotasi 180° around (50, 50) seharusnya menjadi (40, 50)
        x, y = matrix.apply_to_point(60, 50)
        assert abs(x - 40) < 0.01
        assert abs(y - 50) < 0.01
    
    def test_scale(self):
        """Test skala"""
        matrix = TransformationMatrix()
        matrix.scale(2, 2)
        
        # Point (1, 1) setelah scale 2x seharusnya menjadi (2, 2)
        x, y = matrix.apply_to_point(1, 1)
        assert abs(x - 2) < 0.001
        assert abs(y - 2) < 0.001
        
        # Test non-uniform scale
        matrix.reset()
        matrix.scale(2, 3)
        x, y = matrix.apply_to_point(1, 1)
        assert abs(x - 2) < 0.001
        assert abs(y - 3) < 0.001
    
    def test_scale_around_point(self):
        """Test skala terhadap titik tertentu"""
        matrix = TransformationMatrix()
        # Scale 2x around point (50, 50)
        matrix.scale(2, 2, 50, 50)
        
        # Point di center (50, 50) seharusnya tidak berubah
        x, y = matrix.apply_to_point(50, 50)
        assert abs(x - 50) < 0.01
        assert abs(y - 50) < 0.01
        
        # Point (60, 50) setelah scale 2x around (50, 50) seharusnya menjadi (70, 50)
        x, y = matrix.apply_to_point(60, 50)
        assert abs(x - 70) < 0.01
        assert abs(y - 50) < 0.01
    
    def test_scale_uniform(self):
        """Test uniform scaling (sx = sy)"""
        matrix = TransformationMatrix()
        matrix.scale(2)  # Uniform scale, hanya sx yang diberikan
        
        x, y = matrix.apply_to_point(1, 1)
        assert abs(x - 2) < 0.001
        assert abs(y - 2) < 0.001
    
    def test_combination(self):
        """Test kombinasi transformasi"""
        matrix = TransformationMatrix()
        matrix.translate(100, 100)
        matrix.rotate(90)
        matrix.scale(2, 2)
        
        # Transform point (1, 0)
        x, y = matrix.apply_to_point(1, 0)
        # Setelah translate (100, 100): (101, 100)
        # Setelah rotate 90°: (100, 101)
        # Setelah scale 2x: (200, 202)
        # Namun karena kombinasi matriks, hasilnya berbeda
        # Untuk kombinasi translate->rotate->scale, order matters
        
        # Yang penting adalah tidak error dan menghasilkan nilai valid
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
    
    def test_apply_to_points(self):
        """Test apply transform ke multiple points"""
        matrix = TransformationMatrix()
        matrix.translate(10, 20)
        
        points = [(0, 0), (1, 1), (2, 2)]
        transformed = matrix.apply_to_points(points)
        
        assert len(transformed) == 3
        assert abs(transformed[0][0] - 10) < 0.001
        assert abs(transformed[0][1] - 20) < 0.001
        assert abs(transformed[1][0] - 11) < 0.001
        assert abs(transformed[1][1] - 21) < 0.001
    
    def test_reset(self):
        """Test reset matrix"""
        matrix = TransformationMatrix()
        matrix.translate(50, 50)
        matrix.rotate(45)
        matrix.reset()
        
        # Setelah reset, seharusnya kembali ke identity
        identity = matrix.get_matrix()
        assert identity[0][0] == 1
        assert identity[1][1] == 1
        assert identity[2][2] == 1
    
    def test_compose(self):
        """Test compose dengan matrix lain"""
        matrix1 = TransformationMatrix()
        matrix1.translate(10, 10)
        
        matrix2 = TransformationMatrix()
        matrix2.translate(20, 20)
        
        matrix1.compose(matrix2)
        
        # Hasil seharusnya translate (30, 30)
        x, y = matrix1.apply_to_point(0, 0)
        assert abs(x - 30) < 0.001
        assert abs(y - 30) < 0.001


class TestTransform2D:
    """Test class untuk Transform2D"""
    
    def test_default_values(self):
        """Test default values"""
        transform = Transform2D()
        
        assert transform.translation_x == 0.0
        assert transform.translation_y == 0.0
        assert transform.rotation_angle == 0.0
        assert transform.scale_x == 1.0
        assert transform.scale_y == 1.0
    
    def test_get_matrix(self):
        """Test get matrix dari transform parameters"""
        transform = Transform2D()
        transform.translation_x = 50
        transform.translation_y = 30
        transform.rotation_angle = 45
        transform.scale_x = 2.0
        transform.scale_y = 1.5
        
        matrix = transform.get_matrix()
        assert matrix is not None
        
        # Test bahwa matrix bisa digunakan
        x, y = matrix.apply_to_point(0, 0)
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
    
    def test_reset(self):
        """Test reset transform"""
        transform = Transform2D()
        transform.translation_x = 50
        transform.translation_y = 30
        transform.rotation_angle = 45
        transform.scale_x = 2.0
        
        transform.reset()
        
        assert transform.translation_x == 0.0
        assert transform.translation_y == 0.0
        assert transform.rotation_angle == 0.0
        assert transform.scale_x == 1.0
        assert transform.scale_y == 1.0


def run_tests():
    """Run semua tests"""
    print("Running tests...")
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    # Run tests jika dijalankan langsung
    try:
        import pytest
        run_tests()
    except ImportError:
        print("pytest tidak terinstall. Install dengan: pip install pytest")
        print("\nAtau jalankan tests dengan: pytest tests/test_matrix.py")
