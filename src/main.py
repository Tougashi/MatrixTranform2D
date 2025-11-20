"""
Entry point aplikasi MatrixTransform2D
Aplikasi Desain Grafis 2D dengan Transformasi Matriks (Translasi, Rotasi, Skala)
"""

import pygame
import sys
from typing import List, Optional
from .graphics import (
    Rectangle, Triangle, Circle, Line, Polygon, 
    Grid, Axis, Shape2D
)
from .ui import ControlPanel
from .matrix import TransformationMatrix


class MatrixTransform2DApp:
    """Main application class"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        """
        Initialize aplikasi
        Args:
            width: Lebar window
            height: Tinggi window
        """
        pygame.init()
        
        # Window settings
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("MatrixTransform2D - Transformasi Matriks (Translasi, Rotasi, Skala)")
        
        # Clock untuk FPS control
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Colors
        self.bg_color = (255, 255, 255)
        self.grid_color = (230, 230, 230)
        
        # Canvas area (area untuk menggambar objek)
        self.canvas_x = 0
        self.canvas_y = 0
        self.canvas_width = width - 300  # 300px untuk control panel
        self.canvas_height = height
        
        # Grid
        self.grid = Grid(self.canvas_width, self.canvas_height, 
                        spacing=50, color=self.grid_color)
        
        # Axis (origin di center canvas)
        self.origin_x = self.canvas_width // 2
        self.origin_y = self.canvas_height // 2
        self.axis = Axis(self.canvas_width, self.canvas_height,
                        self.origin_x, self.origin_y)
        
        # Control panel
        panel_x = self.canvas_width
        panel_y = 0
        panel_width = width - self.canvas_width
        panel_height = height
        self.control_panel = ControlPanel(panel_x, panel_y, panel_width, panel_height)
        self.control_panel.on_transform_changed = self._on_transform_changed
        
        # Shapes (objek 2D yang bisa di-transform)
        self.shapes: List[Shape2D] = []
        
        # Selected shape
        self.selected_shape: Optional[Shape2D] = None
        self.selected_shape_index = 0
        
        # Camera offset (untuk scrolling)
        self.camera_x = 0
        self.camera_y = 0
        
        # Initialize default shapes
        self._create_default_shapes()
        
        # Running state
        self.running = True
    
    def _create_default_shapes(self):
        """Create default shapes untuk demo"""
        # Rectangle di center
        rect = Rectangle(
            self.origin_x - 50, self.origin_y - 30,
            100, 60,
            color=(0, 150, 255), fill=True
        )
        self.shapes.append(rect)
        
        # Triangle
        triangle = Triangle(
            self.origin_x - 40, self.origin_y + 50,
            self.origin_x + 0, self.origin_y + 100,
            self.origin_x + 40, self.origin_y + 50,
            color=(255, 150, 0), fill=True
        )
        self.shapes.append(triangle)
        
        # Circle
        circle = Circle(
            self.origin_x, self.origin_y - 100,
            40,
            color=(150, 255, 150), fill=True
        )
        self.shapes.append(circle)
        
        # Polygon (pentagon)
        import math
        pentagon_points = []
        for i in range(5):
            angle = 2 * math.pi * i / 5 - math.pi / 2
            x = self.origin_x + 50 * math.cos(angle)
            y = self.origin_y - 150 + 50 * math.sin(angle)
            pentagon_points.append((x, y))
        
        pentagon = Polygon(pentagon_points, color=(255, 100, 150), fill=True)
        self.shapes.append(pentagon)
        
        # Select first shape by default
        if self.shapes:
            self.selected_shape = self.shapes[0]
    
    def _on_transform_changed(self, matrix: TransformationMatrix):
        """Callback saat transformasi berubah dari control panel"""
        if self.selected_shape:
            self.selected_shape.apply_transform(matrix)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                self.running = False
            
            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            # Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            
            # Handle control panel events
            self.control_panel.handle_event(event)
    
    def _handle_keydown(self, event: pygame.event.Event):
        """Handle keyboard key press"""
        if event.key == pygame.K_ESCAPE:
            self.running = False
        
        # Switch between shapes
        elif event.key == pygame.K_TAB:
            if self.shapes:
                self.selected_shape_index = (self.selected_shape_index + 1) % len(self.shapes)
                self.selected_shape = self.shapes[self.selected_shape_index]
                # Update control panel dengan transformasi shape saat ini
                if self.selected_shape:
                    self.selected_shape.reset_transform()
                    self.control_panel.reset_transform()
        
        # Reset transformasi
        elif event.key == pygame.K_r:
            if self.selected_shape:
                self.selected_shape.reset_transform()
                self.control_panel.reset_transform()
        
        # Camera movement
        elif event.key == pygame.K_LEFT:
            self.camera_x += 20
        elif event.key == pygame.K_RIGHT:
            self.camera_x -= 20
        elif event.key == pygame.K_UP:
            self.camera_y += 20
        elif event.key == pygame.K_DOWN:
            self.camera_y -= 20
    
    def _handle_mouse_down(self, event: pygame.event.Event):
        """Handle mouse button down"""
        if event.button == 1:  # Left click
            # Check if clicked on canvas area (not control panel)
            if 0 <= event.pos[0] < self.canvas_width:
                # Check if clicked on any shape
                clicked_shape = None
                for shape in reversed(self.shapes):  # Check from top to bottom
                    points = shape.get_points(transformed=True)
                    if self._point_in_shape(event.pos, points):
                        clicked_shape = shape
                        break
                
                if clicked_shape:
                    self.selected_shape = clicked_shape
                    self.selected_shape_index = self.shapes.index(clicked_shape)
                    # Reset transformasi untuk shape yang dipilih
                    clicked_shape.reset_transform()
                    self.control_panel.reset_transform()
    
    def _point_in_shape(self, point: tuple, points: List[tuple]) -> bool:
        """Check if point is inside shape (simple bounding box check)"""
        if len(points) < 2:
            return False
        
        x, y = point
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def update(self):
        """Update game state (called every frame)"""
        # Update transformation matrix untuk selected shape
        if self.selected_shape:
            matrix = self.control_panel.get_transform_matrix()
            self.selected_shape.apply_transform(matrix)
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(self.bg_color)
        
        # Create surface untuk canvas
        canvas_surface = pygame.Surface((self.canvas_width, self.canvas_height))
        canvas_surface.fill(self.bg_color)
        
        # Draw grid
        self.grid.draw(canvas_surface, self.camera_x, self.camera_y)
        
        # Draw axes
        self.axis.draw(canvas_surface)
        
        # Apply camera offset untuk shapes
        camera_matrix = TransformationMatrix()
        camera_matrix.translate(self.camera_x, self.camera_y)
        
        # Draw all shapes
        for i, shape in enumerate(self.shapes):
            # Combine camera and shape transformations
            combined_matrix = TransformationMatrix()
            combined_matrix.compose(camera_matrix)
            combined_matrix.compose(shape.transform_matrix)
            
            # Temporarily apply combined transform
            original_matrix = shape.transform_matrix
            shape.apply_transform(combined_matrix)
            
            # Draw shape
            is_selected = (shape == self.selected_shape)
            shape.draw(canvas_surface, draw_center=is_selected)
            
            # Draw selection highlight
            if is_selected:
                points = shape.get_points(transformed=True)
                if len(points) >= 2:
                    for j in range(len(points)):
                        start = points[j]
                        end = points[(j + 1) % len(points)]
                        pygame.draw.line(canvas_surface, (255, 0, 0), start, end, 3)
            
            # Restore original transform
            shape.transform_matrix = original_matrix
            shape.transformed_points = [
                p.transform(original_matrix) for p in shape.original_points
            ]
        
        # Draw canvas ke screen
        self.screen.blit(canvas_surface, (self.canvas_x, self.canvas_y))
        
        # Draw control panel
        self.control_panel.draw(self.screen)
        
        # Draw info text
        self._draw_info()
        
        # Update display
        pygame.display.flip()
    
    def _draw_info(self):
        """Draw info text di canvas"""
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            "MatrixTransform2D - Transformasi Matriks 2D",
            f"Selected: Shape {self.selected_shape_index + 1}/{len(self.shapes)}",
            "Controls:",
            "  TAB - Switch shape",
            "  R - Reset transform",
            "  Arrow Keys - Move camera",
            "  Click shape to select"
        ]
        
        y_offset = 10
        for i, line in enumerate(info_lines):
            color = (0, 0, 0) if i == 0 else (100, 100, 100)
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
    
    def run(self):
        """Main game loop"""
        print("=" * 60)
        print("MatrixTransform2D - Aplikasi Transformasi Matriks 2D")
        print("=" * 60)
        print()
        print("Controls:")
        print("  TAB - Switch between shapes")
        print("  R - Reset transformation")
        print("  Arrow Keys - Move camera")
        print("  Left Click - Select shape")
        print("  ESC - Quit")
        print()
        print("Using sliders in control panel to transform selected shape")
        print()
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.draw()
            
            # Control FPS
            self.clock.tick(self.fps)
        
        # Cleanup
        pygame.quit()
        print("Aplikasi ditutup. Terima kasih!")


def main():
    """Main entry point"""
    try:
        app = MatrixTransform2DApp(width=1200, height=800)
        app.run()
    except KeyboardInterrupt:
        print("\nAplikasi dihentikan oleh user.")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
