import pygame
from tile import Tile
from player import Player
from settings import *
from ui import UI
from light import Light

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite groups setup
        self.visibles_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.light = Light()
        # create map
        self.create_map()
        self.ui = UI(self.player)  # Add this line

        
    def run(self):
        self.visibles_sprites.custom_draw(self.player)
        self.light.cast_light(self.player)
        self.visibles_sprites.update()
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
                    Tile((x, y), [self.visibles_sprites, self.obstacle_sprites], img_path = 'graphics/test/rock.png')
                
        for row_index, row in enumerate(entity_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'p':
                    self.player = Player((x, y), [self.visibles_sprites], self.obstacle_sprites, self.background)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):
        
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))

        background_offset = self.offset.x, self.offset.y
        self.display_surface.blit(player.background, (-background_offset[0], -background_offset[1]))


        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.center - self.offset

            self.display_surface.blit(sprite.image, offset_pos) 
            
            


 