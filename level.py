import pygame
from tile import Tile
from player import Player
from enemy import Enemy
from settings import *
from ui import UI
from light import Light
from particles import AnimationPlayer


class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        self.elapsed_time = 0
        # sprite groups setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.animation_player = AnimationPlayer()
        # light setup
        self.light = Light()
        
        # create map
        self.show_map = False
        self.create_map()
        self.create_torches()  # Add this line

        self.ui = UI(self.player)  # Add this line
        self.last_update_time = 0
        self.update_interval = 2000  # 2 seconds in milliseconds


    def run(self, mouse_buttons):

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_interval:
            self.ui.update_explored_area(tile_map)
            self.last_update_time = current_time        
        
        self.player.mouse_buttons = mouse_buttons

        if self.player.show_map:
            self.ui.display(tile_map)
        else:
            self.visible_sprites.custom_draw(self.player, self.light)
            self.visible_sprites.enemy_update(self.player)

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
        print(f'OBJECTS')
        for row_index, row in enumerate(entity_map):
            
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == '394':
                    self.player = Player(
                        pos=(x, y),
                        groups=[self.visible_sprites],
                        obstacle_sprites=self.obstacle_sprites,
                        background=self.background,
                        projectile_group=self.visible_sprites
                        )
                if col == '390':
                    Enemy(
                        'bamboo',
                        (x,y),
                        [self.visible_sprites,self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp)
                if col == 't':
                    Tile((x, y), [self.visible_sprites], sprite_type = 'torch', spritesheet = 'graphics/objects/torches', length = 8)
                    cont+=1
                    print(f'CONT: {cont}, X: {x}, Y: {y}')



    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
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


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
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
                self.display_surface.blit(sprite.image, offset_pos) 


        light.cast_light(player)


    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
            


 