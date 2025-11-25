"""
Class untuk rendering objek 2D
Menggunakan Pygame untuk rendering
"""

import pygame
import math
from typing import List, Tuple
from .matrix import TransformationMatrix


class Point2D:
    """Class untuk merepresentasikan titik 2D"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert ke tuple (x, y)"""
        return (self.x, self.y)
    
    def transform(self, matrix: TransformationMatrix) -> 'Point2D':
        """Terapkan transformasi matriks ke titik"""
        new_x, new_y = matrix.apply_to_point(self.x, self.y)
        return Point2D(new_x, new_y)
    
    def __repr__(self):
        return f"Point2D({self.x:.2f}, {self.y:.2f})"


class Shape2D:
    """Base class untuk objek 2D"""
    
    def __init__(self, points: List[Tuple[float, float]], color=(0, 0, 255), fill=True):
        """
        Args:
            points: List of tuples [(x1,y1), (x2,y2), ...]
            color: RGB color tuple (default: blue)
            fill: True untuk filled shape, False untuk outline only
        """
        self.original_points = [Point2D(x, y) for x, y in points]
        self.transformed_points = self.original_points.copy()
        self.color = color
        self.fill = fill
        self.transform_matrix = TransformationMatrix()
        self.center = self._calculate_center()
    
    def _calculate_center(self) -> Tuple[float, float]:
        """Hitung center point dari shape"""
        if len(self.original_points) == 0:
            return (0, 0)
        
        sum_x = sum(p.x for p in self.original_points)
        sum_y = sum(p.y for p in self.original_points)
        count = len(self.original_points)
        
        return (sum_x / count, sum_y / count)
    
    def get_center(self) -> Tuple[float, float]:
        """Get center point"""
        return self.center
    
    def apply_transform(self, matrix: TransformationMatrix):
        """Terapkan transformasi matriks ke shape"""
        self.transform_matrix = matrix
        self.transformed_points = [
            p.transform(matrix) for p in self.original_points
        ]
    
    def reset_transform(self):
        """Reset transformasi"""
        self.transform_matrix.reset()
        self.transformed_points = self.original_points.copy()
    
    def get_points(self, transformed=True) -> List[Tuple[int, int]]:
        """
        Get points sebagai list of tuples untuk pygame
        Args:
            transformed: True untuk transformed points, False untuk original
        Returns:
            List of tuples dengan koordinat integer untuk pygame
        """
        points = self.transformed_points if transformed else self.original_points
        return [(int(p.x), int(p.y)) for p in points]
    
    def draw(self, surface: pygame.Surface, draw_center=False, zoom_factor=1.0):
        """
        Draw shape ke pygame surface
        Args:
            surface: Pygame surface untuk drawing
            draw_center: True untuk draw center point
            zoom_factor: Camera zoom factor for scaling the center dot
        """
        points = self.get_points(transformed=True)
        
        if len(points) < 2:
            return
        
        # Draw filled polygon atau outline
        if self.fill and len(points) >= 3:
            pygame.draw.polygon(surface, self.color, points)
        else:
            # Draw lines between points
            for i in range(len(points)):
                start = points[i]
                end = points[(i + 1) % len(points)]
                pygame.draw.line(surface, self.color, start, end, 2)
        
        # Draw center point jika diminta
        if draw_center:
            center_x, center_y = int(self.center[0]), int(self.center[1])
            # Transform center point juga
            if self.transform_matrix:
                center_x, center_y = self.transform_matrix.apply_to_point(
                    self.center[0], self.center[1]
                )
                center_x, center_y = int(center_x), int(center_y)
            # Scale center dot radius with gentler zoom curve
            center_radius = int(max(3, min(8, 5 * zoom_factor)))
            pygame.draw.circle(surface, (255, 0, 0), (center_x, center_y), center_radius)


class Rectangle(Shape2D):
    """Class untuk rectangle"""
    
    def __init__(self, x: float, y: float, width: float, height: float, 
                 color=(0, 0, 255), fill=True):
        """
        Args:
            x, y: Posisi top-left corner
            width: Lebar rectangle
            height: Tinggi rectangle
            color: RGB color tuple
            fill: True untuk filled, False untuk outline
        """
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]
        super().__init__(points, color, fill)
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Triangle(Shape2D):
    """Class untuk triangle"""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float, 
                 x3: float, y3: float, color=(0, 0, 255), fill=True):
        """
        Args:
            x1, y1, x2, y2, x3, y3: Koordinat tiga titik triangle
            color: RGB color tuple
            fill: True untuk filled, False untuk outline
        """
        points = [(x1, y1), (x2, y2), (x3, y3)]
        super().__init__(points, color, fill)


class Circle(Shape2D):
    """Class untuk circle (approximated dengan polygon)"""
    
    def __init__(self, center_x: float, center_y: float, radius: float,
                 color=(0, 0, 255), fill=True, segments=32):
        """
        Args:
            center_x, center_y: Center point circle
            radius: Radius circle
            color: RGB color tuple
            fill: True untuk filled, False untuk outline
            segments: Jumlah segment untuk aproksimasi circle
        """
        # Generate points untuk circle
        points = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((x, y))
        
        super().__init__(points, color, fill)
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.segments = segments


