# game.py
import pygame
import random
import math
import sys
from player import Player
from enemy import Enemy
from assets import AssetManager
from ui_manager import UIManager
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, 
    STATE_GAME_OVER, STATE_VICTORY, PLAYER_SIZE, ENEMY_SIZE,
    ENEMY_TYPES, ENEMY_COLORS
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
        
        # Initialize UI manager
        self.ui_manager = UIManager(self)
        
        # Initizalize projectiles

        self.projectiles = []

        # Previous state
        self.previous_state = None

        # Initialize asset manager
        self.assets = AssetManager()
        
        # Create player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * PLAYER_SIZE)
        self.player.set_image(self.assets.get_image("player"))
        
        # Create enemies list (will be populated in reset_game)
        self.enemies = []
        
        # Particles for visual effects
        self.particles = []
        
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
        
        # Clear any previous enemies and particles
        self.enemies = []
        self.particles = []
        
        # Create new enemies
        self.create_enemies(5)  # Create 5 enemies
        
        # Reset score or other game variables
        self.score = 0

        # Reset projectiles
        self.projectiles = [] 
        
    def create_enemies(self, num_enemies):
        """Create a specified number of enemies with different types"""
        self.enemies = []
        
        # Define type distribution (can be adjusted for difficulty)
        type_weights = {
            "basic": 0.6,  # 60% chance for basic enemies
            "fast": 0.25,  # 25% chance for fast enemies
            "tank": 0.15   # 15% chance for tank enemies
        }
        
        # Define minimum safe distance from player
        min_safe_distance = 150  # Pixels
        
        for _ in range(num_enemies):
            # Choose enemy type based on weights
            enemy_type = random.choices(
                ENEMY_TYPES, 
                weights=[type_weights[t] for t in ENEMY_TYPES],
                k=1
            )[0]
            
            # Keep trying positions until we find one that's far enough from the player
            valid_position = False
            attempts = 0
            max_attempts = 100  # Prevent infinite loop
            
            while not valid_position and attempts < max_attempts:
                # Generate random position
                x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
                y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
                
                # Calculate distance to player
                player_center_x = self.player.x + self.player.size / 2
                player_center_y = self.player.y + self.player.size / 2
                enemy_center_x = x + ENEMY_SIZE / 2
                enemy_center_y = y + ENEMY_SIZE / 2
                
                dx = player_center_x - enemy_center_x
                dy = player_center_y - enemy_center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Check if position is valid (far enough from player)
                if distance >= min_safe_distance:
                    valid_position = True
                
                attempts += 1
            
            # Create enemy at the found position (or a fallback if no valid position found)
            if valid_position:
                enemy = Enemy(x, y, target=self.player, enemy_type=enemy_type)
            else:
                # Fallback: place at corner furthest from player
                corners = [
                    (0, 0),  # Top-left
                    (SCREEN_WIDTH - ENEMY_SIZE, 0),  # Top-right
                    (0, SCREEN_HEIGHT - ENEMY_SIZE),  # Bottom-left
                    (SCREEN_WIDTH - ENEMY_SIZE, SCREEN_HEIGHT - ENEMY_SIZE)  # Bottom-right
                ]
                
                # Find the corner furthest from the player
                furthest_corner = max(corners, key=lambda corner: 
                    math.sqrt((corner[0] - self.player.x)**2 + (corner[1] - self.player.y)**2))
                
                enemy = Enemy(furthest_corner[0], furthest_corner[1], target=self.player, enemy_type=enemy_type)
            
            # Set enemy image based on type
            image_name = f"enemy_{enemy_type}"
            if hasattr(self, 'assets') and image_name in self.assets.images:
                enemy.set_image(self.assets.get_image(image_name))
            elif hasattr(self, 'assets') and "enemy" in self.assets.images:
                # Fallback to generic enemy image
                enemy.set_image(self.assets.get_image("enemy"))
            
            self.enemies.append(enemy)
            
    def create_death_effect(self, x, y, color):
        """Create particle effect when an enemy is defeated"""
        num_particles = 20
        particles = []
        
        for _ in range(num_particles):
            speed = random.uniform(1, 3)
            angle = random.uniform(0, 2 * math.pi)
            size = random.randint(2, 6)
            lifetime = random.uniform(0.5, 1.5)  # seconds
            
            particle = {
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'lifetime': lifetime,
                'time_left': lifetime
            }
            particles.append(particle)
        
        self.particles.extend(particles)

    def update_particles(self, delta_time=1/60):
        """Update particle effects"""
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Update lifetime
            particle['time_left'] -= delta_time
            
            # Remove expired particles
            if particle['time_left'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen):
        """Draw particle effects"""
        for particle in self.particles:
            # Calculate fade based on remaining lifetime
            alpha = int(255 * (particle['time_left'] / particle['lifetime']))
            color = list(particle['color'])
            
            # Draw particle
            size = particle['size'] * (particle['time_left'] / particle['lifetime'])
            
            # Create a surface for the particle with alpha
            surf = pygame.Surface((int(size*2), int(size*2)), pygame.SRCALPHA)
            
            # Draw the particle on the surface
            pygame.draw.circle(
                surf, 
                (*color[:3], alpha),  # RGB + alpha
                (int(size), int(size)), 
                int(size)
            )
            
            # Blit the surface to the screen
            screen.blit(surf, (int(particle['x'] - size), int(particle['y'] - size)))
            
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
        
        # Update particles regardless of game state
        delta_time = 1 / FPS
        self.update_particles(delta_time)
        
    def draw(self):
        """Draw the current game state"""
        self.states[self.current_state].draw(self.screen)
        
        # Draw particles on top of everything
        self.draw_particles(self.screen)
        
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
