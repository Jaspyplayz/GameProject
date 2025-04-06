# game_state.py
import pygame
from constants import (
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, 
    STATE_GAME_OVER, STATE_VICTORY,
    SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_COLORS
)

class GameState:
    def __init__(self, game):
        self.game = game
        
    def handle_events(self, events):
        """Handle events for this state"""
        pass
        
    def update(self):
        """Update game elements for this state"""
        pass
        
    def draw(self, screen):
        """Draw the state to the screen"""
        pass
        
    def enter(self):
        """Called when entering this state"""
        pass
        
    def exit(self):
        """Called when exiting this state"""
        pass

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            
            # Let the menu handle its own events
            self.game.menu.handle_events(event)
        
    def update(self):
        # Use scaled mouse position instead of raw position
        raw_mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_pos = self.game.scale_mouse_pos(raw_mouse_pos)
        self.game.menu.update(scaled_mouse_pos)
        
    def draw(self, screen):
        self.game.menu.draw(screen)
        
    def enter(self):
        # Reset menu selection or do other initialization
        if hasattr(self.game.assets, 'play_sound') and "menu_music" in self.game.assets.sounds:
            self.game.assets.play_sound("menu_music")
        
    def exit(self):
        # Clean up any menu-specific resources
        pass

class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.click_indicators = []
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_state(STATE_PAUSED)
                elif event.key == pygame.K_q:  # Q key for shooting
                    # Get scaled mouse position as the target
                    raw_mouse_pos = pygame.mouse.get_pos()
                    mouse_pos = self.game.scale_mouse_pos(raw_mouse_pos)
                    self.create_click_indicator(mouse_pos)
                    
                    # Check if player has shooting capability
                    if hasattr(self.game.player, 'shoot') and self.game.player.can_shoot():
                        # Create projectile
                        projectile = self.game.player.shoot(mouse_pos)
                        if projectile:  # Make sure a valid projectile was returned
                            if not hasattr(self.game, 'projectiles'):
                                self.game.projectiles = []
                            self.game.projectiles.append(projectile)
                            # Play sound effect if available
                            if hasattr(self.game.assets, 'play_sound') and "shoot" in self.game.assets.sounds:
                                self.game.assets.play_sound("shoot")
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button for shooting
                    self.create_click_indicator(event.pos)
                    # Check if player has shooting capability
                    if hasattr(self.game.player, 'shoot'):
                        # Create projectile
                        projectile = self.game.player.shoot(event.pos)
                        if projectile:  # Make sure a valid projectile was returned
                            if not hasattr(self.game, 'projectiles'):
                                self.game.projectiles = []
                            self.game.projectiles.append(projectile)
                            # Play sound effect if available
                            if hasattr(self.game.assets, 'play_sound') and "shoot" in self.game.assets.sounds:
                                self.game.assets.play_sound("shoot")
                    else:
                        # Fallback to attack if shoot method doesn't exist
                        if hasattr(self.game.player, 'attack'):
                            self.game.player.attack()
                elif event.button == 3:  # Right mouse button for movement
                    self.create_click_indicator(event.pos)
                    # Set player target position for movement
                    if hasattr(self.game.player, 'set_target'):
                        self.game.player.set_target(event.pos)

                    
    def update(self):
        # Update player movement
        self.game.player.update()
        
        # Keep player within screen bounds
        self.game.player.x = max(0, min(self.game.player.x, self.game.design_width - self.game.player.size))
        self.game.player.y = max(0, min(self.game.player.y, self.game.design_height - self.game.player.size))
        
        # Update projectiles if they exist
        if hasattr(self.game, 'projectiles'):
            for projectile in self.game.projectiles[:]:  # Use a copy for safe iteration
                # Update projectile position
                if projectile.update():
                    # Remove if lifetime expired
                    self.game.projectiles.remove(projectile)
                    continue
                    
                # Check for projectile going off-screen
                if (projectile.x < 0 or projectile.x > self.game.design_width or 
                    projectile.y < 0 or projectile.y > self.game.design_height):
                    self.game.projectiles.remove(projectile)
                    continue
                    
                # Check for collision with enemies
                for enemy in self.game.enemies[:]:
                    if enemy.get_rect().colliderect(projectile.rect):
                        # Enemy hit by projectile
                        if enemy.take_damage(projectile.damage):
                            # Enemy defeated
                            enemy_color = ENEMY_COLORS.get(enemy.enemy_type, (255, 0, 0))
                            self.game.create_death_effect(
                                enemy.x + enemy.size/2,
                                enemy.y + enemy.size/2,
                                enemy_color
                            )
                            self.game.enemies.remove(enemy)
                            self.game.score += 10  # Basic score for defeating enemy
                            
                            # Add bonus score based on enemy type
                            if enemy.enemy_type == "fast":
                                self.game.score += 5
                            elif enemy.enemy_type == "tank":
                                self.game.score += 10
                        
                        # Remove the projectile after hitting
                        if projectile in self.game.projectiles:
                            self.game.projectiles.remove(projectile)
                        break
        
        # Update enemies
        for enemy in self.game.enemies[:]:  # Use a copy of the list for safe iteration
            enemy.update(self.game.enemies)
            
            # Check for collision with player
            if self.game.player.get_rect().colliderect(enemy.get_rect()):
                # Player hit by enemy
                self.game.player.take_damage(enemy.damage)  # Use enemy's damage value
                
                # Check if player is defeated
                if self.game.player.health <= 0:
                    self.game.set_state(STATE_GAME_OVER)
                    
            # Check for player attack hitting enemy
            if self.game.player.is_attacking:
                attack_rect = self.game.player.get_attack_rect()
                if attack_rect and attack_rect.colliderect(enemy.get_rect()):
                    # Enemy hit by player attack
                    if enemy.take_damage(self.game.player.damage):
                        # Enemy defeated
                        enemy_color = ENEMY_COLORS.get(enemy.enemy_type, (255, 0, 0))
                        self.game.create_death_effect(
                            enemy.x + enemy.size/2,
                            enemy.y + enemy.size/2,
                            enemy_color
                        )
                        self.game.enemies.remove(enemy)
                        self.game.score += 10  # Basic score for defeating enemy
                        
                        # Add bonus score based on enemy type
                        if enemy.enemy_type == "fast":
                            self.game.score += 5  # Fast enemies worth more
                        elif enemy.enemy_type == "tank":
                            self.game.score += 10  # Tank enemies worth even more
        
        # Update click indicators
        self.update_click_indicators()
            
        # Check for victory condition (all enemies defeated)
        if len(self.game.enemies) == 0:
            self.game.set_state(STATE_VICTORY)
            
    def create_click_indicator(self, position):
        # Create a temporary visual effect at the clicked position
        indicator = {
            'position': position,
            'radius': 20,
            'alpha': 255,  # Start fully visible
            'color': (0, 255, 0)  # Green circle
        }
        self.click_indicators.append(indicator)
        
    def update_click_indicators(self):
        # Update all click indicators
        for indicator in self.click_indicators[:]:
            indicator['radius'] += 0.5
            indicator['alpha'] -= 10
            
            if indicator['alpha'] <= 0:
                self.click_indicators.remove(indicator)
        
    def draw(self, screen):
        # Draw background
        if hasattr(self.game.assets, 'get_image') and "background" in self.game.assets.images:
            screen.blit(self.game.assets.get_image("background"), (0, 0))
        else:
            screen.fill((0, 0, 0))  # Fallback to black background
        
        # Draw click indicators
        self.draw_click_indicators(screen)
        
        # Draw projectiles if they exist
        if hasattr(self.game, 'projectiles'):
            for projectile in self.game.projectiles:
                projectile.draw(screen)
        
        # Draw player
        self.game.player.draw(screen)
        
        # Draw enemies
        for enemy in self.game.enemies:
            enemy.draw(screen)
        
        # Draw UI elements
        if hasattr(self.game, 'ui_manager'):
            self.game.ui_manager.draw_playing_ui(screen)
        else:
            # Fallback UI if ui_manager not available
            font = self.game.assets.get_font("small")
            score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))
            health_text = font.render(f"Health: {self.game.player.health}", True, (255, 255, 255))
            
            screen.blit(score_text, (10, 10))
            screen.blit(health_text, (10, 40))
        
    def draw_click_indicators(self, screen):
        for indicator in self.click_indicators:
            s = pygame.Surface((indicator['radius'] * 2, indicator['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*indicator['color'], indicator['alpha']), 
                              (indicator['radius'], indicator['radius']), indicator['radius'], 2)
            screen.blit(s, (indicator['position'][0] - indicator['radius'], 
                           indicator['position'][1] - indicator['radius']))

    def enter(self):
        # Reset the player's target position when entering the playing state
        if hasattr(self.game.player, 'target_x'):
            self.game.player.target_x = None
            self.game.player.target_y = None
        
        # Clear any click indicators
        self.click_indicators = []
        
        # Initialize projectiles list if it doesn't exist
        if not hasattr(self.game, 'projectiles'):
            self.game.projectiles = []
        
        # Play game music if available
        if hasattr(self.game.assets, 'play_sound') and "game_music" in self.game.assets.sounds:
            self.game.assets.play_sound("game_music")
            
    def exit(self):
        # Clean up any playing state resources
        pass

class PausedState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_state(STATE_PLAYING)
                    
            # Handle pause menu button clicks
            for button in self.game.pause_buttons:
                result = button.handle_event(event)
                if result:  # If button action returned something
                    return result
        
    def update(self):
        # Use scaled mouse position
        raw_mouse_pos = pygame.mouse.get_pos()
        scaled_mouse_pos = self.game.scale_mouse_pos(raw_mouse_pos)
        for button in self.game.pause_buttons:
            button.update(scaled_mouse_pos)
        
    def draw(self, screen):
        # First draw the game (dimmed)
        self.game.states[STATE_PLAYING].draw(screen)
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Draw pause menu
        font = self.game.assets.get_font("main")
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.game.design_width // 2, 100))
        screen.blit(text, text_rect)
        
        # Draw buttons
        for button in self.game.pause_buttons:
            button.draw(screen)
            
    def enter(self):
        # Pause any sounds or music if needed
        pass
    
    def exit(self):
        # Resume any sounds or music if needed
        pass

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                # Any key press returns to menu
                self.game.set_state(STATE_MENU)
                
    def update(self):
        # Any animations or timers for game over screen
        pass
        
    def draw(self, screen):
        # Draw background (dimmed)
        screen.fill((0, 0, 0))
        
        # Draw "Game Over" text
        font = self.game.assets.get_font("main")
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 - 50))
        screen.blit(text, text_rect)
        
        # Draw score if available
        if hasattr(self.game, 'score'):
            score_font = self.game.assets.get_font("main")
            score_text = score_font.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 + 20))
            screen.blit(score_text, score_rect)
        
        # Draw "Press any key to continue" text
        prompt_font = self.game.assets.get_font("main")
        prompt_text = prompt_font.render("Press any key to return to menu", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 + 80))
        screen.blit(prompt_text, prompt_rect)
    
    def enter(self):
        # Play game over sound if available
        if hasattr(self.game.assets, 'play_sound') and "game_over" in self.game.assets.sounds:
            self.game.assets.play_sound("game_over")
    
    def exit(self):
        # Clean up any game over specific resources
        pass

class VictoryState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                # Any key press returns to menu
                self.game.set_state(STATE_MENU)
                
    def update(self):
        # Any animations or timers for victory screen
        pass
        
    def draw(self, screen):
        # Draw background (festive)
        screen.fill((0, 0, 50))  # Dark blue background
        
        # Draw "Victory!" text
        font = self.game.assets.get_font("main")
        text = font.render("VICTORY!", True, (255, 215, 0))  # Gold color
        text_rect = text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 - 50))
        screen.blit(text, text_rect)
        
        # Draw score if available
        if hasattr(self.game, 'score'):
            score_font = self.game.assets.get_font("main")
            score_text = score_font.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 + 20))
            screen.blit(score_text, score_rect)
        
        # Draw "Press any key to continue" text
        prompt_font = self.game.assets.get_font("main")
        prompt_text = prompt_font.render("Press any key to return to menu", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.game.design_width // 2, self.game.design_height // 2 + 80))
        screen.blit(prompt_text, prompt_rect)
    
    def enter(self):
        # Play victory sound if available
        if hasattr(self.game.assets, 'play_sound') and "victory" in self.game.assets.sounds:
            self.game.assets.play_sound("victory")
    
    def exit(self):
        # Clean up any victory specific resources
        pass
