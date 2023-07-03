import pygame

# Create a sprite group
sprite_group = pygame.sprite.Group()

# Add some sprites to the group
sprite1 = pygame.sprite.Sprite()
sprite1.rect = pygame.Rect(100, 100, 50, 50)
sprite_group.add(sprite1)

sprite2 = pygame.sprite.Sprite()
sprite2.rect = pygame.Rect(200, 200, 30, 30)
sprite_group.add(sprite2)

# Calculate the bounding rectangle
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for sprite in sprite_group:
    if sprite.rect.x < min_x:
        min_x = sprite.rect.x
    if sprite.rect.y < min_y:
        min_y = sprite.rect.y
    if sprite.rect.x + sprite.rect.width > max_x:
        max_x = sprite.rect.x + sprite.rect.width
    if sprite.rect.y + sprite.rect.height > max_y:
        max_y = sprite.rect.y + sprite.rect.height

# Create the bounding rectangle
bounding_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

# Print the bounding rectangle
print(bounding_rect)
