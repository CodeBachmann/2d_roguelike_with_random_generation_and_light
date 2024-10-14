import pygame
import math
import random
from settings import TILE_SIZE

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type, angle=None, velocity=None, 
                 range=1000, movable=False, initial_color=(255, 255, 255), final_color=None, width=30, height=20, speed_modifier=1, 
                 dispersion=0, missile=True, image_path=None, hostile=False):
        

        super().__init__(groups)
        """ TYPES """
        self.sprite_type = 'projectile'
        self.type = type

        """ CALC PARAMETERS"""
        self.angle = angle
        self.velocity = velocity
        self.hostile = hostile
        self.distance_from_the_player = 40

        angle_rad = math.radians(self.angle)
        offset_x = self.distance_from_the_player * math.cos(angle_rad) - width//4
        offset_y = -self.distance_from_the_player * math.sin(angle_rad) + width//4

        self.initial_pos = pygame.math.Vector2(pos[0] + offset_x, pos[1] + offset_y)
        self.pos = self.initial_pos.copy()

        self.range = range
        self.speed_modifier = speed_modifier
        self.dispersion = math.radians(dispersion)
        if self.dispersion != 0:
            self.velocity = self.calculate_dispersed_velocity(velocity)
        self.start_time = pygame.time.get_ticks()

        """ PARAMETERS"""
        self.movable = movable
        self.initial_color = initial_color
        self.final_color = final_color
        self.missile = missile
        self.width = width
        self.height = height

        """ IMAGE """
        if image_path == None:
            self.original_image = self.create_arc(width, height) if self.type == 'arc' else self.create_bar(width, height)

        else:
            self.original_image = pygame.image.load(image_path).convert_alpha()

        self.image = self.original_image

        self.rect = self.image.get_rect()

        self.hitbox = self.rect.inflate(0, -10)


        if not self.movable:
            self.missile = False
            self.lifetime = 0.5

        elif self.missile:
            self.missile_phase = 0
            self.original_speed = self.velocity.length()
            self.current_speed = self.original_speed * 0.2
            self.velocity = self.velocity.normalize() * self.current_speed

        self.update_image()

    def create_arc(self, width, height):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.arc(surface, self.initial_color, (0, 0, width, height * 4), 0, math.pi, 2)
        return surface

    def create_bar(self, width, height):
        surface = pygame.Surface((width, height))
        surface.fill((0, 255, 0))
        return surface

    def update_image(self):
        if self.type == 'arc':
            rotated_image = pygame.transform.rotate(self.original_image,self.angle - 90)

        elif self.type == 'bar':
            rotated_image = pygame.transform.rotate(self.original_image, self.angle )

        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect.inflate(0, -10)

    def update(self):
        if self.missile:
            self.update_missile_speed()
        if self.hostile:
            self.check_collision()
        if self.movable:
            self.pos += self.velocity
            self.update_image()

        

            distance_traveled = (self.pos - self.initial_pos).length()
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
        new_velocity = pygame.math.Vector2(
            speed * math.cos(dispersed_angle),
            speed * math.sin(dispersed_angle)
        )

        return new_velocity
    
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