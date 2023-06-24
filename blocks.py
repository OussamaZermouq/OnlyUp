import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self,y_shift):
        self.rect.y+=y_shift