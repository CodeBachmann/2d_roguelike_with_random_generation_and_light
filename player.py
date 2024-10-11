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

        self.mouse_direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.speed = 20
        self.background = background

        self.view_radius = 300
          # Fill with opaque black

    def input(self):
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
            
