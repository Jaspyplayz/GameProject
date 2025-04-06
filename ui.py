# ui.py
import pygame
from constants import (
    BUTTON_NORMAL_COLOR, BUTTON_HOVER_COLOR, 
    BUTTON_TEXT_COLOR, WHITE
)

class Button:
    def __init__(self, x, y, width, height, text, font, 
                 normal_color=BUTTON_NORMAL_COLOR,
                 hover_color=BUTTON_HOVER_COLOR,
                 text_color=BUTTON_TEXT_COLOR,
                 action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False
        
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, screen):
        """Draw the button on the screen"""
        color = self.hover_color if self.is_hovered else self.normal_color
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw button border
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        """Handle mouse click events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered and self.action:
                return self.action()
        return None

class TextBox:
    def __init__(self, x, y, text, font, color=WHITE):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        
    def draw(self, screen):
        """Draw the text on the screen"""
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        screen.blit(text_surf, text_rect)
        
    def update_text(self, new_text):
        """Update the text content"""
        self.text = new_text
