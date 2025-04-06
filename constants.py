#Initialize Display
#Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "WASD Movement Game"

#Player initalization and frame of reference
PLAYER_SIZE = 50
PLAYER_SPEED = 5     

#Enemy settings
ENEMY_SIZE = 40
ENEMY_SPEED = 3

#Preset colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
BLACK = (0,0,0)

#Game States
STATE_MENU = "MENU"
STATE_PLAYING= "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"

#Asset paths
ASSET_DIR = "assets"
IMAGE_DIR = f"{ASSET_DIR}/images"
SOUND_DIR = f"{ASSET_DIR}/sounds"
FONT_DIR = f"{ASSET_DIR}/fonts"

#UI settings
MENU_BG_COLOR = (25, 25, 50)
MENU_TEXT_COLOR = WHITE
MENU_HIGHLIGHT_COLOR = (255, 255, 0)
BUTTON_NORMAL_COLOR = (100, 100, 200)
BUTTON_HOVER_COLOR = (150, 150, 255)
BUTTON_TEXT_COLOR = WHITE

# Add to constants.py
# Asset directories
IMAGE_DIR = "assets/images"
SOUND_DIR = "assets/sounds"
FONT_DIR = "assets/fonts"

# Enemy types
ENEMY_TYPES = ["basic", "fast", "tank"]
ENEMY_COLORS = {
    "basic": (255, 0, 0),      # Red
    "fast": (255, 165, 0),     # Orange
    "tank": (128, 0, 128)      # Purple
}
