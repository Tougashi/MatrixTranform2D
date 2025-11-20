"""
Contoh penggunaan MatrixTransform2D API
Demonstrasi transformasi matriks pada objek 2D
"""

import sys
import os

# Add parent directory ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.matrix import TransformationMatrix, Transform2D
from src.graphics import Rectangle, Triangle, Circle, Point2D
import math


def demo_transformation_matrix():
    """Demo penggunaan TransformationMatrix"""
    print("=" * 60)
    print("Demo: TransformationMatrix")
    print("=" * 60)
    print()
    
    # Buat matrix transformasi
    matrix = TransformationMatrix()
    
    # Test translasi
    print("1. Translasi (50, 30):")
    matrix.translate(50, 30)
    point = matrix.apply_to_point(0, 0)
    print(f"   Point (0, 0) -> {point}")
    print(f"   Matrix:\n{matrix.get_matrix()}")
    print()
    
    # Test rotasi
    print("2. Rotasi 45 derajat:")
    matrix.rotate(45)
    point = matrix.apply_to_point(100, 0)
    print(f"   Point (100, 0) -> ({point[0]:.2f}, {point[1]:.2f})")
    print()
    
    # Test skala
    print("3. Skala (2x, 2y):")
    matrix.scale(2, 2)
    point = matrix.apply_to_point(50, 50)
    print(f"   Point (50, 50) -> ({point[0]:.2f}, {point[1]:.2f})")
    print()
    
    # Reset dan test kombinasi
    matrix.reset()
    print("4. Kombinasi transformasi (Translate -> Rotate -> Scale):")
    matrix.translate(100, 100)
    matrix.rotate(90, 100, 100)  # Rotate around center
    matrix.scale(1.5, 1.5, 100, 100)  # Scale around center
    print(f"   Matrix:\n{matrix.get_matrix()}")
    print()


def demo_transform2d():
    """Demo penggunaan Transform2D"""
    print("=" * 60)
    print("Demo: Transform2D")
    print("=" * 60)
    print()
    
    transform = Transform2D()
    transform.translation_x = 50
    transform.translation_y = 30
    transform.rotation_angle = 45
    transform.scale_x = 2.0
    transform.scale_y = 1.5
    
    print(f"Transform parameters: {transform}")
    matrix = transform.get_matrix()
    print(f"Matrix:\n{matrix.get_matrix()}")
    print()


def demo_shape_transformation():
    """Demo transformasi pada shape"""
    print("=" * 60)
    print("Demo: Shape Transformation")
    print("=" * 60)
    print()
    
    # Buat rectangle
    rect = Rectangle(0, 0, 100, 50, color=(0, 0, 255))
    print(f"Original rectangle points:")
    for i, point in enumerate(rect.get_points(transformed=False)):
        print(f"   Point {i+1}: {point}")
    print()
    
    # Terapkan transformasi
    matrix = TransformationMatrix()
    matrix.translate(200, 100)
    matrix.rotate(30)
    matrix.scale(1.5, 1.5)
    
    rect.apply_transform(matrix)
    print(f"Transformed rectangle points:")
    for i, point in enumerate(rect.get_points(transformed=True)):
        print(f"   Point {i+1}: ({point[0]:.2f}, {point[1]:.2f})")
    print()
    
    # Reset
    rect.reset_transform()
    print(f"After reset - Original points restored")
    for i, point in enumerate(rect.get_points(transformed=False)):
        print(f"   Point {i+1}: {point}")
    print()


def demo_rotation_around_point():
    """Demo rotasi terhadap titik tertentu"""
    print("=" * 60)
    print("Demo: Rotation Around Point")
    print("=" * 60)
    print()
    
    # Buat triangle di center (100, 100)
    triangle = Triangle(80, 90, 120, 90, 100, 110, color=(255, 0, 0))
    center = triangle.get_center()
    print(f"Triangle center: {center}")
    print()
    
    # Rotasi 90 derajat terhadap center
    matrix = TransformationMatrix()
    matrix.rotate(90, center[0], center[1])
    triangle.apply_transform(matrix)
    
    print(f"After 90° rotation around center:")
    for i, point in enumerate(triangle.get_points(transformed=True)):
        print(f"   Point {i+1}: ({point[0]:.2f}, {point[1]:.2f})")
    print()


def demo_scale_around_point():
    """Demo skala terhadap titik tertentu"""
    print("=" * 60)
    print("Demo: Scale Around Point")
    print("=" * 60)
    print()
    
    # Buat circle
    circle = Circle(100, 100, 50, color=(0, 255, 0))
    center = circle.get_center()
    print(f"Circle center: {center}")
    print(f"Original radius: {circle.radius}")
    print()
    
    # Skala 2x terhadap center
    matrix = TransformationMatrix()
    matrix.scale(2.0, 2.0, center[0], center[1])
    circle.apply_transform(matrix)
    
    print(f"After 2x scale around center:")
    # Hitung approximate radius baru
    points = circle.get_points(transformed=True)
    if len(points) > 0:
        first_point = points[0]
        new_center_x = sum(p[0] for p in points) / len(points)
        new_center_y = sum(p[1] for p in points) / len(points)
        dx = first_point[0] - new_center_x
        dy = first_point[1] - new_center_y
        new_radius = math.sqrt(dx*dx + dy*dy)
        print(f"   Approximate new radius: {new_radius:.2f}")
        print(f"   (Expected: {circle.radius * 2:.2f})")
    print()


def main():
    """Run semua demo"""
    print("\n" + "=" * 60)
    print("MatrixTransform2D - API Demo")
    print("=" * 60)
    print()
    
    try:
        demo_transformation_matrix()
        demo_transform2d()
        demo_shape_transformation()
        demo_rotation_around_point()
        demo_scale_around_point()
        
        print("=" * 60)
        print("✅ Semua demo selesai!")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

