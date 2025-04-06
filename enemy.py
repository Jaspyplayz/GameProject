import pygame
import random
import math
from constants import ENEMY_SIZE, ENEMY_SPEED, RED, SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy:
    def __init__(self, x, y, target=None):
        self.x = x
        self.y = y
        self.size = ENEMY_SIZE
        self.speed = ENEMY_SPEED
        self.color = RED
        self.image = None
        self.direction = random.uniform(0, 2 * math.pi)  # Random direction in radians
        self.avoid_force = 0.5  # How strongly enemies avoid each other
        self.detection_radius = ENEMY_SIZE * 2  # How far enemies detect each other
        self.target = target  # Store the target (player)
        self.chase_weight = 0.3  # How strongly to chase the target (0 = no chase, 1 = direct chase)
        
    def set_image(self, image):
        """Set the enemy's image"""
        self.image = image
        
    def update(self, enemies=None):
        """Update enemy position and handle collisions"""
        # Calculate movement based on direction
        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed
        
        # Apply target chasing behavior if target exists
        if self.target:
            chase_dx, chase_dy = self.calculate_chase_vector()
            dx = dx * (1 - self.chase_weight) + chase_dx * self.chase_weight
            dy = dy * (1 - self.chase_weight) + chase_dy * self.chase_weight
        
        # Apply avoidance behavior if enemies list is provided
        if enemies:
            avoid_x, avoid_y = self.calculate_avoidance(enemies)
            dx += avoid_x
            dy += avoid_y
            
            # Recalculate direction based on the new movement vector
            if dx != 0 or dy != 0:
                self.direction = math.atan2(dy, dx)
        
        # Update position
        self.x += dx
        self.y += dy
        
        # Bounce off screen edges
        if self.x <= 0 or self.x + self.size >= SCREEN_WIDTH:
            self.direction = math.pi - self.direction  # Reflect horizontally
            # Keep within bounds
            self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))
            
        if self.y <= 0 or self.y + self.size >= SCREEN_HEIGHT:
            self.direction = -self.direction  # Reflect vertically
            # Keep within bounds
            self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))
            
        # Occasionally change direction randomly
        if random.random() < 0.01:  # 1% chance each frame
            self.direction += random.uniform(-0.5, 0.5)
    
    def calculate_chase_vector(self):
        """Calculate vector to chase the target"""
        if not self.target:
            return 0, 0
            
        # Get target position (assuming target has x, y attributes)
        target_x = self.target.x + self.target.size/2
        target_y = self.target.y + self.target.size/2
        
        # Calculate direction to target
        dx = target_x - (self.x + self.size/2)
        dy = target_y - (self.y + self.size/2)
        
        # Normalize the vector
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
        return dx, dy
            
    def calculate_avoidance(self, enemies):
        """Calculate avoidance vector to prevent collisions with other enemies"""
        avoid_x, avoid_y = 0, 0
        
        for other in enemies:
            # Skip self
            if other is self:
                continue
                
            # Calculate distance between centers
            dx = (other.x + other.size/2) - (self.x + self.size/2)
            dy = (other.y + other.size/2) - (self.y + self.size/2)
            distance = math.sqrt(dx*dx + dy*dy)
            
            # If within detection radius, calculate avoidance force
            if distance < self.detection_radius:
                # Avoid with a force inversely proportional to distance
                if distance > 0:  # Avoid division by zero
                    force = self.avoid_force * (self.detection_radius - distance) / distance
                    avoid_x -= dx * force
                    avoid_y -= dy * force
                else:
                    # If exactly overlapping (shouldn't happen), move in random direction
                    angle = random.uniform(0, 2 * math.pi)
                    avoid_x -= math.cos(angle) * self.avoid_force
                    avoid_y -= math.sin(angle) * self.avoid_force
                    
        return avoid_x, avoid_y
        
    def draw(self, screen):
        """Draw the enemy"""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
            
        # Uncomment to visualize detection radius (for debugging)
        # pygame.draw.circle(screen, (255, 255, 255, 50), 
        #                   (int(self.x + self.size/2), int(self.y + self.size/2)), 
        #                   int(self.detection_radius), 1)
            
    def get_rect(self):
        """Get the enemy's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.size, self.size)
