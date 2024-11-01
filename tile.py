import pygame
from settings import *
from entity import Entity

class Tile(Entity):
    def __init__(self, pos, groups, img_path=None, color=None, sprite_type=None, spritesheet=None, length=None):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.status = 'idle'
        self.animations = {'idle':[]}
        
        if img_path:
            self.image = pygame.image.load(img_path).convert()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        elif spritesheet:
            self.import_assets(spritesheet, length)
            self.image = self.animations[self.status][0]
        elif color:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(color)
        else:
            raise ValueError("Either img_path or color must be provided")
        
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, 0)

    def import_assets(self, path, length):
        self.animations = {'idle':[]}
        for image in range(length):
            full_path = path + '/' + str(image + 1) + '.png'
            img = pygame.image.load(full_path)
            img = pygame.transform.scale(img, (int(img.get_width() * IMG_SCALE), int(img.get_height() * IMG_SCALE)))
            self.animations[self.status].append(img)

    def update(self):
        if self.sprite_type == 'torch':
            self.animate()
