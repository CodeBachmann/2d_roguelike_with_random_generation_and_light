import pygame
from pygame.math import Vector2
from settings import projectile_data

# Constants
DEFAULT_DAMAGE = 10
CONTAINER_WIDTH = 20  # Width of the cone (adjust as needed)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprites, visible_sprites, entity_type, rect, player_offset, name="sword", target_pos=None, damage=500, creator_id=None):
        super().__init__(groups)

        self.creator_id = creator_id
        self.sprite_type = 'projectile'
        print(10 * name)
        self.projectile_info = projectile_data[name]
        self.entity_type = entity_type
        self.entity_rect = rect
        self.entity_rect_width, self.entity_rect_height = rect.width, rect.height
        self.obstacle_sprites = obstacle_sprites
        self.visible_sprites = visible_sprites
        self.damage = damage  # Use the provided damage value

        # POSITION AND ANGLE CREATION
        self.pivot = Vector2(self.entity_rect.centerx + self.entity_rect_width / 2, self.entity_rect.centery + self.entity_rect_height / 2)
        self.angle = 0
        self.chain_length = self.projectile_info['chain_length'] // 2
        self.world_offset = player_offset
        offset = Vector2()
        offset.from_polar((self.chain_length, -90))
        self.target_pos = target_pos

        # PARAMETERS
        self.movable = self.projectile_info['movable']
        self.shield = self.projectile_info['shield']
        self.image_orig = self.load_image()  # Load image using a method
        self.range = self.projectile_info['range']
        self.is_animation = self.projectile_info['animation']

        # IMAGE CREATION
        self.pos = self.pivot + offset
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=self.pos)
        self.initial_pos = self.pos
        self.update_image()

        speed = 10 * self.projectile_info.get('speed_modifier', 1)
        direction = Vector2(1, 0).rotate(-self.angle)
        self.velocity = direction * speed

    def load_image(self):
        """Load the projectile image or create a cone if no image is provided."""
        if self.projectile_info['image_path'] != "None":
            return pygame.image.load(self.projectile_info['image_path']).convert()
        else:
            return self.create_cone()

    def update_image(self):
        # Get the mouse position
        direction_pos = pygame.mouse.get_pos() if self.entity_type == 'player' else self.target_pos

        # Calculate the angle based on the mouse position relative to the pivot
        self.angle = (direction_pos - (self.pivot - self.world_offset)).angle_to(Vector2(1, 0))
        print(self.angle)

        self.image, self.rect = self.rotate_on_pivot()
        self.pos = self.pivot + Vector2(self.chain_length, 0).rotate(-self.angle)  # Ensure distance is always chain_length
        self.rect.center = self.pos # Update rect position

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
        surf = pygame.transform.rotate(self.image_orig, self.angle - 90)
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        rect = surf.get_rect(center=offset)
        rect.center = offset

        return surf, rect

    def create_cone(self):
        # Create a cone shape using the projectile's position and angle
        cone_length = self.chain_length  # Length of the cone

        # Calculate the points for the cone shape
        tip = self.pos
        left_point = self.pos + Vector2(-CONTAINER_WIDTH / 2, cone_length).rotate(-self.angle)
        right_point = self.pos + Vector2(CONTAINER_WIDTH / 2, cone_length).rotate(-self.angle)

        # Create a list of points to form the cone
        cone_points = [tip, left_point, right_point]

        # Create a surface to draw the cone on
        cone_surface = pygame.Surface((CONTAINER_WIDTH, cone_length), pygame.SRCALPHA)  # Create a transparent surface
        pygame.draw.polygon(cone_surface, (255, 0, 0), cone_points)  # Draw the cone in red

        return cone_surface

    def collision(self):
        if not self.shield:
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.rect):
                    self.kill()

        for sprite in self.visible_sprites:
            if sprite.sprite_type in ['enemy', 'player'] and sprite.sprite_type != self.entity_type and sprite.hitbox.colliderect(self.rect) and not self.shield:
                sprite.health -= self.damage
                print(sprite.health)
                self.kill()

            elif sprite.sprite_type == 'sprite' and sprite.hitbox.colliderect(self.rect) and self.shield:
                for sprite_defender in self.visible_sprites:
                    if sprite_defender.creator_id == self.creator_id:
                        sprite_defender.shield_block(sprite.damage)
                sprite.kill()


    