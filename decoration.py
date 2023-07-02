import pygame
from settings import *
from tiles import AnimatedTile,StaticTile
from support import import_folder
from random import choice, randint

class Sky:

    def __init__(self,horizon):
        self.top = pygame.image.load('Assets/Sky/sky_top.png').convert()
        self.bottom = pygame.image.load('Assets/Sky/sky_bottom.png').convert()
        self.middle= pygame.image.load('Assets/Sky/sky_middle.png').convert()
        self.horizon = horizon

        #stretch 
        self.top = pygame.transform.scale(self.top,(SCREEN_HEIGHT,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(SCREEN_HEIGHT,tile_size))
        self.middle = pygame.transform.scale(self.middle,(SCREEN_HEIGHT,tile_size))

    def draw(self,surface):
        for row in range(horizontal_tile_number):
            x = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(x,0))
            elif row == self.horizon:
                surface.blit(self.middle,(x,0))
    
class Clouds:
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surf_list = import_folder('Assets/Clouds')
        min_x = -SCREEN_WIDTH
        max_x = level_width + SCREEN_WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range (cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)