import pygame
import math

class Projectile:
    def __init__(self, x, y, target_x, target_y, speed=10, damage=10, size=5, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.speed = speed
        
        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        distance = max(1, math.sqrt(dx * dx + dy * dy))  # Avoid division by zero
        
        # Normalize direction vector and multiply by speed
        self.dx = (dx / distance) * speed
        self.dy = (dy / distance) * speed
        
        # Create a rect for collision detection
        self.rect = pygame.Rect(x - size/2, y - size/2, size, size)
        
        # Track lifetime to remove old projectiles
        self.lifetime = 120  # frames (2 seconds at 60 FPS)
        
    def update(self):
        # Move the projectile
        self.x += self.dx
        self.y += self.dy
        
        # Update the collision rectangle
        self.rect.x = self.x - self.size/2
        self.rect.y = self.y - self.size/2
        
        # Reduce lifetime
        self.lifetime -= 1
        
        # Return True if the projectile should be removed
        return self.lifetime <= 0
        
    def draw(self, screen):
        # Draw the projectile as a small circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
