"""
Source code utama aplikasi MatrixTransform2D
Aplikasi Desain Grafis 2D dengan Transformasi Matriks (Translasi, Rotasi, Skala)
"""

from .main import MatrixTransform2DApp, main
from .matrix import TransformationMatrix, Transform2D
from .graphics import (
    Point2D, Shape2D, Rectangle, Triangle, Circle, Line, Polygon,
    Grid, Axis
)
from .ui import Button, Slider, TextLabel, ControlPanel

__version__ = "1.0.0"
__all__ = [
    "MatrixTransform2DApp",
    "main",
    "TransformationMatrix",
    "Transform2D",
    "Point2D",
    "Shape2D",
    "Rectangle",
    "Triangle",
    "Circle",
    "Line",
    "Polygon",
    "Grid",
    "Axis",
    "Button",
    "Slider",
    "TextLabel",
    "ControlPanel",
]
