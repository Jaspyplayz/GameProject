# menu.py
import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MENU_BG_COLOR, 
    MENU_TEXT_COLOR, MENU_HIGHLIGHT_COLOR, STATE_PLAYING
)
from ui import Button, TextBox

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.texts = []
        self._create_menu_elements()
        
    def _create_menu_elements(self):
        """Create buttons and text elements for the menu"""
        center_x = SCREEN_WIDTH // 2
        
        # Create title
        title_font = self.game.assets.get_font("title")
        self.texts.append(TextBox(
            center_x, 100, "YOUR GAME", title_font, MENU_TEXT_COLOR
        ))
        
        # Create buttons
        button_font = self.game.assets.get_font("main")
        button_width, button_height = 200, 50
        button_x = center_x - button_width // 2
        
        # Start button
        self.buttons.append(Button(
            button_x, 250, button_width, button_height,
            "Start Game", button_font,
            action=lambda: self.game.set_state(STATE_PLAYING)
        ))
        
        # Options button
        self.buttons.append(Button(
            button_x, 320, button_width, button_height,
            "Options", button_font,
            action=self.show_options
        ))
        
        # Credits button
        self.buttons.append(Button(
            button_x, 390, button_width, button_height,
            "Credits", button_font,
            action=self.show_credits
        ))
        
        # Quit button
        self.buttons.append(Button(
            button_x, 460, button_width, button_height,
            "Quit", button_font,
            action=self.quit_game
        ))
        
    def update(self, mouse_pos):
        """Update all menu elements"""
        for button in self.buttons:
            button.update(mouse_pos)
            
    def draw(self, screen):
        """Draw the menu"""
        # Draw background
        screen.fill(MENU_BG_COLOR)
        
        # Optional: Draw background image
        bg_image = self.game.assets.get_image("menu_bg")
        screen.blit(bg_image, (0, 0))
        
        # Draw text elements
        for text in self.texts:
            text.draw(screen)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
            
    def handle_events(self, event):
        """Handle menu input events"""
        for button in self.buttons:
            result = button.handle_event(event)
            if result:  # If button action returned something
                return result
        return None
        
    def show_options(self):
        """Show options menu"""
        print("Options menu would appear")
        # You would implement this with another menu state
        
    def show_credits(self):
        """Show credits screen"""
        print("Credits would appear")
        # You would implement this with another menu state
        
    def quit_game(self):
        """Exit the game"""
        self.game.running = False
