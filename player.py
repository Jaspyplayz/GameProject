import pygame
from constants import PLAYER_SIZE, PLAYER_SPEED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        self.color = BLUE
        self.image = None
        self.health = 100
        self.score = 0
        self.target_position = None
        
    def set_image(self, image):
        """Set the player's image"""
        self.image = image
        
    def set_target(self, position):
        """Set a target position to move towards"""
        self.target_position = position
        
    def stop_movement(self):
        """Stop the player's movement"""
        self.target_position = None
        
    def update(self):
        """Update player position based on target position"""
        # If there's no target position, player doesn't move
        if not self.target_position:
            return
            
        # Calculate direction vector to target
        dx = self.target_position[0] - (self.x + self.size/2)
        dy = self.target_position[1] - (self.y + self.size/2)
        
        # Calculate distance to target
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        
        # If player is close enough to target, stop moving
        if distance < 5:  # Threshold for "close enough"
            self.target_position = None
            return
            
        # Normalize direction vector and apply speed
        if distance > 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
        
        # Update position
        self.x += dx
        self.y += dy
        
        # Keep player within screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
        
    def draw(self, screen):
        """Draw the player"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
            
        # Optionally draw a small indicator at the target position if moving
        if self.target_position:
            pygame.draw.circle(screen, (255, 255, 0), self.target_position, 3, 1)
            
    def get_rect(self):
        """Get the player's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)
        
    def take_damage(self, amount):
        """Reduce player health by specified amount"""
        self.health -= amount
        return self.health <= 0  # Return True if player died
        
    def add_score(self, points):
        """Add points to player's score"""
        self.score += points
    
    def stop_movement(self):
        """Stop the player's movement by clearing the target"""
        self.target_x = None
        self.target_y = None

