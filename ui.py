import pygame


#class interface
class UI:
    def __init__(self, surface):
        #setup 
        self.display_surface = surface

        #health 
        self.health_bar = pygame.image.load('Assets/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54,38)
        self.bar_max_width = 152
        self.bar_height = 4

        #coins
        #self.coin = pygame.image.load('Assets/ui/coin.png').convert_alpha()
        self.coin = pygame.image.load('Tiled/graphics/coins/gold/0.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,61))

        #font
        self.font = pygame.font.Font('Assets/ui/ARCADEPI.TTF',30)

    def show_health(self,current_health,full_health):
        self.display_surface.blit(self.health_bar,(20,10))
        current_health_ratio = current_health/full_health
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
        pygame.draw.rect(self.display_surface,'red',health_bar_rect)

    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'white')
        #position du texte
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 5,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)
