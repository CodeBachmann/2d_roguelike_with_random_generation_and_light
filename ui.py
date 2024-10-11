import pygame
from settings import *

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # Minimap setup
        self.minimap_size = 150  # Size of the minimap square
        self.minimap_surface = pygame.Surface((self.minimap_size, self.minimap_size))
        self.minimap_rect = pygame.Rect(WIDTH - self.minimap_size - 10, 10, self.minimap_size, self.minimap_size)
        
        # Zoom factor (higher value means more zoomed in)
        self.zoom_factor = 0.2
        self.minimap_tile_size = int(TILE_SIZE * self.zoom_factor)
        
        # Visible tiles on the minimap (odd number to center on player)
        self.visible_tiles = 15

    def display(self, tile_map):
        self.draw_minimap(tile_map)
        # Add other UI elements here in the future

    def draw_minimap(self, tile_map):
        self.minimap_surface.fill('black')
        
        player_tile_x = int(self.player.rect.centerx / TILE_SIZE)
        player_tile_y = int(self.player.rect.centery / TILE_SIZE)
        
        start_x = max(0, player_tile_x - self.visible_tiles // 2)
        start_y = max(0, player_tile_y - self.visible_tiles // 2)
        end_x = min(MAP_SIZE_X, start_x + self.visible_tiles)
        end_y = min(MAP_SIZE_Y, start_y + self.visible_tiles)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                minimap_x = (x - start_x) * self.minimap_tile_size
                minimap_y = (y - start_y) * self.minimap_tile_size
                
                if tile_map[y][x] == 'x':
                    pygame.draw.rect(self.minimap_surface, 'darkgray', 
                                     (minimap_x, minimap_y, self.minimap_tile_size, self.minimap_tile_size))
                else:
                    pygame.draw.rect(self.minimap_surface, 'lightgray', 
                                     (minimap_x, minimap_y, self.minimap_tile_size, self.minimap_tile_size))

        # Draw player position
        player_minimap_x = (self.visible_tiles // 2) * self.minimap_tile_size
        player_minimap_y = (self.visible_tiles // 2) * self.minimap_tile_size
        pygame.draw.circle(self.minimap_surface, 'red', (player_minimap_x, player_minimap_y), 
                           max(2, int(3 * self.zoom_factor)))

        # Draw minimap on the main display
        self.display_surface.blit(self.minimap_surface, self.minimap_rect)
        pygame.draw.rect(self.display_surface, 'white', self.minimap_rect, 2)  # Border for the minimap