import pygame
from pygame.math import Vector2
from settings import IMG_SCALE, projectile_data
class Projectile(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites, visible_sprites, entity_type, rect, player_offset, name, target_pos = None, damage = 10):
        super().__init__(groups)

        self.sprite_type = 'projectile'
        self.projectile_info = projectile_data[name]
        self.entity_type = entity_type
        self.entity_rect = rect
        self.entity_rect_width, self.entity_rect_height = rect.width, rect.height
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.damage = damage

        # POSITION AND ANGLE CREATION
        self.pivot = Vector2(self.entity_rect.centerx + self.entity_rect_width/2, self.entity_rect.centery + self.entity_rect_height/2)
        self.angle = 0
        self.chain_length = self.projectile_info['chain_length']
        self.world_offset = player_offset
        offset = Vector2()
        offset.from_polar((self.chain_length, -90))
        self.target_pos = target_pos

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
        if self.shield:
            self.image_orig = pygame.transform.scale(self.image_orig, (self.projectile_info['width'], self.projectile_info['height']))
        else:
            self.image_orig = pygame.transform.scale(self.image_orig, (self.image_orig.get_width() * IMG_SCALE, self.image_orig.get_height() * IMG_SCALE))

        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)
        self.initial_pos = self.pos
        self.update_image()

        speed = 10 * self.projectile_info.get('speed_modifier', 1)
        direction = Vector2(1, 0).rotate(-self.angle)
        self.velocity = direction * speed
        
    def update_image(self):
        # Get the mouse position
        if self.entity_type == 'player':
            mouse_pos = pygame.mouse.get_pos()
        else:
            mouse_pos = self.target_pos
 
        # Calculate the angle based on the mouse position relative to the pivot
        self.angle = (mouse_pos - (self.pivot - self.world_offset)).angle_to(Vector2(1, 0))
        
        self.image, self.rect = self.rotate_on_pivot()
        self.pos = self.pivot + Vector2(self.chain_length, 0).rotate(-self.angle )  # Ensure distance is always chain_length
        self.rect.center = self.pos  # Update rect position

    def update(self):
        if self.movable:
            self.pos += self.velocity
            self.rect.center = self.pos
            if self.pos.distance_to(self.initial_pos) > self.range:
                self.kill()
                
        if self.shield:
            self.update_image()
        
        self.collision()


    def rotate_on_pivot(self):
        print(self.angle)
        surf = pygame.transform.rotate(self.image_orig, self.angle - 90)
        
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        rect = surf.get_rect(center = offset)

        rect.center = offset
        
        return surf, rect
    
    def collision(self):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.rect):
                self.kill()

        for sprite in self.visible_sprites:
            if sprite.sprite_type == 'enemy':
                if sprite.hitbox.colliderect(self.rect):
                    sprite.health -= self.damage
                    self.kill()
