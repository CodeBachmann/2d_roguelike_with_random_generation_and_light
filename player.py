import pygame, math
from settings import *
from entity import Entity
from support import import_folder
from debug import debug
class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, lootable_sprites, background, projectile_group, id, player_class='Fighter', create_projectile=None):
        super().__init__(groups)
        
        # Define Sprite and Position
        self.id = id
        self.sprite_type = 'player'
        self.import_player_assets()
        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft = pos)
        self.rect_width, self.rect_height = self.rect.size  # Use the size attribute directly
        self.hitbox = self.rect.inflate(-10, HITBOX_OFFSET['player'])
        self.create_projectile = create_projectile
        
        self.offset = pygame.math.Vector2(0, 0)
        self.status = 'down'
        
        # Define Class
        self.player_class = player_class

        # Define Stats
        self.base_stats()
        self.max_stats()
        self.actual_stats()

        # Define Weapon
        self.armor = {'head': None, 'chest': None, 'legs': None, 'feet': None, 'hands': None}
        self.accessory = {'left': None, 'right': None, 'neck': None}
        self.weapon_1 = None
        self.weapon_2 = None
        self.weapon_data = weapon_data
        self.m1 = 'slash'
        self.m2 = 'buckler'
        self.mouse_direction = pygame.math.Vector2()
        self.angle =  math.degrees(math.atan2(self.mouse_direction.y, self.mouse_direction.x))
        self.vector_angle = pygame.Vector2(1, 0)
        self.lootable_sprites = lootable_sprites
        self.obstacle_sprites = obstacle_sprites
        self.projectile_group = projectile_group
        self.mouse_buttons = MOUSE_BUTTONS

        # Define Map
        self.show_map = False
        self.background = background

        # timers
        self.map_toggle_timer = 0

        # cooldowns
        self.attacking = False
        self.defending = False
        self.map_toggled = False
        self.inventory_toggled = False
        self.c_cooldown = False
        self.v_cooldown = False
        self.b_cooldown = False
        self.can_loot = False
        self.touching_loot = None

        # lighting
        self.view_radius = int(500 * IMG_SCALE)
        self.cone = True
        self.circle = True

        #vulnerability
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        self.exp = 0


    def input(self):
        self.map_toggle_timer -= 1
        keys = pygame.key.get_pressed()

        if not self.attacking:

            if keys[pygame.K_m] and not self.map_toggled:
                self.show_map = not self.show_map
                self.map_toggled = True
                self.map_toggle_time = pygame.time.get_ticks()
            
            if keys[pygame.K_c] and not self.c_cooldown:
                self.cone = not self.cone
                self.c_cooldown = True
                self.c_time = pygame.time.get_ticks()

            if keys[pygame.K_v] and not self.v_cooldown:
                self.circle = not self.circle
                self.v_cooldown = True
                self.v_time = pygame.time.get_ticks()

            if keys[pygame.K_b] and not self.b_cooldown:
                self.inventory_toggled = not self.inventory_toggled
                self.b_cooldown = True
                self.b_time = pygame.time.get_ticks()

            if not self.inventory_toggled:
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

                if not self.defending:
                    self.attack()
                
        else:
            self.direction.x = 0
            self.direction.y = 0 

    def attack(self):

        if self.mouse_buttons[0]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            damage = self.m1_base_damage + (1 * self.strength)
            self.create_projectile(self.m1, entity_type = 'player', rect = self.rect, player_offset = self.offset, id = self.id, damage = damage)  # Add this line
            print("left mouse button pressed")

        elif self.mouse_buttons[2]:
            if projectile_data[self.m2]['shield']:
                self.defending = True
                self.attack_time = pygame.time.get_ticks()
                self.create_projectile(self.m2, entity_type = 'player', rect = self.rect, player_offset = self.offset, id=self.id)
                self.actual_speed -= self.max_speed/2
                #self.view_radius -= 10

                print("right mouse button pressed")

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker 
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)  
    
    def get_mouse_position(self):
        mouse_pos = pygame.mouse.get_pos()
        player_screen_pos = (self.rect.centerx - self.offset.x, self.rect.centery - self.offset.y)
        
        self.mouse_direction = pygame.math.Vector2(mouse_pos[0] - player_screen_pos[0], 
                                                mouse_pos[1] - player_screen_pos[1])
        self.mouse_position = mouse_pos
        self.angle = (mouse_pos - pygame.Vector2(self.rect.center)).angle_to(pygame.Vector2(1, 0)) - 90
        # Calculate angle, adjusting for PyGame's coordinate system
        self.angle = math.degrees(math.atan2(-self.mouse_direction.y, self.mouse_direction.x))
        
        # Ensure angle is between 0 and 360 degrees
        self.angle = (self.angle + 360) % 360

    def cooldowns(self):
        time = pygame.time.get_ticks()

        if self.attacking:
            if time - self.attack_time > 500:
                self.attacking = False

        if self.map_toggled:
            if time - self.map_toggle_time > 200:
                self.map_toggled = False

        if self.c_cooldown:
            if time - self.c_time > 200:
                self.c_cooldown = False

        if self.v_cooldown:
            if time - self.v_time > 200:
                self.v_cooldown = False

        if not self.vulnerable:
            if time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        
        if self.defending and not self.mouse_buttons[2]:
            if time - self.attack_time > 200:
                self.defending = False
                self.actual_speed += self.max_speed/2
        
        if self.b_cooldown:
            if time - self.b_time > 200:
                self.b_cooldown = False


    def update(self):
        self.input()
        self.get_mouse_position()        
        self.move(self.actual_speed)
        self.get_offset()
        self.cooldowns()
        self.get_status()
        self.animate()
        
        # debug(f'ANGLE:{self.angle}', y = 10*IMG_SCALE)
        # debug(f'RIGHT MOUSE:{self.mouse_buttons[2]}', y = 40*IMG_SCALE)
        # debug(f'MOUSE DIRECTION:{self.mouse_direction}', y = 70*IMG_SCALE)
        # debug(f'OFFSET:{self.offset}', y = 190*IMG_SCALE)
        # debug(f'MOUSE - OFFSET:{self.mouse_direction + self.offset}', y = 130*IMG_SCALE)
        debug(f'PLAYER POS:{self.rect.center}', y = 160*IMG_SCALE)
        # debug(f'MOUSE SCREEN POS:{pygame.mouse.get_pos()}', y = 220*IMG_SCALE)
        # debug(f'PLAYER SCREEN POS:{self.rect.center - self.offset}', y = 250*IMG_SCALE)
        # debug(f'ANGLE:{self.rect.size}', y = 280*IMG_SCALE)


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

        x_c = x if x > 0 else (x*-1)
        y_c = y if y > 0 else (y*-1)

        if x_c > y_c:
            self.status = 'right' if x > 0 else 'left'
        else:
            self.status = 'down' if y > 0 else 'up'
    
        if self.attacking:
            self.status += '_attack'

        elif self.direction == [0,0]:
            self.status += '_idle'

      
    def base_stats(self):
        self.health = classes_data[self.player_class]['hp']
        self.mana = classes_data[self.player_class]['mana']
        self.stamina = classes_data[self.player_class]['stamina']
        self.prot = classes_data[self.player_class]['prot']
        self.speed = int(classes_data[self.player_class]['speed'] * IMG_SCALE)
        self.wisdom = classes_data[self.player_class]['wisdom']
        self.dexterity = classes_data[self.player_class]['dexterity']
        self.strength = classes_data[self.player_class]['strength']
        self.endurance = classes_data[self.player_class]['endurance']
        self.intelligence = classes_data[self.player_class]['intelligence']
        self.vigor = classes_data[self.player_class]['vigor']
        self.faith = classes_data[self.player_class]['faith']
        self.level = classes_data[self.player_class]['level']
        self.xp = 0
        self.xp_to_next_level = 100
        
    def max_stats(self):
        self.max_health = self.health + (22 * self.vigor)
        self.max_mana = self.mana + (1 * self.wisdom)
        self.max_stamina = self.stamina + (2 * self.endurance)
        self.max_prot = self.prot
        self.max_speed = self.speed
        self.max_wisdom = self.wisdom 
        self.max_dexterity = self.dexterity
        self.max_strength = self.strength
        self.max_endurance = self.endurance
        self.max_intelligence = self.intelligence
        self.max_vigor = self.vigor
        self.max_faith = self.faith

    def actual_stats(self):
        self.actual_health = self.max_health
        self.actual_mana = self.max_mana
        self.actual_stamina = self.max_stamina
        self.actual_prot = self.max_prot
        self.actual_speed = self.max_speed
        self.actual_wisdom = self.max_wisdom
        self.actual_dexterity = self.max_dexterity
        self.actual_strength = self.max_strength
        self.actual_endurance = self.max_endurance
        self.actual_intelligence = self.max_intelligence
        self.actual_vigor = self.max_vigor
        self.actual_faith = self.max_faith

    def addHp(self, hp_gain):
        self.actual_health += hp_gain
        self.actual_health = min(self.actual_health, self.max_health)

    def addProt(self, prot_gain):
        self.actual_prot += prot_gain

    def equip_armor(self, item):
        if self.armor[item.slot] != None:
            self.unequip_armor(item.slot)
        self.armor[item.slot] = item
        self.actual_prot += item.prot

    def unequip_armor(self, slot):
        if self.armor[slot] != None:
            self.actual_prot -= self.armor[slot].prot
            self.armor[slot] = None

    def equip_weapon(self, weapon):
        if self.weapon_1 != None:
            self.unequip_weapon(1)
            
        elif self.weapon_2 != None:
            self.unequip_weapon(2)
                
        if weapon.slot == "hand":
            self.weapon_1 = weapon
            self.m1 = weapon.projectile
            self.m1_base_damage = weapon.base_damage

        elif weapon.slot == "right_hand":
            self.weapon_2 = weapon
            self.m2 = weapon.projectile
            self.m2_base_damage = weapon.base_damage

    def unequip_weapon(self, hand):
        if self.weapon_1 != None and hand == 1:
            self.m1_base_damage = 0
            self.weapon_1 = None
        
        elif self.weapon_2 != None and hand == 2:
            self.m2_base_damage = 0
            self.weapon_2 = None
    
    def shield_block(self, damage):
        pass