"""
Floating debug log system
"""
import pygame
from typing import List, Tuple
import time

class LogMessage:
    """A single log message with timestamp"""
    def __init__(self, message: str, color: Tuple[int, int, int] = (255, 255, 255)):
        self.message = message
        self.color = color
        self.timestamp = time.time()
        self.lifetime = 5.0  # 5 seconds
    
    def is_expired(self) -> bool:
        """Check if message has expired"""
        return time.time() - self.timestamp > self.lifetime
    
    def get_alpha(self) -> int:
        """Get alpha value for fade-out effect"""
        elapsed = time.time() - self.timestamp
        if elapsed < self.lifetime - 1.0:
            return 255
        else:
            # Fade out in the last 1 second
            fade_time = elapsed - (self.lifetime - 1.0)
            alpha = int(255 * (1.0 - fade_time))
            return max(0, min(255, alpha))


class DebugLogger:
    """Floating debug log system that appears at the bottom of the screen"""
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.messages: List[LogMessage] = []
        self.font = pygame.font.Font(None, 20)
        self.max_messages = 5  # Maximum messages to display at once
        
        # Position settings
        self.padding = 10
        self.line_height = 25
        self.bottom_offset = 20  # Distance from bottom of screen
    
    def log(self, message: str, color: Tuple[int, int, int] = (255, 255, 255)):
        """Add a new log message"""
        # Remove expired messages
        self._cleanup_expired()
        
        # Add new message
        log_msg = LogMessage(message, color)
        self.messages.append(log_msg)
        
        # Keep only the most recent messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        
        # Also print to console for debugging
        print(f"[LOG] {message}")
    
    def _cleanup_expired(self):
        """Remove expired messages"""
        self.messages = [msg for msg in self.messages if not msg.is_expired()]
    
    def render(self, screen: pygame.Surface):
        """Render all active log messages"""
        # Remove expired messages
        self._cleanup_expired()
        
        if not self.messages:
            return
        
        # Render messages from bottom to top
        y_pos = self.screen_height - self.bottom_offset
        
        for msg in reversed(self.messages):
            # Create text surface
            text_surface = self.font.render(msg.message, True, msg.color)
            
            # Apply alpha for fade-out effect
            alpha = msg.get_alpha()
            text_surface.set_alpha(alpha)
            
            # Calculate position (centered horizontally)
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.screen_width // 2
            text_rect.bottom = y_pos
            
            # Draw semi-transparent background
            bg_padding = 5
            bg_rect = pygame.Rect(
                text_rect.x - bg_padding,
                text_rect.y - bg_padding,
                text_rect.width + bg_padding * 2,
                text_rect.height + bg_padding * 2
            )
            
            # Background with alpha
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_alpha = int(alpha * 0.7)  # 70% of text alpha
            pygame.draw.rect(bg_surface, (0, 0, 0, bg_alpha), bg_surface.get_rect(), border_radius=5)
            screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
            
            # Draw text
            screen.blit(text_surface, text_rect)
            
            # Move up for next message
            y_pos -= self.line_height
