# assets.py
import pygame
import os
from constants import IMAGE_DIR, SOUND_DIR, FONT_DIR

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        
        # Create asset directories if they don't exist
        os.makedirs(IMAGE_DIR, exist_ok=True)
        os.makedirs(SOUND_DIR, exist_ok=True)
        os.makedirs(FONT_DIR, exist_ok=True)
        
        self._load_default_assets()
    
    # Fixed indentation - this should be at the class level, not nested in __init__    
    def _load_default_assets(self):
        """Load essential game assets on initialization"""
        # Create placeholder images if files don't exist
        self._ensure_image("player", (50, 50), (0, 0, 255))  # Blue player
        self._ensure_image("background", (800, 600), (50, 50, 50))  # Dark gray background
        self._ensure_image("menu_bg", (800, 600), (25, 25, 50))    # Dark blue menu background
        
        # Load enemy assets
        self.load_enemy_assets()
        
        # Load default system font instead of custom fonts
        self.fonts["main"] = pygame.font.SysFont("Arial", 36)
        self.fonts["title"] = pygame.font.SysFont("Arial", 72)
        self.fonts["small"] = pygame.font.SysFont("Arial", 24)
        
        # Create empty sounds (will be silent)
        self.sounds["click"] = None
        self.sounds["game_over"] = None

    def _ensure_image(self, name, size, color):
        """Create a placeholder image if the file doesn't exist"""
        file_path = os.path.join(IMAGE_DIR, f"{name}.png")
        try:
            # Try to load the image if it exists
            if os.path.exists(file_path):
                self.images[name] = pygame.image.load(file_path).convert_alpha()
            else:
                # Create a placeholder image
                surf = pygame.Surface(size)
                surf.fill(color)
                
                # Add some visual indication that this is a placeholder
                if size[0] > 20 and size[1] > 20:
                    pygame.draw.rect(surf, (255, 255, 255), 
                                    (5, 5, size[0]-10, size[1]-10), 2)
                    
                    # Add text if the image is large enough
                    if size[0] >= 80 and size[1] >= 20:
                        font = pygame.font.SysFont("Arial", min(24, size[1]//2))
                        text = font.render(name, True, (255, 255, 255))
                        text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
                        surf.blit(text, text_rect)
                
                self.images[name] = surf
                print(f"Created placeholder for missing image: {name}")
        except Exception as e:
            print(f"Error loading image {name}: {e}")
            # Create a simple colored rectangle as fallback
            surf = pygame.Surface(size)
            surf.fill((255, 0, 255))  # Magenta for errors
            self.images[name] = surf
            
    def load_image(self, name, path):
        """Load an image and store it with the given name"""
        try:
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                self.images[name] = image
                return image
            else:
                print(f"Image file not found: {path}")
                # Create a placeholder
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((255, 0, 255))  # Magenta for missing textures
                self.images[name] = placeholder
                return placeholder
        except pygame.error as e:
            print(f"Failed to load image {path}: {e}")
            # Create a placeholder
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            self.images[name] = placeholder
            return placeholder
            
    def get_image(self, name):
        """Get a loaded image by name"""
        if name in self.images:
            return self.images[name]
        else:
            print(f"Warning: Image '{name}' not found")
            # Return a placeholder
            placeholder = pygame.Surface((100, 100))
            placeholder.fill((255, 0, 255))  # Magenta for missing textures
            return placeholder
            
    def load_sound(self, name, path):
        """Load a sound and store it with the given name"""
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                self.sounds[name] = sound
                return sound
            else:
                print(f"Sound file not found: {path}")
                return None
        except pygame.error as e:
            print(f"Failed to load sound {path}: {e}")
            return None
            
    def get_sound(self, name):
        """Get a loaded sound by name"""
        if name in self.sounds:
            return self.sounds[name]
        else:
            print(f"Warning: Sound '{name}' not found")
            return None
            
    def play_sound(self, name):
        """Play a sound by name"""
        sound = self.get_sound(name)
        if sound:
            sound.play()
            
    def load_font(self, name, path, size):
        """Load a font and store it with the given name"""
        try:
            if os.path.exists(path):
                font = pygame.font.Font(path, size)
            else:
                print(f"Font file not found: {path}, using system font")
                font = pygame.font.SysFont("Arial", size)
            self.fonts[name] = font
            return font
        except pygame.error as e:
            print(f"Failed to load font {path}: {e}")
            # Use system font as fallback
            font = pygame.font.SysFont("Arial", size)
            self.fonts[name] = font
            return font
            
    def get_font(self, name):
        """Get a loaded font by name"""
        if name in self.fonts:
            return self.fonts[name]
        else:
            print(f"Warning: Font '{name}' not found, using default")
            # Return a default font
            return pygame.font.SysFont("Arial", 36)
        
    def load_enemy_assets(self):
        """Load assets for different enemy types"""
        from constants import ENEMY_TYPES, ENEMY_COLORS
        
        for enemy_type in ENEMY_TYPES:
            # Generate name like "enemy_basic", "enemy_fast", etc.
            name = f"enemy_{enemy_type}"
            file_path = os.path.join(IMAGE_DIR, f"{name}.png")
            
            # Check if custom enemy image exists
            if os.path.exists(file_path):
                self.load_image(name, file_path)
            else:
                # Create placeholder with appropriate color
                color = ENEMY_COLORS.get(enemy_type, (255, 0, 0))  # Default to red
                size = (40, 40)
                
                # Create a more distinctive enemy shape based on type
                surf = pygame.Surface(size, pygame.SRCALPHA)
                
                if enemy_type == "basic":
                    # Basic enemy: filled circle
                    pygame.draw.circle(surf, color, (size[0]//2, size[1]//2), size[0]//2)
                elif enemy_type == "fast":
                    # Fast enemy: triangle
                    points = [(size[0]//2, 0), (size[0], size[1]), (0, size[1])]
                    pygame.draw.polygon(surf, color, points)
                elif enemy_type == "tank":
                    # Tank enemy: square with details
                    pygame.draw.rect(surf, color, (0, 0, size[0], size[1]))
                    pygame.draw.rect(surf, (0, 0, 0), (size[0]//4, size[1]//4, 
                                                    size[0]//2, size[1]//2))
                else:
                    # Default: diamond shape
                    points = [(size[0]//2, 0), (size[0], size[1]//2), 
                            (size[0]//2, size[1]), (0, size[1]//2)]
                    pygame.draw.polygon(surf, color, points)
                
                # Add outline
                if enemy_type == "basic":
                    pygame.draw.circle(surf, (255, 255, 255), 
                                    (size[0]//2, size[1]//2), size[0]//2, 2)
                elif enemy_type == "fast":
                    pygame.draw.polygon(surf, (255, 255, 255), points, 2)
                elif enemy_type == "tank":
                    pygame.draw.rect(surf, (255, 255, 255), (0, 0, size[0], size[1]), 2)
                else:
                    pygame.draw.polygon(surf, (255, 255, 255), points, 2)
                
                self.images[name] = surf
                print(f"Created placeholder for enemy type: {enemy_type}")
