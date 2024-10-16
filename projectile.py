import pygame
import math
import random
from settings import TILE_SIZE, projectile_data, IMG_SCALE
from debug import debug

class Projectile(pygame.sprite.Sprite):
    def __init__(self, entity, groups, angle=None, velocity=None, hostile=False, name=None):
        

        super().__init__(groups)
        """ TYPES """
        self.projectile_info = projectile_data[name]
        self.sprite_type = 'projectile'
        self.type = self.projectile_info['type']

        """ CALC PARAMETERS"""
        self.angle = angle
        self.velocity = velocity
        self.hostile = hostile
        self.entity = entity

        """ PARAMETERS"""
        self.movable = self.projectile_info['movable']
        self.shield = self.projectile_info['shield']
        self.initial_color = self.projectile_info['initial_color']
        self.final_color = self.projectile_info['final_color']
        self.missile = self.projectile_info['missile']
        self.width = self.projectile_info['width']
        self.height = self.projectile_info['height']
        self.image_path = self.projectile_info['image_path']
        self.range = self.projectile_info['range']
        """ IMAGE """
        
        
        if self.image_path is None:
            self.image = self.create_arc(self.width, self.height) if self.type == 'arc' else self.create_bar(self.width, self.height)
        else:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * IMG_SCALE, self.image.get_height() * IMG_SCALE))
            self.width = self.image.get_width()
            self.height = self.image.get_height()

        self.original_image = self.image.copy()  # Keep a copy of the original image for rotation
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Center rect at spawn position
        self.pos = pygame.math.Vector2(self.rect.center)  # The original center position/pivot point.
        self.offset = pygame.math.Vector2(50, 0)  # Shift the sprite 50 px to the right.
        self.angle = angle  # Initialize angle


        if not self.movable:
            self.missile = False
            self.lifetime = 0.5
        
        if self.shield:
            self.lifetime = 0.01

        elif self.missile:
            self.missile_phase = 0
            self.original_speed = self.velocity.length()
            self.current_speed = self.original_speed * 0.2
            self.velocity = self.velocity.normalize() * self.current_speed

        self.start_time = pygame.time.get_ticks()
        self.draw_debug

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos+offset_rotated)



    def update(self):
        if self.missile:
            self.update_missile_speed()
        if self.hostile:
            self.check_collision()
        
        self.move()
        
        current_distance = self.calculate_distance_from_entity()
        print(f"Initial distance: {self.initial_distance:.2f}, Current distance: {current_distance:.2f}")
        
        if self.movable:
            distance_traveled = pygame.math.Vector2(self.x, self.y).distance_to(self.initial_pos)
            if distance_traveled >= self.range:
                self.kill()
        else:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0
            if elapsed_time >= self.lifetime:
                self.kill()





    def calculate_dispersed_velocity(self, original_velocity):
        # Calculate the angle of the original velocity
        angle = math.atan2(original_velocity.y, original_velocity.x)

        # Apply dispersion
        dispersed_angle = angle + random.uniform(-self.dispersion, self.dispersion)

        # Calculate the new velocity vector
        speed = original_velocity.length() * self.speed_modifier
        return pygame.math.Vector2(
            speed * math.cos(dispersed_angle), speed * math.sin(dispersed_angle)
        )
    
    def update_missile_speed(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0  # Convert to seconds
        if self.missile_phase == 0 and elapsed_time >= 0.1:
            # After 0.3 seconds, reduce to 5% of original speed
            self.current_speed = self.original_speed * 0.1
            self.missile_phase = 1
        elif self.missile_phase == 1 and elapsed_time >= 1.2:
            # After 5 seconds total, increase to 5x original speed
            self.current_speed = self.original_speed * 5
            self.missile_phase = 2

        # Update velocity magnitude while keeping direction
        self.velocity = self.velocity.normalize() * self.current_speed


    def draw_debug(self, screen):
        # Draw a dot at the projectile's position
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 3)
        
        # Draw the rect outline
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1)
        
        # Draw a line from the projectile's position in the direction it's facing
        end_point = self.pos + pygame.math.Vector2(30, 0).rotate(-self.angle)
        pygame.draw.line(screen, (0, 0, 255), self.pos, end_point, 2)