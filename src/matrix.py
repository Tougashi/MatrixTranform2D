"""
Implementasi transformasi matriks (Translasi, Rotasi, Skala)
Menggunakan NumPy untuk operasi matriks 2D
"""

import numpy as np
import math


class TransformationMatrix:
    """Class untuk transformasi matriks 2D"""
    
    def __init__(self):
        """Initialize dengan identity matrix"""
        self.matrix = np.eye(3, dtype=np.float64)
    
    def reset(self):
        """Reset ke identity matrix"""
        self.matrix = np.eye(3, dtype=np.float64)
        return self
    
    def translate(self, tx, ty):
        """
        Translasi (pergeseran) objek
        Args:
            tx: Pergeseran pada sumbu X
            ty: Pergeseran pada sumbu Y
        Returns:
            self untuk method chaining
        """
        translation_matrix = np.array([
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ], dtype=np.float64)
        
        self.matrix = np.dot(self.matrix, translation_matrix)
        return self
    
    def rotate(self, angle_degrees, pivot_x=0, pivot_y=0):
        """
        Rotasi objek terhadap titik pivot
        Args:
            angle_degrees: Sudut rotasi dalam derajat (counter-clockwise)
            pivot_x: Koordinat X titik pivot rotasi (default: 0,0)
            pivot_y: Koordinat Y titik pivot rotasi (default: 0,0)
        Returns:
            self untuk method chaining
        """
        # Konversi derajat ke radian
        angle_rad = math.radians(angle_degrees)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Jika pivot bukan di origin, kita perlu:
        # 1. Translate ke origin
        # 2. Rotate
        # 3. Translate kembali
        
        if pivot_x != 0 or pivot_y != 0:
            # Translate ke origin
            self.translate(-pivot_x, -pivot_y)
        
        # Matriks rotasi
        rotation_matrix = np.array([
            [cos_a, -sin_a, 0],
            [sin_a,  cos_a, 0],
            [0,      0,     1]
        ], dtype=np.float64)
        
        self.matrix = np.dot(self.matrix, rotation_matrix)
        
        # Translate kembali jika pivot bukan di origin
        if pivot_x != 0 or pivot_y != 0:
            self.translate(pivot_x, pivot_y)
        
        return self
    
    def scale(self, sx, sy=None, pivot_x=0, pivot_y=0):
        """
        Skala (perbesar/perkecil) objek terhadap titik pivot
        Args:
            sx: Skala pada sumbu X
            sy: Skala pada sumbu Y (jika None, menggunakan sx untuk uniform scaling)
            pivot_x: Koordinat X titik pivot scaling (default: 0,0)
            pivot_y: Koordinat Y titik pivot scaling (default: 0,0)
        Returns:
            self untuk method chaining
        """
        if sy is None:
            sy = sx  # Uniform scaling
        
        # Jika pivot bukan di origin, kita perlu:
        # 1. Translate ke origin
        # 2. Scale
        # 3. Translate kembali
        
        if pivot_x != 0 or pivot_y != 0:
            # Translate ke origin
            self.translate(-pivot_x, -pivot_y)
        
        # Matriks skala
        scale_matrix = np.array([
            [sx, 0,  0],
            [0,  sy, 0],
            [0,  0,  1]
        ], dtype=np.float64)
        
        self.matrix = np.dot(self.matrix, scale_matrix)
        
        # Translate kembali jika pivot bukan di origin
        if pivot_x != 0 or pivot_y != 0:
            self.translate(pivot_x, pivot_y)
        
        return self
    
    def apply_to_point(self, x, y):
        """
        Terapkan transformasi ke sebuah titik
        Args:
            x: Koordinat X titik
            y: Koordinat Y titik
        Returns:
            Tuple (new_x, new_y) setelah transformasi
        """
        # Buat vektor homogen [x, y, 1]
        point = np.array([x, y, 1], dtype=np.float64)
        
        # Terapkan transformasi
        transformed = np.dot(self.matrix, point)
        
        return (transformed[0], transformed[1])
    
    def apply_to_points(self, points):
        """
        Terapkan transformasi ke array of points
        Args:
            points: List of tuples [(x1,y1), (x2,y2), ...]
        Returns:
            List of tuples dengan koordinat yang sudah ditransformasi
        """
        if len(points) == 0:
            return []
        
        # Convert ke numpy array
        points_array = np.array([(x, y, 1) for x, y in points], dtype=np.float64).T
        
        # Terapkan transformasi
        transformed = np.dot(self.matrix, points_array)
        
        # Convert kembali ke list of tuples
        return [(transformed[0, i], transformed[1, i]) for i in range(transformed.shape[1])]
    
    def get_matrix(self):
        """Get matrix transformasi saat ini"""
        return self.matrix.copy()
    
    def set_matrix(self, matrix):
        """Set matrix transformasi"""
        self.matrix = np.array(matrix, dtype=np.float64)
        return self
    
    def compose(self, other):
        """
        Komposisi transformasi dengan transformasi lain
        Args:
            other: TransformationMatrix lainnya
        Returns:
            self untuk method chaining
        """
        self.matrix = np.dot(self.matrix, other.matrix)
        return self
    
    def __str__(self):
        """String representation untuk debugging"""
        return f"TransformationMatrix:\n{self.matrix}"
    
    def __repr__(self):
        """Representation untuk debugging"""
        return self.__str__()


class Transform2D:
    """
    Helper class untuk transformasi 2D yang lebih sederhana
    Menyimpan parameter transformasi secara terpisah
    """
    
    def __init__(self):
        self.translation_x = 0.0
        self.translation_y = 0.0
        self.rotation_angle = 0.0  # dalam derajat
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.pivot_x = 0.0
        self.pivot_y = 0.0
    
    def get_matrix(self):
        """Get TransformationMatrix dari parameter saat ini"""
        matrix = TransformationMatrix()
        
        # Urutan: Translate -> Rotate -> Scale
        # (atau bisa disesuaikan dengan kebutuhan)
        if self.scale_x != 1.0 or self.scale_y != 1.0:
            matrix.scale(self.scale_x, self.scale_y, self.pivot_x, self.pivot_y)
        
        if self.rotation_angle != 0.0:
            matrix.rotate(self.rotation_angle, self.pivot_x, self.pivot_y)
        
        if self.translation_x != 0.0 or self.translation_y != 0.0:
            matrix.translate(self.translation_x, self.translation_y)
        
        return matrix
    
    def reset(self):
        """Reset semua parameter ke default"""
        self.translation_x = 0.0
        self.translation_y = 0.0
        self.rotation_angle = 0.0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.pivot_x = 0.0
        self.pivot_y = 0.0
        return self
    
    def __str__(self):
        return (f"Transform2D(tx={self.translation_x:.2f}, ty={self.translation_y:.2f}, "
                f"rot={self.rotation_angle:.2f}°, "
                f"sx={self.scale_x:.2f}, sy={self.scale_y:.2f})")
