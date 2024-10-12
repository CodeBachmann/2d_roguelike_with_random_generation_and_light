import pygame, math
from settings import *
from entity import Entity
from support import import_folder
from debug import debug

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, background):
        super().__init__(groups)
        self.sprite_type = 'player'
        self.import_player_assets()
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
        self.map_toggle_cooldown = 0
        self.offset = pygame.math.Vector2(0, 0)
        self.status = 'down'

        self.mouse_direction = pygame.math.Vector2()
        self.angle =  math.degrees(math.atan2(self.mouse_direction.y, self.mouse_direction.x))
        self.obstacle_sprites = obstacle_sprites
        self.speed = 7 * IMG_SCALE
        self.background = background

        self.view_radius = int(300 * IMG_SCALE)
        self.show_map = False
        self.mouse_buttons = MOUSE_BUTTONS

        # cooldowns
        self.attacking = False
        self.map_toggled = False


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
        
        if keys[pygame.K_m] and not self.map_toggled:
            self.show_map = not self.show_map
            self.map_toggled = True
            self.map_toggle_time = pygame.time.get_ticks()

        if self.mouse_buttons[0] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.view_radius += 10

            print("left mouse button pressed")
        elif self.mouse_buttons[2] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.view_radius -= 10

            print("right mouse button pressed")

    
    def get_mouse_position(self):
        mouse_pos = pygame.mouse.get_pos()
        player_screen_pos = (self.rect.centerx - self.offset.x, self.rect.centery - self.offset.y)
        
        self.mouse_direction = pygame.math.Vector2(mouse_pos[0] - player_screen_pos[0], 
                                                mouse_pos[1] - player_screen_pos[1])
        self.mouse_position = mouse_pos
        
        # Calculate angle, adjusting for PyGame's coordinate system
        self.angle = math.degrees(math.atan2(-self.mouse_direction.y, self.mouse_direction.x))
        
        # Ensure angle is between 0 and 360 degrees
        self.angle = (self.angle + 360) % 360

    def cooldowns(self):
        if self.attacking:
            if pygame.time.get_ticks() - self.attack_time > 100:
                self.attacking = False
        if self.map_toggled:
            if pygame.time.get_ticks() - self.map_toggle_time > 200:
                self.map_toggled = False

    def update(self):
        self.input()
        self.get_mouse_position()
        self.move(self.speed)
        self.get_offset()
        self.cooldowns()
        self.get_status()
        self.animate()
        debug(f'ANGLE:{self.angle}', y = 10*IMG_SCALE)
        debug(f'RIGHT MOUSE:{self.mouse_buttons[2]}', y = 40*IMG_SCALE)
        debug(f'MOUSE DIRECTION:{self.mouse_direction}', y = 70*IMG_SCALE)
        debug(f'OFFSET:{self.offset}', y = 190*IMG_SCALE)
        debug(f'MOUSE - OFFSET:{self.mouse_direction + self.offset}', y = 130*IMG_SCALE)
        debug(f'PLAYER POS:{self.rect.center}', y = 160*IMG_SCALE)
        debug(f'MOUSE SCREEN POS:{pygame.mouse.get_pos()}', y = 220*IMG_SCALE)
        debug(f'PLAYER SCREEN POS:{self.rect.center - self.offset}', y = 250*IMG_SCALE)
        debug(f'ANGLE:{self.rect.size}', y = 280*IMG_SCALE)


    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            for x, i in enumerate(self.animations[animation]):
                img = pygame.transform.scale(i, (int(i.get_width() * IMG_SCALE), int(i.get_height() * IMG_SCALE)))
                self.animations[animation][x] = img
    
    def get_offset(self):
        self.offset.x = self.rect.centerx - (WIDTH / 2)
        self.offset.y = self.rect.centery - (HEIGHT / 2)

        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH ))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))
    
    def get_status(self):
        x = self.mouse_position[0] - (self.rect.centerx - self.offset.x)
        y = self.mouse_position[1] - (self.rect.centery - self.offset.y)

        if x > 0:
            x_c = x
        else:
            x_c = (x*-1)
        
        if y > 0:
            y_c = y
        else:
            y_c = (y*-1) 

        if x_c > y_c:
            if x > 0:
                self.status = 'right'
            else:
                self.status = 'left'
        else:
            if y > 0:
                self.status = 'down'
            else:
                self.status = 'up'

        if self.attacking:
            self.status = self.status + '_attack'

        elif self.direction == [0,0]:
            self.status = self.status + '_idle'




