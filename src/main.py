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
        self.control_panel.on_zoom_changed = self._on_zoom_changed
        # Connect control panel camera reset to application
        self.control_panel.on_camera_reset = self.reset_camera
        
        # Shapes (objek 2D yang bisa di-transform)
        self.shapes: List[Shape2D] = []
        
        # Selected shape
        self.selected_shape: Optional[Shape2D] = None
        self.selected_shape_index = 0
        
        # Camera offset (untuk scrolling)
        self.camera_x = 0
        self.camera_y = 0
        
        # Camera zoom (1.0 = normal, >1.0 = zoom in, <1.0 = zoom out)
        self.camera_zoom = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.zoom_step = 0.1
        
        # Initialize default shapes
        self._create_default_shapes()
        
        # Running state
        self.running = True
    
    def _create_default_shapes(self):
        """Create default shapes untuk demo"""
        # Rectangle di center
        rect = Rectangle(
            self.origin_x - 50, self.origin_y + 31.25,
            100, 60,
            color=(0, 150, 255), fill=True
        )
        self.shapes.append(rect)
        
        # Triangle
        triangle = Triangle(
            self.origin_x - 50, self.origin_y + 187.5,
            self.origin_x + 0, self.origin_y + 112.5,
            self.origin_x + 50, self.origin_y + 187.5,
            color=(255, 150, 0), fill=True
        )
        self.shapes.append(triangle)
        
        # Circle
        circle = Circle(
            self.origin_x, self.origin_y - 62.5,
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
            y = self.origin_y - 162.5 + 50 * math.sin(angle)
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
    
    def _on_zoom_changed(self, zoom_value: float):
        """Callback saat zoom berubah dari control panel"""
        self.camera_zoom = zoom_value
        # Update zoom slider value display
        if self.control_panel:
            self.control_panel.zoom_slider.set_value(zoom_value)
    
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
            
            # Mouse wheel for zoom
            elif event.type == pygame.MOUSEWHEEL:
                self._handle_mouse_wheel(event)
            
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
        
        # Zoom controls
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
            self.zoom_in()
        elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
            self.zoom_out()
        elif event.key == pygame.K_0:  # Reset zoom
            self.reset_zoom()
        elif event.key == pygame.K_PAGEUP:
            self.zoom_in()
        elif event.key == pygame.K_PAGEDOWN:
            self.zoom_out()
    
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
    
    def _handle_mouse_wheel(self, event: pygame.event.Event):
        """Handle mouse wheel for zoom"""
        # Check if mouse is over canvas area (not control panel)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 0 <= mouse_x < self.canvas_width:
            if event.y > 0:  # Scroll up - zoom in
                self.zoom_in()
            elif event.y < 0:  # Scroll down - zoom out
                self.zoom_out()
    
    def zoom_in(self, factor: float = None):
        """Zoom in camera"""
        if factor is None:
            factor = 1.0 + self.zoom_step
        
        new_zoom = self.camera_zoom * factor
        if new_zoom <= self.max_zoom:
            self.camera_zoom = new_zoom
            # Update zoom slider
            if self.control_panel:
                self.control_panel.set_zoom(self.camera_zoom)
            return True
        return False
    
    def zoom_out(self, factor: float = None):
        """Zoom out camera"""
        if factor is None:
            factor = 1.0 / (1.0 + self.zoom_step)
        
        new_zoom = self.camera_zoom * factor
        if new_zoom >= self.min_zoom:
            self.camera_zoom = new_zoom
            # Update zoom slider
            if self.control_panel:
                self.control_panel.set_zoom(self.camera_zoom)
            return True
        return False
    
    def reset_zoom(self):
        """Reset zoom ke default (1.0)"""
        self.camera_zoom = 1.0
        # Update zoom slider
        if self.control_panel:
            self.control_panel.set_zoom(self.camera_zoom)

    def reset_camera(self):
        """Reset kamera: posisi offset dan zoom kembali ke default"""
        self.camera_x = 0
        self.camera_y = 0
        self.camera_zoom = 1.0
        # Update control panel zoom slider
        if self.control_panel:
            self.control_panel.set_zoom(self.camera_zoom)
    
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
        
        # Apply camera transform (zoom + translate)
        # Transform ke center canvas dulu, lalu zoom, lalu translate kembali
        camera_matrix = TransformationMatrix()
        
        # Translate ke center canvas untuk zoom dari center
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        camera_matrix.translate(center_x, center_y)
        
        # Apply zoom
        camera_matrix.scale(self.camera_zoom, self.camera_zoom)
        
        # Translate kembali + camera offset
        camera_matrix.translate(-center_x + self.camera_x, -center_y + self.camera_y)
        
        # Draw grid dengan zoom consideration
        self._draw_grid_with_zoom(canvas_surface)
        
        # Draw axes dengan zoom consideration
        self._draw_axes_with_zoom(canvas_surface)
        
        # Draw all shapes dengan camera transform
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
            
            # Draw selection highlight dengan zoom consideration
            if is_selected:
                points = shape.get_points(transformed=True)
                if len(points) >= 2:
                    thickness = max(1, int(3 / self.camera_zoom))  # Thickness scales with zoom
                    for j in range(len(points)):
                        start = points[j]
                        end = points[(j + 1) % len(points)]
                        pygame.draw.line(canvas_surface, (255, 0, 0), start, end, thickness)
            
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
    
    def _draw_grid_with_zoom(self, surface):
        """Draw grid dengan zoom consideration"""
        # Grid spacing dalam world coordinates
        base_spacing = 50
        grid_color = self.grid_color
        
        # Buat camera matrix untuk transformasi
        camera_matrix = TransformationMatrix()
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        camera_matrix.translate(center_x, center_y)
        camera_matrix.scale(self.camera_zoom, self.camera_zoom)
        camera_matrix.translate(-center_x + self.camera_x, -center_y + self.camera_y)
        
        # Hitung visible range dalam world coordinates
        # Inverse transform untuk mendapatkan world coordinates dari screen corners
        screen_corners = [
            (0, 0),
            (self.canvas_width, 0),
            (self.canvas_width, self.canvas_height),
            (0, self.canvas_height)
        ]
        
        # Inverse camera transform
        inv_camera = TransformationMatrix()
        inv_camera.translate(center_x - self.camera_x, center_y - self.camera_y)
        inv_camera.scale(1.0 / self.camera_zoom, 1.0 / self.camera_zoom)
        inv_camera.translate(-center_x, -center_y)
        
        world_corners = [inv_camera.apply_to_point(x, y) for x, y in screen_corners]
        world_xs = [p[0] for p in world_corners]
        world_ys = [p[1] for p in world_corners]
        
        min_world_x = min(world_xs)
        max_world_x = max(world_xs)
        min_world_y = min(world_ys)
        max_world_y = max(world_ys)
        
        # Draw vertical lines
        start_x = int(min_world_x - base_spacing)
        end_x = int(max_world_x + base_spacing)
        for x in range(start_x, end_x, base_spacing):
            point1 = camera_matrix.apply_to_point(x, min_world_y - base_spacing)
            point2 = camera_matrix.apply_to_point(x, max_world_y + base_spacing)
            # Clip ke screen bounds
            if (0 <= point1[0] <= self.canvas_width or 0 <= point2[0] <= self.canvas_width or
                (point1[0] < 0 and point2[0] > self.canvas_width) or
                (point1[0] > self.canvas_width and point2[0] < 0)):
                pygame.draw.line(surface, grid_color, 
                               (int(point1[0]), int(point1[1])), 
                               (int(point2[0]), int(point2[1])), 1)
        
        # Draw horizontal lines
        start_y = int(min_world_y - base_spacing)
        end_y = int(max_world_y + base_spacing)
        for y in range(start_y, end_y, base_spacing):
            point1 = camera_matrix.apply_to_point(min_world_x - base_spacing, y)
            point2 = camera_matrix.apply_to_point(max_world_x + base_spacing, y)
            # Clip ke screen bounds
            if (0 <= point1[1] <= self.canvas_height or 0 <= point2[1] <= self.canvas_height or
                (point1[1] < 0 and point2[1] > self.canvas_height) or
                (point1[1] > self.canvas_height and point2[1] < 0)):
                pygame.draw.line(surface, grid_color, 
                               (int(point1[0]), int(point1[1])), 
                               (int(point2[0]), int(point2[1])), 1)
    
    def _draw_axes_with_zoom(self, surface):
        """Draw axes dengan zoom consideration"""
        # Create temporary axis dengan zoom transform
        camera_matrix = TransformationMatrix()
        center_x = self.canvas_width / 2
        center_y = self.canvas_height / 2
        camera_matrix.translate(center_x, center_y)
        camera_matrix.scale(self.camera_zoom, self.camera_zoom)
        camera_matrix.translate(-center_x + self.camera_x, -center_y + self.camera_y)
        
        # Transform origin
        origin_world_x = self.origin_x
        origin_world_y = self.origin_y
        origin_screen = camera_matrix.apply_to_point(origin_world_x, origin_world_y)
        origin_screen_x = int(origin_screen[0])
        origin_screen_y = int(origin_screen[1])
        
        # Draw axes jika masih dalam viewport
        axis_color = (100, 100, 100)
        
        # X-axis
        if 0 <= origin_screen_y <= self.canvas_height:
            # Transform points untuk axis
            point_start = camera_matrix.apply_to_point(-1000, origin_world_y)
            point_end = camera_matrix.apply_to_point(1000, origin_world_y)
            pygame.draw.line(surface, axis_color, 
                           (int(point_start[0]), int(point_start[1])), 
                           (int(point_end[0]), int(point_end[1])), 
                           max(1, int(2 / self.camera_zoom)))
            
            # Arrow head
            arrow_size = max(5, int(10 / self.camera_zoom))
            pygame.draw.polygon(surface, axis_color, [
                (int(point_end[0]), int(point_end[1])),
                (int(point_end[0]) - arrow_size, int(point_end[1]) - arrow_size // 2),
                (int(point_end[0]) - arrow_size, int(point_end[1]) + arrow_size // 2)
            ])
        
        # Y-axis
        if 0 <= origin_screen_x <= self.canvas_width:
            # Transform points untuk axis
            point_start = camera_matrix.apply_to_point(origin_world_x, -1000)
            point_end = camera_matrix.apply_to_point(origin_world_x, 1000)
            pygame.draw.line(surface, axis_color, 
                           (int(point_start[0]), int(point_start[1])), 
                           (int(point_end[0]), int(point_end[1])), 
                           max(1, int(2 / self.camera_zoom)))
            
            # Arrow head
            arrow_size = max(5, int(10 / self.camera_zoom))
            pygame.draw.polygon(surface, axis_color, [
                (int(point_start[0]), int(point_start[1])),
                (int(point_start[0]) - arrow_size // 2, int(point_start[1]) + arrow_size),
                (int(point_start[0]) + arrow_size // 2, int(point_start[1]) + arrow_size)
            ])
        
        # Label origin
        if 0 <= origin_screen_x <= self.canvas_width and 0 <= origin_screen_y <= self.canvas_height:
            font_size = max(12, int(24 / self.camera_zoom))
            font = pygame.font.Font(None, font_size)
            text = font.render("O", True, axis_color)
            surface.blit(text, (origin_screen_x + max(2, int(5 / self.camera_zoom)), 
                              origin_screen_y + max(2, int(5 / self.camera_zoom))))
    
    def _draw_info(self):
        """Draw info text di canvas"""
        font = pygame.font.Font(None, 24)
        
        info_lines = [
            "MatrixTransform2D - Transformasi Matriks 2D",
            f"Selected: Shape {self.selected_shape_index + 1}/{len(self.shapes)}",
            f"Zoom: {self.camera_zoom:.2f}x",
            "Controls:",
            "  TAB - Switch shape",
            "  R - Reset transform",
            "  Arrow Keys - Move camera",
            "  +/- or Mouse Wheel - Zoom in/out",
            "  0 - Reset zoom",
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
        print("  +/- or Mouse Wheel - Zoom in/out")
        print("  0 - Reset zoom")
        print("  PageUp/PageDown - Zoom in/out")
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
