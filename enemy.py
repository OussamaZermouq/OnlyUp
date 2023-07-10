import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y,'Tiled/graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)
        #self.gravity = 0.8
        self.direction = pygame.math.Vector2(0,0)
    
    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed>0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, y_shift):
        self.rect.y += y_shift
        #self.apply_gravity()
        self.animate()
        self.move()
        self.reverse_image()