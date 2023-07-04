import pygame
import pygame

# Set the desired window dimensions
window_width = 800
window_height = 600

# Set the desired initial y position
initial_y = 500

# Initialize the game
pygame.init()
window = pygame.display.set_mode((window_width, window_height))

# Create the player sprite
player_image = pygame.Surface((50, 50))  # Placeholder surface for the player image
player_rect = player_image.get_rect()
player_rect.x = window_width // 2  # Set the initial x position to the middle of the window
player_rect.y = initial_y  # Set the initial y position

# Camera system variables
camera_offset_x = 0
camera_offset_y = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic

    # Update camera position based on player's position
    camera_offset_y = -player_rect.y + window_height // 2

    # Draw game objects
    window.fill((0, 0, 0))  # Fill the window with black color
    pygame.draw.rect(window, (255, 0, 0), player_rect.move(camera_offset_x, camera_offset_y))  # Draw the player sprite with camera offset
    pygame.display.flip()

pygame.quit()
