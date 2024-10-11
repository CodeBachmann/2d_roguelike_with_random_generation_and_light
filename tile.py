import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, img_path=None, color=None):
        super().__init__(groups)

        self.sprite_type = "tile"
        
        if img_path:
            self.image = pygame.image.load(img_path).convert_alpha()
        elif color:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(color)
        else:
            raise ValueError("Either img_path or color must be provided")
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, HITBOX_OFFSET['object'])