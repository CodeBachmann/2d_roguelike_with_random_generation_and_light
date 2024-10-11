import pygame
from tile import Tile
from player import Player
from enemy import Enemy
from settings import *
from ui import UI
from light import Light

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.light = Light()
        
        
        # create map
        self.create_map()
        self.ui = UI(self.player)  # Add this line

    def run(self):
        self.visible_sprites.custom_draw(self.player, self.light)
        self.visible_sprites.update()
        self.ui.display(tile_map)        

    def create_map(self):
        self.background = pygame.Surface((MAP_SIZE_X * TILE_SIZE, MAP_SIZE_Y * TILE_SIZE))
        for row_index, row in enumerate(tile_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                color = color_map[row_index][col_index]

                pygame.draw.rect(self.background, color, (x, y, TILE_SIZE, TILE_SIZE))

                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], img_path = 'graphics/test/rock.png')
                
        for row_index, row in enumerate(entity_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == '394':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.background)
                if col == '390':
                    Enemy(
                        'bamboo',
                        (x,y),
                        [self.visible_sprites,self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp)



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

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
       


    def custom_draw(self, player, light):

        # Update the camera offset to follow the player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y =  player.rect.centery - self.half_height

        # Clamp the camera offset
        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))

        # Create a surface for the circular area
        circular_area = pygame.Surface((player.view_radius * 2, player.view_radius * 2), pygame.SRCALPHA)
        circular_area.fill((0, 0, 0, 255))  # Fill with opaque black
        pygame.draw.circle(circular_area, (0, 0, 0, 0), (player.view_radius, player.view_radius), player.view_radius)  # Draw transparent circle

        # Remove clipping region and clear the entire screen
        self.display_surface.set_clip(None)
        self.display_surface.fill((0, 0, 0))  # Clear the screen

        # Set the clipping region to a square around the circular area
        area_topleft = (player.rect.centerx - player.view_radius - self.offset.x, player.rect.centery - player.view_radius - self.offset.y)
        clip_rect = pygame.Rect(area_topleft, (player.view_radius * 2, player.view_radius * 2))
        self.display_surface.set_clip(clip_rect)

        # Draws the background
        background_offset = self.offset.x-32, self.offset.y-32
        self.display_surface.blit(player.background, (-background_offset[0], -background_offset[1]))
        light.cast_light(player)


        # Draw the scene (sprites, background, etc.)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.sprite_type == "player":
                sprite.rect.centery = sprite.rect.centery - sprite.rect.size[1]/2
                sprite.rect.centerx = sprite.rect.centerx - sprite.rect.size[0]
                offset_pos = sprite.rect.center - self.offset

                self.display_surface.blit(sprite.image, offset_pos)
            elif sprite.sprite_type != "tile":
                offset_pos = sprite.rect.center - self.offset
                self.display_surface.blit(sprite.image, offset_pos)                
        
        # Draw the transparent circle on top of the rectangular clipping region
        self.display_surface.blit(circular_area, area_topleft)

        
        # Clear the clipping region and draw any other things that should be visible
        self.display_surface.set_clip(None)

            


 