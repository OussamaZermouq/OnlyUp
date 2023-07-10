import pygame
from support import import_folder
from math import sin

class Player (pygame.sprite.Sprite):

    def __init__(self,pos,surface,create_jump_particles,change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        #dust 
        self.import_dust_run_particle()
        self.dust_frame_index=0
        self.dust_animation_speed=0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        self.direction = pygame.math.Vector2(0,0)
        self.speed=8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        #x=64
        #y=2688
        #health
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

    def import_character_assets(self):
        path='Assets/character/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}
        for animation in self.animations.keys():
            full_path=path+animation
            self.animations[animation]=import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys [pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        player_image  = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = player_image
        else:
            flipped_player_image = pygame.transform.flip(player_image,flip_x = True,flip_y =False)
            self.image = flipped_player_image

        if self.invincible:
            #controle d'opacite
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft= self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.on_ceiling and self.on_right :
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left :
            self.rect = self.image.get_rect(topleft = self.rect.topleft)

        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particle):
                self.dust_frame_index = 0

            dust_partcile = self.dust_run_particle[int(self.dust_frame_index)]

            if self.facing_right:
                #if you change the player pictures change the x and y of this vector and set them to be correct with the picture
                pos = self.rect.bottomleft - pygame.math.Vector2(-4,20)
                self.display_surface.blit(dust_partcile,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(60,20)
                flipped_dust_particle = pygame.transform.flip(dust_partcile,True,False)
                self.display_surface.blit(flipped_dust_particle,pos)

    def import_dust_run_particle(self):
        self.dust_run_particle =import_folder('Assets/character/dust/run')

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False


    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1: # to avoid the standing bug otherwise it should be 0 
            self.status = 'fall'
        else:
            if self.direction.x !=0:
                self.status = 'run'
            else:
                self.status = 'idle'


    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value>= 0:
            return 255
        else :
            return 0


    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()