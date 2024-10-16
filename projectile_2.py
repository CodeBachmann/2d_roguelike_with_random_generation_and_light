import pygame
from pygame.math import Vector2
from settings import IMG_SCALE
class SpikeBall(pygame.sprite.Sprite):
    def __init__(self, groups, screen_center):
        super().__init__(groups)

        self.sprite_type = 'projectile'
        self.chain_length = 40 * IMG_SCALE
    
        
        self.pivot = Vector2(screen_center)
        self.angle = 0
        self.lifetime = 1000
        self.start_time = pygame.time.get_ticks()
        offset = Vector2()
        offset.from_polar((self.chain_length,- 90))
        
        self.pos = self.pivot + offset
        
        self.image_orig = pygame.image.load('graphics/weapons/wood_buckler/Wood_Buckler.png').convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)
        
    def update(self):
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
 
        # Calculate the angle based on the mouse position relative to the pivot
        self.angle = (mouse_pos - self.pivot).angle_to(Vector2(1, 0)) - 90
        
        self.image, self.rect = self.rotate_on_pivot()
        print(self.rect.center)
        print(self.angle)
        print(self.pos)

    def rotate_on_pivot(self):
        
        surf = pygame.transform.rotate(self.image_orig, self.angle)
        
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        rect = surf.get_rect(center = offset)
        
        return surf, rect