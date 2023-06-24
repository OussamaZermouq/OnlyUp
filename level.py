import pygame
from blocks import Block
from settings import *
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.setup_level(level_data) 
        self.world_shift=0
        self.current_x = 0

        self.dust_sprite = pygame.sprite.GroupSingle()
        player_on_ground = False
        
    def setup_level(self,layout):
        self.blocks = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * BLOCK_SIZE
                y = row_index * BLOCK_SIZE

                if col == 'X':
                    block=Block((x,y),BLOCK_SIZE)
                    self.blocks.add(block)
                if col == 'P':
                    player=Player((x,y),self.display_surface,self.create_jump_particles)
                    self.player.add(player)
    

#note: seems that even if the player is below the trigger point it doesnt appear on the screen, make an infinite loop which can be broken when the player is back on frame

    def scroll_Y(self):
        player = self.player.sprite
        player_y = player.rect.centery
        direction_y = player.direction.y

        if player_y<100 and direction_y < 0:
            self.world_shift = 8
            player.speed=0
        elif player_y > 600 and direction_y > 0:
            self.world_shift = -8
            player.speed=0
        else:
            self.world_shift = 0
            player.speed=8
    

    def create_jump_particles(self,pos):
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x*player.speed

        for sprite in self.blocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False


    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.blocks.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y=0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y=0
                    player.on_ceiling = True
                    
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust)

    def run(self):

        #dust
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #level
        self.blocks.update(self.world_shift)
        self.blocks.draw(self.display_surface)
        self.scroll_Y()

        #player methods
        self.player.update()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface) 

