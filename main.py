import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))

#Clock
clock = pygame.time.Clock()

running = True
while running:

    # Set frame rate
    clock.tick(60)

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s]:
        player_pos[1] += player_speed

    #Player bound restriction
    player_pos[0] = max(0, min(player_pos[0], screen_width - player_size))
    player_pos[1] = max(0, min(player_pos[1], screen_height - player_size))

    #Clear the screen
    screen.fill(BLACK)
    
    #Drawing the players
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.draw.circle(screen, RED, (screen_width // 2, 100), 30)

    font = pygame.font.Font(None, 36)
    text = font.render("Use WASD keys to move", True, WHITE)
    screen.blit(text, (screen_width // 2 - 150, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
