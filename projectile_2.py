import pygame
from pygame.math import Vector2
from settings import IMG_SCALE, projectile_data
class SpikeBall(pygame.sprite.Sprite):
    def __init__(self, groups, screen_center, offset, name):
        super().__init__(groups)

        self.sprite_type = 'projectile'
        self.projectile_info = projectile_data[name]

        # POSITION AND ANGLE CREATION
        self.pivot = Vector2(screen_center)
        self.angle = 0
        self.chain_length = 10
        self.world_offset = offset
        offset = Vector2()
        offset.from_polar((self.chain_length, 0))
        self.velocity = Vector2()

        # PARAMETERS
        self.movable = self.projectile_info['movable']
        self.shield = self.projectile_info['shield']
        self.initial_color = self.projectile_info['initial_color']
        self.final_color = self.projectile_info['final_color']
        self.missile = self.projectile_info['missile']
        self.image_path = self.projectile_info['image_path']
        self.range = self.projectile_info['range']
        
        # IMAGE CREATION
        self.pos = self.pivot + offset
        self.image_orig = pygame.image.load(self.projectile_info['image_path']).convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)
        self.update_image()
        
    def update_image(self):
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
 
        # Calculate the angle based on the mouse position relative to the pivot
        self.angle = (mouse_pos - (self.pivot - self.world_offset)).angle_to(Vector2(1, 0))
        
        #self.image, self.rect = self.rotate_on_pivot()
        self.pos = self.pivot + Vector2(self.chain_length, 0).rotate(-self.angle)  # Ensure distance is always chain_length
        self.rect.center = self.pos  # Update rect position

    def update(self):
        if self.movable:
            self.pos += self.velocity
        if self.shield:
            self.update_image()


    def rotate_on_pivot(self):
        
        surf = pygame.transform.rotate(self.image_orig, self.angle - 90)
        
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        rect = surf.get_rect(center = offset)

        rect.center = offset
        
        return surf, rect