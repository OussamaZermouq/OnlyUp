import sys
import pygame
from settings import *
from level import Level
from game_data import level_0

pygame.init()
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock=pygame.time.Clock()
level = Level(level_0,screen)
pygame.mixer.init()
pygame.mixer.music.load("Assets/Music/song0.mp3")
pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    level.run()
    pygame.display.update()
    clock.tick(60)
