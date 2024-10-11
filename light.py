#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys, math
import lighting
from settings import light_map, LIGHT_COLOR, TILE_SIZE, WIDTH, HEIGHT, MIN_X_OFFSET, MIN_Y_OFFSET, MAX_X_OFFSET, MAX_Y_OFFSET

class Light():
    def __init__(self):
        self.offset = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.light_img = pygame.image.load('light.png').convert()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.light_box = lighting.LightBox((WIDTH, HEIGHT))
        
        self.light = self.light_box.add_light(lighting.Light([0, 0], 40, self.light_img, (100, 50, 255)))
        lighting.generate_walls(self.light_box, light_map, TILE_SIZE)

    def cast_light(self, player):
    # Update Lights ------------------------------------------ #
        # True argument overrides light alpha for faster updates
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))


        self.light_box.get_light(self.light).set_color(LIGHT_COLOR, True)
        self.light_box.get_light(self.light).position = [player.rect.centerx, player.rect.centery] 
        self.light_box.get_light(self.light).set_size(300)

        self.offset.y = self.offset.y - 30
        self.offset.x = self.offset.x - 30
        visible_walls =  self.light_box.render(self.display_surface, list(self.offset))

        # # wall lines
        for wall in visible_walls:
            wall.render(self.display_surface)
        