class Line(Shape2D):
    """Class untuk line"""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float,
                 color=(0, 0, 255), thickness=2):
        """
        Args:
            x1, y1: Start point
            x2, y2: End point
            color: RGB color tuple
            thickness: Ketebalan line
        """
        points = [(x1, y1), (x2, y2)]
        super().__init__(points, color, fill=False)
        self.thickness = thickness
    
    def draw(self, surface: pygame.Surface, draw_center=False, zoom_factor=1.0):
        """Override draw untuk line khusus
        Args:
            surface: Pygame surface untuk drawing
            draw_center: True untuk draw center point
            zoom_factor: Camera zoom factor for scaling the center dot
        """
        points = self.get_points(transformed=True)
        if len(points) >= 2:
            pygame.draw.line(surface, self.color, points[0], points[1], self.thickness)
        
        if draw_center:
            center_x, center_y = int(self.center[0]), int(self.center[1])
            if self.transform_matrix:
                center_x, center_y = self.transform_matrix.apply_to_point(
                    self.center[0], self.center[1]
                )
                center_x, center_y = int(center_x), int(center_y)
            # Scale center dot radius with gentler zoom curve
            center_radius = int(max(3, min(8, 5 * zoom_factor)))
            pygame.draw.circle(surface, (255, 0, 0), (center_x, center_y), center_radius)


class Polygon(Shape2D):
    """Class untuk polygon dengan banyak titik"""
    
    def __init__(self, points: List[Tuple[float, float]], 
                 color=(0, 0, 255), fill=True):
        """
        Args:
            points: List of tuples [(x1,y1), (x2,y2), ...]
            color: RGB color tuple
            fill: True untuk filled, False untuk outline
        """
        super().__init__(points, color, fill)


class Grid:
    """Class untuk menggambar grid di background"""
    
    def __init__(self, width: int, height: int, spacing: int = 50, 
                 color=(200, 200, 200)):
        """
        Args:
            width: Lebar area grid
            height: Tinggi area grid
            spacing: Jarak antar grid lines
            color: Warna grid lines
        """
        self.width = width
        self.height = height
        self.spacing = spacing
        self.color = color
    
    def draw(self, surface: pygame.Surface, offset_x=0, offset_y=0):
        """
        Draw grid ke surface
        Args:
            surface: Pygame surface
            offset_x, offset_y: Offset untuk scrolling
        """
        # Vertical lines
        start_x = (-offset_x % self.spacing) - self.spacing
        for x in range(int(start_x), self.width + self.spacing, self.spacing):
            pygame.draw.line(surface, self.color, (x, 0), (x, self.height), 1)
        
        # Horizontal lines
        start_y = (-offset_y % self.spacing) - self.spacing
        for y in range(int(start_y), self.height + self.spacing, self.spacing):
            pygame.draw.line(surface, self.color, (0, y), (self.width, y), 1)
        
        # Draw axes (origin lines)
        origin_x = int(-offset_x)
        origin_y = int(-offset_y)
        
        if 0 <= origin_x <= self.width:
            pygame.draw.line(surface, (150, 150, 150), 
                           (origin_x, 0), (origin_x, self.height), 2)
        if 0 <= origin_y <= self.height:
            pygame.draw.line(surface, (150, 150, 150), 
                           (0, origin_y), (self.width, origin_y), 2)


class Axis:
    """Class untuk menggambar axes (sumbu X dan Y)"""
    
    def __init__(self, width: int, height: int, origin_x: int = 0, origin_y: int = 0,
                 arrow_size: int = 10, color=(100, 100, 100)):
        """
        Args:
            width: Lebar area
            height: Tinggi area
            origin_x, origin_y: Posisi origin (0,0)
            arrow_size: Ukuran arrow head
            color: Warna axes
        """
        self.width = width
        self.height = height
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.arrow_size = arrow_size
        self.color = color
    
    def draw(self, surface: pygame.Surface):
        """Draw axes dengan arrow heads"""
        # X-axis
        if 0 <= self.origin_y <= self.height:
            pygame.draw.line(surface, self.color, 
                           (0, self.origin_y), (self.width, self.origin_y), 2)
            # Arrow head untuk X-axis
            pygame.draw.polygon(surface, self.color, [
                (self.width, self.origin_y),
                (self.width - self.arrow_size, self.origin_y - self.arrow_size // 2),
                (self.width - self.arrow_size, self.origin_y + self.arrow_size // 2)
            ])
        
        # Y-axis
        if 0 <= self.origin_x <= self.width:
            pygame.draw.line(surface, self.color, 
                           (self.origin_x, 0), (self.origin_x, self.height), 2)
            # Arrow head untuk Y-axis
            pygame.draw.polygon(surface, self.color, [
                (self.origin_x, 0),
                (self.origin_x - self.arrow_size // 2, self.arrow_size),
                (self.origin_x + self.arrow_size // 2, self.arrow_size)
            ])
        
        # Label origin
        font = pygame.font.Font(None, 24)
        text = font.render("O", True, self.color)
        surface.blit(text, (self.origin_x + 5, self.origin_y + 5))
