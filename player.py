import pygame
from settings import *
from entity import Entity
from support import import_folder
from debug import debug

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, background):
        super().__init__(groups)
        self.sprite_type = 'player'
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
        self.map_toggle_cooldown = 0

        self.mouse_direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.speed = 7
        self.background = background

        self.view_radius = 300
        self.show_map = False
          # Fill with opaque black

    def input(self):
        self.map_toggle_cooldown -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        
        if keys[pygame.K_m] and self.map_toggle_cooldown <= 0:
            self.show_map = not self.show_map
            self.map_toggle_cooldown = 20  # Adjust this value to set the cooldown duration

    
    def mouse_position(self):
        self.mouse_direction = pygame.math.Vector2(pygame.mouse.get_pos()) - self.rect.center

    def update(self):
        self.input()
        self.mouse_position()
        self.move(self.speed)
        debug(self.mouse_direction)

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
