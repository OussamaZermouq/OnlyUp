import sys
import pygame
from settings import *
from level import Level
from game_data import level_0
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level =2
        self.overworld = Overworld(2,self.max_level,screen)
    def run(self):
        self.overworld.run()
        
pygame.init()
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock=pygame.time.Clock()
level = Level(level_0,screen)
game = Game()
pygame.mixer.init()
pygame.mixer.music.load("Assets/Music/song0.mp3")
#pygame.mixer.music.play(-1)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    level.run()
    #game.run()
    pygame.display.update()
    clock.tick(60)
