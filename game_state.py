import pygame
from constants import (
    STATE_MENU, STATE_PLAYING, STATE_PAUSED, 
    STATE_GAME_OVER, STATE_VICTORY
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
        mouse_pos = pygame.mouse.get_pos()
        self.game.menu.update(mouse_pos)
        
    def draw(self, screen):
        self.game.menu.draw(screen)
        
    def enter(self):
        # Reset menu selection or do other initialization
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
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_state(STATE_PAUSED)
                    return
                # Add a key to stop movement if needed
                elif event.key == pygame.K_SPACE:
                    self.game.player.stop_movement()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if right mouse button was clicked
                if event.button == 3:  # 3 is right mouse button
                    # Set the target position for the player to move towards
                    self.game.player.set_target(event.pos)
                    # Create a click indicator
                    self.create_click_indicator(event.pos)
                # Add left click to stop movement if needed
                elif event.button == 1:  # 1 is left mouse button
                    self.game.player.stop_movement()
        
    def update(self):
        # Update player movement
        self.game.player.update()
        
        # Update enemies with collision avoidance
        for enemy in self.game.enemies:
            enemy.update(self.game.enemies)
            
        # Update click indicators
        self.update_click_indicators()
            
        # Check for collisions between player and enemies
        self.check_collisions()

    
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
        screen.blit(self.game.assets.get_image("background"), (0, 0))
        
        # Draw click indicators
        self.draw_click_indicators(screen)
        
        # Draw player
        self.game.player.draw(screen)
        
        # Draw enemies
        for enemy in self.game.enemies:
            enemy.draw(screen)
        
        # Draw UI elements
        self.game.ui_manager.draw_playing_ui(screen)
        
    def draw_click_indicators(self, screen):
        for indicator in self.click_indicators:
            s = pygame.Surface((indicator['radius'] * 2, indicator['radius'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*indicator['color'], indicator['alpha']), 
                              (indicator['radius'], indicator['radius']), indicator['radius'], 2)
            screen.blit(s, (indicator['position'][0] - indicator['radius'], 
                           indicator['position'][1] - indicator['radius']))
        
    def check_collisions(self):
        # Check player-enemy collisions
        player_rect = self.game.player.get_rect()
        for enemy in self.game.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.game.set_state(STATE_GAME_OVER)
                break

    def enter(self):
    # Reset the player's target position when entering the playing state
        if hasattr(self.game.player, 'target_x'):
            self.game.player.target_x = None
            self.game.player.target_y = None
        
        # Clear any click indicators
        self.click_indicators = []
        
        # Play game music if available
        if hasattr(self.game.assets, 'play_sound') and "game_music" in self.game.assets.sounds:
            self.game.assets.play_sound("game_music")

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
        mouse_pos = pygame.mouse.get_pos()
        for button in self.game.pause_buttons:
            button.update(mouse_pos)
        
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
        text_rect = text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(text, text_rect)
        
        # Draw buttons
        for button in self.game.pause_buttons:
            button.draw(screen)

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
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text, text_rect)
        
        # Draw score if available
        if hasattr(self.game, 'score'):
            score_font = self.game.assets.get_font("main")
            score_text = score_font.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
            screen.blit(score_text, score_rect)
        
        # Draw "Press any key to continue" text
        prompt_font = self.game.assets.get_font("main")
        prompt_text = prompt_font.render("Press any key to return to menu", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80))
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
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text, text_rect)
        
        # Draw score if available
        if hasattr(self.game, 'score'):
            score_font = self.game.assets.get_font("main")
            score_text = score_font.render(f"Final Score: {self.game.score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20))
            screen.blit(score_text, score_rect)
        
        # Draw "Press any key to continue" text
        prompt_font = self.game.assets.get_font("main")
        prompt_text = prompt_font.render("Press any key to return to menu", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80))
        screen.blit(prompt_text, prompt_rect)
    
    def enter(self):
        # Play victory sound if available
        if hasattr(self.game.assets, 'play_sound') and "victory" in self.game.assets.sounds:
            self.game.assets.play_sound("victory")
    
    def exit(self):
        # Clean up any victory specific resources
        pass
