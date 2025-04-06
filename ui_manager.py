# ui_manager.py
import pygame
from constants import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT

class UIManager:
    def __init__(self, game):
        self.game = game
        
    def draw_playing_ui(self, screen):
        """Draw UI elements during gameplay"""
        # Draw health bar
        self._draw_health_bar(screen, 20, 20, self.game.player.health)
        
        # Draw score
        font = self.game.assets.get_font("main")
        score_text = f"Score: {self.game.player.score}"
        score_surf = font.render(score_text, True, WHITE)
        screen.blit(score_surf, (20, 60))
        
    def draw_menu_ui(self, screen):
        """Draw UI elements for the menu"""
        # Draw title
        font = self.game.assets.get_font("title")
        title_surf = font.render("SPACE SHOOTER", True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)
        
    def draw_paused_ui(self, screen):
        """Draw UI elements for the pause screen"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw pause text
        font = self.game.assets.get_font("title")
        pause_surf = font.render("PAUSED", True, WHITE)
        pause_rect = pause_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(pause_surf, pause_rect)
        
    def draw_game_over_ui(self, screen):
        """Draw UI elements for the game over screen"""
        # Draw game over text
        font = self.game.assets.get_font("title")
        game_over_surf = font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(game_over_surf, game_over_rect)
        
        # Draw final score
        font = self.game.assets.get_font("main")
        score_surf = font.render(f"Final Score: {self.game.player.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(score_surf, score_rect)
        
    def draw_victory_ui(self, screen):
        """Draw UI elements for the victory screen"""
        # Draw victory text
        font = self.game.assets.get_font("title")
        victory_surf = font.render("VICTORY!", True, WHITE)
        victory_rect = victory_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(victory_surf, victory_rect)
        
        # Draw final score
        font = self.game.assets.get_font("main")
        score_surf = font.render(f"Final Score: {self.game.player.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(score_surf, score_rect)
        
    def _draw_health_bar(self, screen, x, y, health):
        """Draw a health bar at the specified position"""
        bar_width = 200
        bar_height = 20
        fill_width = int((health / 100) * bar_width)
        
        # Draw background (empty health)
        pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_width, bar_height))
        
        # Draw filled health
        pygame.draw.rect(screen, (0, 200, 0), (x, y, fill_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
        
        # Draw text
        font = self.game.assets.get_font("small") if hasattr(self.game.assets, "get_font") else pygame.font.SysFont("Arial", 16)
        health_text = f"Health: {health}"
        health_surf = font.render(health_text, True, WHITE)
        health_rect = health_surf.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(health_surf, health_rect)
