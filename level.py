import pygame
from tile import Tile
from player import Player
from enemy import Enemy
from settings import *
from ui import UI
from light import Light
from particles import AnimationPlayer
from projectile import Projectile
from pygame.math import Vector2
from inventory import *
from itens import *


class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.elapsed_time = 0

        # sprite groups setup
        self.visible_sprites = YSortCameraGroup()
        self.lootable_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.animation_player = AnimationPlayer()

        # light setup
        self.light = Light()
        self.id_index = 0
        print(IMG_SCALE)
        # create map
        self.show_map = False
        self.create_map()
        self.create_torches()  # Add this line

        self.ui = UI(self.player)  # Add this line
        self.last_update_time = 0
        self.update_interval = 2000  # 2 seconds in milliseconds
        self.inventory = Inventory(self.player, 6, 2)
        self.new()

    def run(self, mouse_buttons):

        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_update_time > self.update_interval:
            self.ui.update_explored_area(tile_map)
            self.last_update_time = current_time        
        
        self.player.mouse_buttons = mouse_buttons
        self.check_for_loot()

        if self.player.show_map:
            self.ui.display(tile_map)
        
        elif self.player.inventory_toggled:
            if not self.inventory.can_loot and self.player.can_loot:
                self.add_loot()

            self.inventory.can_loot = self.player.can_loot
            print(self.inventory.can_loot)
            self.update_inventory()
        
        else:
            self.visible_sprites.custom_draw(self.player, self.light)
            self.ui.draw_stats()

        self.visible_sprites.update()

    def create_map(self):
        self.background = pygame.Surface((MAP_SIZE_X * TILE_SIZE, MAP_SIZE_Y * TILE_SIZE))
        for row_index, row in enumerate(tile_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                color = color_map[row_index][col_index]

                pygame.draw.rect(self.background, color, (x, y, TILE_SIZE, TILE_SIZE))

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], sprite_type = 'invisible_wall', img_path = 'graphics/test/rock.png')

        cont = 0
        print('OBJECTS')
        for row_index, row in enumerate(entity_map):

            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == '394':
                    self.player = Player(
                        pos=(x, y),
                        groups=[self.visible_sprites],
                        obstacle_sprites=self.obstacle_sprites,
                        lootable_sprites=self.obstacle_sprites,
                        background=self.background,
                        projectile_group=self.visible_sprites,
                        create_projectile=self.create_projectile,
                        id=self.id_index
                        )
                    self.id_index += 1
                if col == '390':
                    Enemy(
                        'bamboo',
                        (x,y),
                        [self.visible_sprites,self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp,
                        self.create_projectile,
                        self.create_lootbag,
                        self.id_index)
                    
                    self.id_index += 1
                
                # Place the Torchs
                if col == 't':
                    Tile((x, y), self.visible_sprites, sprite_type = 'torch', spritesheet = 'graphics/objects/torches', length = 8)



    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.actual_health -= amount
            print(self.player.actual_health)
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):

        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_exp(self,amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused 

    def create_torches(self):
        cont = 0
        for row_index, row in enumerate(entity_map):
            for col_index, col in enumerate(row):
                if col == 't':  # Change 'l' to 't' to match the torch sprite placement
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    self.light.add_torch(x, y)
                    cont += 1
                    print(f'LIGHT CONT: {cont}, X: {x}, Y: {y}')    

    def create_projectile(self, name, entity_type, rect, player_offset, target_pos = None, id = None):
        Projectile(self.visible_sprites, self.obstacle_sprites, self.visible_sprites, entity_type, rect, player_offset, name, target_pos, id)

    def new(self):
        self.inventory.addItemInv(helmet_armor)
        self.inventory.addItemInv(hp_potion)
        self.inventory.addItemInv(sword_steel)
        self.inventory.addItemInv(sword_wood)
        self.inventory.addItemInv(chest_armor)
        self.inventory.addItemInv(upg_helmet_armor)
        self.inventory.addItemInv(upg_chest_armor)

    def add_loot(self):
        for item in self.player.loot:
            print(item)
            self.inventory.addItemInv(item, loot=True)

    def update_inventory(self):
        if self.player.mouse_buttons[2] and not self.inventory.switched_item:
            mouse_pos = pg.mouse.get_pos()
            self.inventory.checkSlot(self.display_surface, mouse_pos)
            self.inventory.switched_item = True
        
        elif not self.player.mouse_buttons[2] and self.inventory.switched_item:
            self.inventory.switched_item = False

        elif self.player.mouse_buttons[0] and not self.inventory.holding_item:
            self.inventory.moveItem(self.display_surface)
            self.inventory.holding_item = True

        elif not self.player.mouse_buttons[0] and self.inventory.holding_item:
            self.inventory.placeItem(self.display_surface)
            self.inventory.holding_item = False
        
        self.inventory.draw(self.display_surface)
    
    def create_lootbag(self, pos, loot):
        loot = LootBag([self.visible_sprites, self.lootable_sprites], pos, loot)
    
    def check_for_loot(self):
        for loot in self.lootable_sprites:
                if loot.rect.colliderect(self.player.rect):
                    self.player.can_loot == True
                    print(self.player.can_loot)
                    self.player.loot = loot.loot


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.sprite_type = 'camera'
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, light):

        # Update the camera offset to follow the player
        self.offset.x = player.rect.centerx - self.half_width + player.rect.width/2
        self.offset.y =  player.rect.centery - self.half_height + player.rect.height/2

        # Clamp the camera offset
        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH ))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))

        # Remove clipping region and clear the entire screen
        self.display_surface.set_clip(None)
        self.display_surface.fill((0, 0, 0))  # Clear the screen

        # Draws the background
        background_offset = self.offset.x - TILE_SIZE/2, self.offset.y - TILE_SIZE/2
        self.display_surface.blit(player.background, (-background_offset[0], -background_offset[1]))

        # Draw the scene (sprites, background, etc.)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.sprite_type not in ["invisible_wall"]:
                offset_pos = sprite.rect.center - self.offset
                if sprite.sprite_type == 'enemy':
                    sprite.player_rect_center = player.rect.center
                if sprite.sprite_type == 'projectile':
                    offset_pos = sprite.rect.center - self.offset
                    if sprite.shield:
                        sprite.pivot = pygame.math.Vector2(player.rect.centerx + player.rect_width/2, player.rect.centery + player.rect_height/2)
                        if not MOUSE_BUTTONS[2]:
                            sprite.kill()
                    
                self.display_surface.blit(sprite.image, offset_pos) 
                   

        #light.cast_light(player)