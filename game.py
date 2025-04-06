# game.py
import pygame
import sys
from player import Player
from enemy import Enemy
from assets import AssetManager
from ui_manager import UIManager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, 
    STATE_GAME_OVER, STATE_VICTORY, PLAYER_SIZE
)
from game_state import MenuState, PlayingState, PausedState, GameOverState, VictoryState
from menu import Menu
from ui import Button

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = STATE_MENU
        
        #Initialize UI manager
        self.ui_manager = UIManager(self)
        

        #Previous state
        self.previous_state = None

        # Initialize asset manager
        self.assets = AssetManager()
        
        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * PLAYER_SIZE)
        self.player.set_image(self.assets.get_image("player"))
        
        # Create enemies list (will be populated in reset_game)
        self.enemies = []
        
        # Create menu
        self.menu = Menu(self)
        
        # Create pause menu buttons
        font = self.assets.get_font("main")
        self.pause_buttons = [
            Button(
                SCREEN_WIDTH // 2 - 100, 200, 200, 50,
                "Resume", font,
                action=lambda: self.set_state(STATE_PLAYING)
            ),
            Button(
                SCREEN_WIDTH // 2 - 100, 270, 200, 50,
                "Main Menu", font,
                action=lambda: self.set_state(STATE_MENU)
            ),
            Button(
                SCREEN_WIDTH // 2 - 100, 340, 200, 50,
                "Quit", font,
                action=lambda: self.quit_game()
            )
        ]
        
        # Create game states
        self.states = {
            STATE_MENU: MenuState(self),
            STATE_PLAYING: PlayingState(self),
            STATE_PAUSED: PausedState(self),
            STATE_GAME_OVER: GameOverState(self),
            STATE_VICTORY: VictoryState(self)
        }
        
        # Initialize the game
        self.reset_game()
        
    def reset_game(self):
        # Create player at center of screen
        self.player = Player(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, 
                            SCREEN_HEIGHT // 2 - PLAYER_SIZE // 2)
        
        # Set player image if available
        if "player" in self.assets.images:
            self.player.set_image(self.assets.get_image("player"))
        
        # Clear any previous enemies
        self.enemies = []
        
        # Create new enemies
        self.create_enemies(5)  # Create 5 enemies
        
        # Reset score or other game variables
        self.score = 0
        
    def create_enemies(self, count):
        """Create a specified number of enemies"""
        import random
        
        for _ in range(count):
            x = random.randint(0, SCREEN_WIDTH - PLAYER_SIZE)
            y = random.randint(0, SCREEN_HEIGHT // 2)
            enemy = Enemy(x, y, target=self.player)
            enemy.set_image(self.assets.get_image("enemy"))
            self.enemies.append(enemy)
        
    def set_state(self, state_name):
        """Change the current game state"""
        # Exit the current state

        self.previous_state = self.current_state

        self.states[self.current_state].exit()
        
        # Set the new state
        self.current_state = state_name
        
        # Enter the new state
        self.states[self.current_state].enter()
        
        # If changing to playing state, reset the game
        if state_name == STATE_PLAYING and self.previous_state != STATE_PAUSED:
            self.reset_game()
            
    def handle_events(self):
        """Process all game events"""
        events = pygame.event.get()
        self.states[self.current_state].handle_events(events)
        
    def update(self):
        """Update the current game state"""
        self.states[self.current_state].update()
        
    def draw(self):
        """Draw the current game state"""
        self.states[self.current_state].draw(self.screen)
        pygame.display.flip()
        
    def quit_game(self):
        """Exit the game"""
        self.running = False
        
    def run(self):
        """Main game loop"""
        while self.running:
            # Control frame rate
            self.clock.tick(FPS)
            
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
        
        # Clean up
        pygame.quit()
        sys.exit()
