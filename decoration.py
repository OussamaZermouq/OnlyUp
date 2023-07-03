import pygame
from settings import *
from tiles import AnimatedTile,StaticTile
from support import import_folder
from random import choice, randint

class Sky:

    def __init__(self,horizon):
        self.top = pygame.image.load('Assets/Sky/sky_top.png').convert()
        self.middle= pygame.image.load('Assets/Sky/sky_middle.png').convert()
        self.bottom = pygame.image.load('Assets/Sky/sky_bottom.png').convert()
        self.horizon = horizon

        #stretch 
        self.top = pygame.transform.scale(self.top,(SCREEN_WIDTH,tile_size))
        self.middle = pygame.transform.scale(self.middle,(SCREEN_WIDTH,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(SCREEN_WIDTH,tile_size))

    def draw(self,surface):
        for row in range(horizontal_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
    
class Clouds:

    def __init__(self,horizon,level_width,cloud_number):
        cloud_surf_list = import_folder('Assets/Clouds')
        #des valeurs max et min pour x et y pour creer une intervale 
        #des nuages
        min_y = -SCREEN_HEIGHT
        max_y = level_width + SCREEN_HEIGHT
        min_x = 0
        max_x = SCREEN_WIDTH
        self.cloud_sprites = pygame.sprite.Group()
        #une boucle pour generer des nuages
        for cloud in range (cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)