"""
Pixel art editor for custom item sprites
"""
import pygame
from typing import List, Dict, Any, Optional, Tuple
import json
from item_types import ItemType

class PixelSprite:
    """Pixel art sprite data"""
    def __init__(self, width: int = 32, height: int = 32):
        self.width = width
        self.height = height
        # Grid of RGB colors (None = transparent)
        self.pixels: List[List[Optional[Tuple[int, int, int]]]] = [
            [None for _ in range(width)] for _ in range(height)
        ]
    
    def set_pixel(self, x: int, y: int, color: Optional[Tuple[int, int, int]]):
        """Set pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color
    
    def get_pixel(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None
    
    def clear(self):
        """Clear all pixels"""
        self.pixels = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def fill(self, color: Tuple[int, int, int]):
        """Fill with solid color"""
        self.pixels = [[color for _ in range(self.width)] for _ in range(self.height)]
    
    def copy(self) -> 'PixelSprite':
        """Create a deep copy of this sprite"""
        new_sprite = PixelSprite(self.width, self.height)
        new_sprite.pixels = [
            [pixel for pixel in row]
            for row in self.pixels
        ]
        return new_sprite
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON"""
        return {
            "width": self.width,
            "height": self.height,
            "pixels": [
                [list(pixel) if pixel else None for pixel in row]
                for row in self.pixels
            ]
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PixelSprite':
        """Create from dictionary"""
        sprite = PixelSprite(data["width"], data["height"])
        sprite.pixels = [
            [tuple(pixel) if pixel else None for pixel in row]
            for row in data["pixels"]
        ]
        return sprite
    
    def render_to_surface(self, size: int) -> pygame.Surface:
        """Render to pygame surface with precise pixel alignment"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pixel_size = size / self.width  # Use float for precise calculation
        
        for y in range(self.height):
            for x in range(self.width):
                color = self.pixels[y][x]
                if color:
                    # Calculate exact pixel boundaries
                    px = int(x * pixel_size)
                    py = int(y * pixel_size)
                    pw = int((x + 1) * pixel_size) - px
                    ph = int((y + 1) * pixel_size) - py
                    
                    rect = pygame.Rect(px, py, pw, ph)
                    pygame.draw.rect(surface, color, rect)
        
        return surface


class PixelSpriteLibrary:
    """Manage all custom sprites"""
    def __init__(self, filepath: str = "sprites.json"):
        self.filepath = filepath
        self.sprites: Dict[str, PixelSprite] = {}
        self.load()
    
    def get_sprite(self, item_type: ItemType) -> Optional[PixelSprite]:
        """Get sprite for item type"""
        return self.sprites.get(item_type.value)
    
    def set_sprite(self, item_type: ItemType, sprite: PixelSprite):
        """Set sprite for item type"""
        self.sprites[item_type.value] = sprite
    
    def save(self):
        """Save all sprites to JSON"""
        data = {
            key: sprite.to_dict()
            for key, sprite in self.sprites.items()
        }
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Sprites saved: {self.filepath}")
    
    def load(self):
        """Load sprites from JSON"""
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            
            self.sprites = {
                key: PixelSprite.from_dict(sprite_data)
                for key, sprite_data in data.items()
            }
            print(f"Sprites loaded: {self.filepath}")
        except FileNotFoundError:
            print("No sprite file found, starting fresh")
            self.sprites = {}
        except Exception as e:
            print(f"Failed to load sprites: {e}")
            self.sprites = {}


class PixelEditorPanel:
    """Pixel art editor UI"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Canvas settings
        self.canvas_size = min(width - 40, height - 200)
        self.canvas_x = x + (width - self.canvas_size) // 2
        self.canvas_y = y + 60
        
        self.grid_size = 32  # 32x32 pixel grid
        self.pixel_size = self.canvas_size // self.grid_size
        
        # Current sprite being edited
        self.current_sprite: Optional[PixelSprite] = None
        self.default_color: Optional[Tuple[int, int, int]] = None  # Store original default color
        
        # Undo/Redo system
        self.undo_stack: List[PixelSprite] = []
        self.redo_stack: List[PixelSprite] = []
        self.stroke_start_state: Optional[PixelSprite] = None  # State before current stroke
        
        # Color palette
        self.palette_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (255, 128, 0), (128, 0, 255), (0, 255, 128),
            (255, 255, 255), (128, 128, 128), (64, 64, 64),
            (0, 0, 0), (139, 69, 19), (34, 139, 34),
        ]
        self.selected_color: Tuple[int, int, int] = (255, 255, 255)
        self.eraser_mode = False
        
        # Palette position
        self.palette_y = self.canvas_y + self.canvas_size + 20
        self.palette_cell_size = 30
        
        # Drawing state
        self.is_drawing = False
        
        # Reset button rect (set in render)
        self.reset_button_rect: Optional[pygame.Rect] = None
    
    def set_sprite(self, sprite: PixelSprite, default_color: Optional[Tuple[int, int, int]] = None):
        """Set the sprite to edit"""
        self.current_sprite = sprite
        self.default_color = default_color
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.stroke_start_state = None
    
    def handle_mouse_down(self, pos: Tuple[int, int]):
        """Handle mouse down"""
        x, y = pos
        
        # Check reset button
        if self.reset_button_rect and self.reset_button_rect.collidepoint(x, y):
            return "reset"  # Signal to editor to handle reset
        
        # Check canvas
        if (self.canvas_x <= x < self.canvas_x + self.canvas_size and
            self.canvas_y <= y < self.canvas_y + self.canvas_size):
            # Save state before starting a new stroke
            if self.current_sprite:
                self.stroke_start_state = self.current_sprite.copy()
            self.is_drawing = True
            self.paint_pixel(pos)
        
        # Check palette
        elif self.palette_y <= y < self.palette_y + self.palette_cell_size:
            palette_x = self.x + 20
            for i, color in enumerate(self.palette_colors):
                cell_x = palette_x + i * (self.palette_cell_size + 5)
                if cell_x <= x < cell_x + self.palette_cell_size:
                    self.selected_color = color
                    self.eraser_mode = False
                    return
            
            # Eraser button (after colors)
            eraser_x = palette_x + len(self.palette_colors) * (self.palette_cell_size + 5)
            if eraser_x <= x < eraser_x + self.palette_cell_size:
                self.eraser_mode = True
    
    def handle_mouse_up(self, pos: Tuple[int, int]):
        """Handle mouse up - finalize stroke for undo/redo"""
        if self.is_drawing and self.stroke_start_state:
            # Push to undo stack
            self.undo_stack.append(self.stroke_start_state)
            # Clear redo stack when new action is made
            self.redo_stack.clear()
            self.stroke_start_state = None
        self.is_drawing = False
    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse motion"""
        if self.is_drawing:
            self.paint_pixel(pos)
    
    def paint_pixel(self, pos: Tuple[int, int]):
        """Paint pixel at mouse position"""
        if not self.current_sprite:
            return
        
        x, y = pos
        
        # Convert to grid coordinates
        grid_x = (x - self.canvas_x) // self.pixel_size
        grid_y = (y - self.canvas_y) // self.pixel_size
        
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            if self.eraser_mode:
                self.current_sprite.set_pixel(grid_x, grid_y, None)
            else:
                self.current_sprite.set_pixel(grid_x, grid_y, self.selected_color)
    
    def undo(self):
        """Undo last action"""
        if self.undo_stack and self.current_sprite:
            # Save current state to redo stack
            self.redo_stack.append(self.current_sprite.copy())
            # Restore previous state
            restored_state = self.undo_stack.pop()
            self.current_sprite.pixels = restored_state.pixels
            return True
        return False
    
    def redo(self):
        """Redo last undone action"""
        if self.redo_stack and self.current_sprite:
            # Save current state to undo stack
            self.undo_stack.append(self.current_sprite.copy())
            # Restore redo state
            restored_state = self.redo_stack.pop()
            self.current_sprite.pixels = restored_state.pixels
            return True
        return False
    
    def reset_to_default(self):
        """Reset sprite to default single color"""
        if self.current_sprite and self.default_color:
            # Save current state for undo
            self.undo_stack.append(self.current_sprite.copy())
            self.redo_stack.clear()
            # Fill with default color
            self.current_sprite.fill(self.default_color)
            return True
        return False
    
    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        """Render pixel editor panel"""
        # Background
        pygame.draw.rect(screen, (40, 40, 40), (self.x, self.y, self.width, self.height))
        
        # Title
        title = font.render("Pixel Editor", True, (255, 255, 255))
        screen.blit(title, (self.x + 10, self.y + 10))
        
        if not self.current_sprite:
            no_sprite = font.render("No sprite selected", True, (180, 180, 180))
            screen.blit(no_sprite, (self.x + 10, self.y + 50))
            return
        
        # Canvas background
        pygame.draw.rect(screen, (60, 60, 60), 
                        (self.canvas_x, self.canvas_y, self.canvas_size, self.canvas_size))
        
        # Draw pixels
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = self.current_sprite.get_pixel(x, y)
                if color:
                    rect = pygame.Rect(
                        self.canvas_x + x * self.pixel_size,
                        self.canvas_y + y * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size
                    )
                    pygame.draw.rect(screen, color, rect)
        
        # Grid lines
        for i in range(self.grid_size + 1):
            # Vertical
            x_pos = self.canvas_x + i * self.pixel_size
            pygame.draw.line(screen, (80, 80, 80),
                           (x_pos, self.canvas_y),
                           (x_pos, self.canvas_y + self.canvas_size), 1)
            # Horizontal
            y_pos = self.canvas_y + i * self.pixel_size
            pygame.draw.line(screen, (80, 80, 80),
                           (self.canvas_x, y_pos),
                           (self.canvas_x + self.canvas_size, y_pos), 1)
        
        # Color palette
        palette_x = self.x + 20
        for i, color in enumerate(self.palette_colors):
            cell_x = palette_x + i * (self.palette_cell_size + 5)
            
            # Highlight if selected
            border_color = (255, 255, 0) if (color == self.selected_color and not self.eraser_mode) else (150, 150, 150)
            border_width = 3 if (color == self.selected_color and not self.eraser_mode) else 1
            
            pygame.draw.rect(screen, color, 
                           (cell_x, self.palette_y, self.palette_cell_size, self.palette_cell_size))
            pygame.draw.rect(screen, border_color,
                           (cell_x, self.palette_y, self.palette_cell_size, self.palette_cell_size), border_width)
        
        # Eraser button
        eraser_x = palette_x + len(self.palette_colors) * (self.palette_cell_size + 5)
        eraser_color = (80, 80, 80)
        border_color = (255, 255, 0) if self.eraser_mode else (150, 150, 150)
        border_width = 3 if self.eraser_mode else 1
        
        pygame.draw.rect(screen, eraser_color,
                       (eraser_x, self.palette_y, self.palette_cell_size, self.palette_cell_size))
        pygame.draw.rect(screen, border_color,
                       (eraser_x, self.palette_y, self.palette_cell_size, self.palette_cell_size), border_width)
        
        # Eraser X
        pygame.draw.line(screen, (255, 255, 255),
                       (eraser_x + 5, self.palette_y + 5),
                       (eraser_x + self.palette_cell_size - 5, self.palette_y + self.palette_cell_size - 5), 2)
        pygame.draw.line(screen, (255, 255, 255),
                       (eraser_x + self.palette_cell_size - 5, self.palette_y + 5),
                       (eraser_x + 5, self.palette_y + self.palette_cell_size - 5), 2)
        
        # Reset button (below palette)
        reset_button_y = self.palette_y + self.palette_cell_size + 15
        reset_button_width = 120
        reset_button_height = 30
        reset_button_x = self.x + (self.width - reset_button_width) // 2
        
        pygame.draw.rect(screen, (150, 50, 50), 
                        (reset_button_x, reset_button_y, reset_button_width, reset_button_height))
        pygame.draw.rect(screen, (200, 200, 200), 
                        (reset_button_x, reset_button_y, reset_button_width, reset_button_height), 2)
        
        reset_text = font.render("Reset", True, (255, 255, 255))
        reset_rect = reset_text.get_rect(center=(reset_button_x + reset_button_width // 2, 
                                                   reset_button_y + reset_button_height // 2))
        screen.blit(reset_text, reset_rect)
        
        # Store reset button position for click detection
        self.reset_button_rect = pygame.Rect(reset_button_x, reset_button_y, 
                                             reset_button_width, reset_button_height)
        
        # Instructions and shortcuts
        instructions = [
            "Left click/drag: Paint",
            "Ctrl+Z: Undo | Shift+Ctrl+Z: Redo",
        ]
        inst_y = reset_button_y + reset_button_height + 15
        small_font = pygame.font.Font(None, 18)
        for inst in instructions:
            text = small_font.render(inst, True, (200, 200, 200))
            screen.blit(text, (self.x + 20, inst_y))
            inst_y += 20
