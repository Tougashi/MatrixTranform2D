"""
User interface dan kontrol aplikasi
Menggunakan Pygame untuk UI components
"""

import pygame
from typing import Optional, Callable
from .matrix import Transform2D


class Button:
    """Class untuk button di UI"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 color=(200, 200, 200), hover_color=(220, 220, 220),
                 text_color=(0, 0, 0), font_size=20, callback: Optional[Callable] = None):
        """
        Args:
            x, y: Posisi button
            width, height: Ukuran button
            text: Teks button
            color: Warna background normal
            hover_color: Warna background saat hover
            text_color: Warna teks
            font_size: Ukuran font
            callback: Function yang dipanggil saat button diklik
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.callback = callback
        self.is_hovered = False
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event
        Returns:
            True jika event handled, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw button ke surface"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)
        
        # Draw text centered
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Slider:
    """Class untuk slider di UI"""
    
    def __init__(self, x: int, y: int, width: int, min_val: float, max_val: float,
                 initial_val: float = 0.0, label: str = "", callback: Optional[Callable] = None):
        """
        Args:
            x, y: Posisi slider
            width: Lebar slider
            min_val: Nilai minimum
            max_val: Nilai maksimum
            initial_val: Nilai awal
            label: Label untuk slider
            callback: Function(val) yang dipanggil saat nilai berubah
        """
        self.rect = pygame.Rect(x, y, width, 20)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.callback = callback
        self.font = pygame.font.Font(None, 20)
        self.is_dragging = False
        self.knob_radius = 8
    
    def get_normalized_value(self) -> float:
        """Get value normalized ke 0-1"""
        if self.max_val == self.min_val:
            return 0.0
        return (self.value - self.min_val) / (self.max_val - self.min_val)
    
    def set_value_from_pos(self, pos_x: int):
        """Set value berdasarkan posisi mouse X"""
        relative_x = max(0, min(self.rect.width, pos_x - self.rect.x))
        normalized = relative_x / self.rect.width
        new_value = self.min_val + normalized * (self.max_val - self.min_val)
        self.set_value(new_value)
    
    def set_value(self, value: float, trigger_callback: bool = True):
        """Set value dan trigger callback jika diminta"""
        old_value = self.value
        self.value = max(self.min_val, min(self.max_val, value))
        if self.value != old_value and self.callback and trigger_callback:
            self.callback(self.value)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame event
        Returns:
            True jika event handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                knob_x = self.rect.x + self.get_normalized_value() * self.rect.width
                knob_rect = pygame.Rect(knob_x - self.knob_radius - 5,
                                       self.rect.y - 5,
                                       (self.knob_radius + 5) * 2,
                                       self.rect.height + 10)
                if knob_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                    self.is_dragging = True
                    self.set_value_from_pos(event.pos[0])
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                self.set_value_from_pos(event.pos[0])
                return True
        
        return False
    
    def draw(self, surface: pygame.Surface):
        """Draw slider ke surface"""
        # Draw track
        pygame.draw.rect(surface, (150, 150, 150), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 1)
        
        # Draw knob
        knob_x = self.rect.x + self.get_normalized_value() * self.rect.width
        knob_y = self.rect.centery
        pygame.draw.circle(surface, (50, 50, 50), (int(knob_x), knob_y), self.knob_radius)
        pygame.draw.circle(surface, (200, 200, 200), (int(knob_x), knob_y), self.knob_radius - 2)
        
        # Draw label and value
        if self.label:
            label_text = f"{self.label}: {self.value:.2f}"
            text_surface = self.font.render(label_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            # Draw label centered above the slider to avoid vertical overlap
            label_x = self.rect.x + (self.rect.width - text_rect.width) // 2
            label_y = self.rect.y - text_rect.height - 6
            # If there's no room above (rare inside small panels), clamp
            if label_y < 0:
                label_y = self.rect.y - text_rect.height
            surface.blit(text_surface, (label_x, label_y))


class TextLabel:
    """Class untuk text label di UI"""
    
    def __init__(self, x: int, y: int, text: str, font_size: int = 20,
                 color=(0, 0, 0), bg_color=None):
        """
        Args:
            x, y: Posisi label
            text: Teks label
            font_size: Ukuran font
            color: Warna teks
            bg_color: Warna background (None untuk transparent)
        """
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.bg_color = bg_color
    
    def set_text(self, text: str):
        """Update teks label"""
        self.text = text
    
    def draw(self, surface: pygame.Surface):
        """Draw label ke surface"""
        text_surface = self.font.render(self.text, True, self.color, self.bg_color)
        surface.blit(text_surface, (self.x, self.y))


class ControlPanel:
    """Panel kontrol untuk transformasi"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Args:
            x, y: Posisi panel
            width, height: Ukuran panel
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = (240, 240, 240)
        self.border_color = (150, 150, 150)
        
        # Transform control
        self.transform = Transform2D()
        
        # Sliders untuk transformasi
        # Increase top offset so sliders and their labels sit below the
        # "Transform Controls" title with better spacing.
        y_offset = 60
        slider_width = width - 40
        
        # Camera zoom control (added at the top)
        self.zoom_slider = Slider(
            x + 20, y + y_offset, slider_width, 0.1, 5.0, 1.0, "Camera Zoom",
            callback=lambda v: self._on_zoom_change()
        )
        
        # Offset for transform sliders (below zoom)
        y_offset += 60
        
        self.translate_x_slider = Slider(
            x + 20, y + y_offset, slider_width, -200, 200, 0, "Translate X",
            callback=lambda v: self._on_transform_change()
        )
        
        self.translate_y_slider = Slider(
            x + 20, y + y_offset + 50, slider_width, -200, 200, 0, "Translate Y",
            callback=lambda v: self._on_transform_change()
        )
        
        self.rotate_slider = Slider(
            x + 20, y + y_offset + 100, slider_width, -180, 180, 0, "Rotate (deg)",
            callback=lambda v: self._on_transform_change()
        )
        
        self.scale_x_slider = Slider(
            x + 20, y + y_offset + 150, slider_width, 0.1, 3.0, 1.0, "Scale X",
            callback=lambda v: self._on_transform_change()
        )
        
        self.scale_y_slider = Slider(
            x + 20, y + y_offset + 200, slider_width, 0.1, 3.0, 1.0, "Scale Y",
            callback=lambda v: self._on_transform_change()
        )
        
        # Buttons
        button_y = y + y_offset + 260
        # Arrange buttons vertically in this order:
        # 1) Reset Button
        # 2) Reset Camera
        # 3) Center
        button_width = slider_width

        self.reset_button = Button(
            x + 20, button_y, button_width, 30, "Reset Objek",
            callback=lambda: self.reset_transform()
        )

        self.reset_camera_button = Button(
            x + 20, button_y + 40, button_width, 30, "Reset Camera",
            callback=lambda: self.reset_camera()
        )

        self.reset_center_button = Button(
            x + 20, button_y + 80, button_width, 30, "Center",
            callback=lambda: self.reset_to_center()
        )
        
        # Labels
        self.title_label = TextLabel(x + 20, y + 10, "Transform Controls", 
                         font_size=24, color=(0, 0, 0))
        # Place matrix label below the stacked buttons (buttons take ~110px)
        self.matrix_label = TextLabel(x + 20, button_y + 120, "", 
                          font_size=16, color=(100, 100, 100))
        
        # Callback untuk perubahan transformasi
        self.on_transform_changed: Optional[Callable] = None
        self.on_zoom_changed: Optional[Callable] = None
        # Callback untuk mereset kamera pada level aplikasi
        self.on_camera_reset: Optional[Callable] = None
    
    def _on_transform_change(self):
        """Update transform parameters dari sliders"""
        self.transform.translation_x = self.translate_x_slider.value
        self.transform.translation_y = self.translate_y_slider.value
        self.transform.rotation_angle = self.rotate_slider.value
        self.transform.scale_x = self.scale_x_slider.value
        self.transform.scale_y = self.scale_y_slider.value
        
        # Simplified display (tidak perlu membuat matrix, hanya tampilkan nilai)
        matrix_str = f"TX: {self.transform.translation_x:.1f}, " \
                    f"TY: {self.transform.translation_y:.1f}, " \
                    f"R: {self.transform.rotation_angle:.1f}°, " \
                    f"SX: {self.transform.scale_x:.2f}, " \
                    f"SY: {self.transform.scale_y:.2f}"
        self.matrix_label.set_text(matrix_str)
        
        # Notify aplikasi bahwa transformasi berubah (untuk save)
        # Ini akan dipanggil setiap kali slider berubah
    
    def _on_zoom_change(self):
        """Update zoom dari slider"""
        zoom_value = self.zoom_slider.value
        if self.on_zoom_changed:
            self.on_zoom_changed(zoom_value)
    
    def set_zoom(self, zoom_value: float):
        """Set zoom slider value"""
        self.zoom_slider.set_value(zoom_value)
    
    def reset_transform(self):
        """Reset semua transformasi ke default"""
        self.transform.reset()
        self.translate_x_slider.set_value(0)
        self.translate_y_slider.set_value(0)
        self.rotate_slider.set_value(0)
        self.scale_x_slider.set_value(1.0)
        self.scale_y_slider.set_value(1.0)
    
    def reset_to_center(self):
        """Reset ke center (translasi saja yang di-reset)"""
        self.translate_x_slider.set_value(0)
        self.translate_y_slider.set_value(0)

    def reset_camera(self):
        """Reset camera-related controls (zoom) and notify app"""
        # Reset the zoom slider to default
        self.set_zoom(1.0)
        # Notify application if present
        if self.on_camera_reset:
            self.on_camera_reset()
    
    def get_transform_matrix(self, pivot_x=0, pivot_y=0):
        """Get transformation matrix saat ini dengan pivot point"""
        # Set pivot point untuk scale dan rotate
        self.transform.pivot_x = pivot_x
        self.transform.pivot_y = pivot_y
        return self.transform.get_matrix()
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame event untuk semua controls"""
        self.zoom_slider.handle_event(event)
        self.translate_x_slider.handle_event(event)
        self.translate_y_slider.handle_event(event)
        self.rotate_slider.handle_event(event)
        self.scale_x_slider.handle_event(event)
        self.scale_y_slider.handle_event(event)
        self.reset_button.handle_event(event)
        self.reset_center_button.handle_event(event)
        self.reset_camera_button.handle_event(event)
    
    def draw(self, surface: pygame.Surface):
        """Draw panel dan semua controls"""
        # Draw panel background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Draw title
        self.title_label.draw(surface)
        
        # Draw zoom slider (camera control)
        self.zoom_slider.draw(surface)
        
        # Draw transform sliders
        self.translate_x_slider.draw(surface)
        self.translate_y_slider.draw(surface)
        self.rotate_slider.draw(surface)
        self.scale_x_slider.draw(surface)
        self.scale_y_slider.draw(surface)
        
        # Draw buttons
        self.reset_button.draw(surface)
        self.reset_center_button.draw(surface)
        self.reset_camera_button.draw(surface)
        
        # Draw matrix label
        self.matrix_label.draw(surface)
