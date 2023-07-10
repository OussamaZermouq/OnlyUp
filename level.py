import pygame
from settings import *
from support import *
from player import Player
from particles import ParticleEffect
from support import import_csv_layout
from tiles import Tile, StaticTile,Crate,Coin,Palm
from enemy import Enemy
from decoration import Sky, Clouds
from game_data import levels
from game_data import levels
from music import Music
import random
import time


class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health):
        #self.level = Level(current_level,screen,self.create_overworld)
        #self.setup_level(level_data) 
        self.display_surface = surface
        self.world_shift=10
        self.current_x = 0

        #overword connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)

        #layout pour le terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
        
        #layout pour les crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprite = self.create_tile_group(crate_layout,'crates')

        #layout pour les coins
        coin_layout =  import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'coins')

        #palm trees
        fg_palm_layout = import_csv_layout(level_data['fg_palm'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg_palm')

        #enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')
        
        #constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        #interface
        self.change_coins = change_coins

        #music 
        self.track = Music(random.randint(0,3))
        self.track.run()

        #decoration
        self.sky = Sky(20)
        level_width = len(terrain_layout[0])* tile_size
        self.clouds = Clouds(400, level_width, 20)

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        player_on_ground = False

        #explosion
        self.explosion_sprites= pygame.sprite.Group()


        #level setup 
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]

        #level_content = level_data['content']
        self.new_max_level = level_data['unlock']

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()
        
    def create_tile_group(self,layout,type):
        sprite_group= pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type=='terrain':
                        terrain_tile_list = import_cut_graphic('Tiled/graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    if type=='crates':
                        sprite = Crate(tile_size,x,y)
                    if type == 'coins':
                        sprite = Coin(tile_size,x,y,'Tiled/graphics/coins/gold')
                    if type == 'fg_palm':
                        if val =='0':
                            sprite = Palm(tile_size,x,y,'Tiled/graphics/terrain/palm_small',38)
                        if val =='1':
                            sprite = Palm(tile_size,x,y,'Tiled/graphics/terrain/palm_large',64)
                        else:
                            pass
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)
                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)

                    sprite_group.add(sprite)

        return sprite_group

    #a group that only has the enemy sprite group
    def tile_group_enemy(self,layout,type):
        sprite_group_enemy= pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y)

                    sprite_group_enemy.add(sprite)

        return sprite_group_enemy

    def player_setup(self,layout,change_health):
        for row_index, row in enumerate(layout):
            for col_index,val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size        
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('Assets/character/hat.png')
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)
    
    world_shift = -8
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
            if player_y < 800:
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
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprite.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
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
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprite.sprites() + self.fg_palm_sprites.sprites()
       
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y=0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y=0
                    player.on_ceiling = True

        #une autre methode pour traiter les collision et les movements des enemies:
        #since the enemy object create in the init method is a Group and not a single it doesnt have the rect attribute 
        #which can be used to detect collisions with the terrain
        #enemy = self.enemy_sprites.sprites()
        #collidable_sprites_terrain = self.terrain_sprites.sprites()
        #for sprite_enemy in self.enemy_sprites:
        #    for sprite_terrain in collidable_sprites_terrain:
        #        if sprite_terrain.rect.colliderect(sprite_enemy.rect):
        #            sprite_enemy.rect.bottom = sprite_terrain.rect.top
        #            sprite_enemy.direction.y =0
                     

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    #test si les collision sont horizontal ou vertical avec lenemie
    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                enemy_bottom = enemy.rect.bottom
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >=0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust)

    def check_death(self):
        #si le joueur tombe au dessous de l'ecran + 400 px , il meurt 
        if self.player.sprite.rect.top>(SCREEN_HEIGHT + 2000 ) and self.player.sprite.direction.y>0:
            self.create_overworld(self.current_level,0)
            self.track.stop()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level, self.new_max_level)
            self.track.stop()            
    
    def check_coin_collisions(self):
        pygame.mixer.init()
        player = self.player.sprite
        for coin in self.coin_sprites.sprites():
            if coin.rect.colliderect(player.rect):
                #ajouter le son de collecte des coins
                self.change_coins(1)
                #on utilise une chaine differente pour ne pas ecraser les sons deja execute
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("Assets/Music/coin_effect.mp3"))
                coin.kill()
    
    def run(self):
        #decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        #dust
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #level
        #self.blocks.update(self.world_shift)
        #self.blocks.draw(self.display_surface)
        #terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        #crates
        self.crate_sprite.update(self.world_shift)
        self.crate_sprite.draw(self.display_surface)

        #coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        #fg_palm
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        
        #player_sprites
        self.player.update()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        
        #player methods
        self.player.update()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface) 
        self.scroll_Y()
        
        self.check_coin_collisions()
        self.check_enemy_collisions()

        self.check_death()
        self.check_win()