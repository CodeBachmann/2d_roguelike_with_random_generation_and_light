#!/usr/bin/python3.4
import pygame, sys, math
import lighting
from settings import light_map, IMG_SCALE, LIGHT_COLOR, TILE_SIZE, WIDTH, HEIGHT, MIN_X_OFFSET, MIN_Y_OFFSET, MAX_X_OFFSET, MAX_Y_OFFSET

class Light():
    def __init__(self):
        self.sprite_type = 'light'
        self.offset = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.light_box = lighting.LightBox((WIDTH, HEIGHT), pygame.BLEND_RGBA_MULT)
        
        self.light_color = [v * 0.90 for v in LIGHT_COLOR]
        # Light Power
        default_light_img = self.create_default_light(40)
        self.cone_light = self.light_box.add_light(lighting.Light([0, 0], 40, default_light_img, self.light_color))
        self.circle_light = self.light_box.add_light(lighting.Light([0, 0], 40, default_light_img, self.light_color))
        lighting.generate_walls(self.light_box, light_map, TILE_SIZE)

        self.current_view_radius = 0
        self.current_masked_light = None
        self.max_light_size = 1024  # Maximum size for light surfaces
        self.light_surfaces = {}  # Cache for light surfaces

    def create_default_light(self, size):
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 255), (size, size), size)
        return surface
    
    def get_circle_light(self, size):
        if size not in self.light_surfaces:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 255, 255), (size // 2, size // 2), size // 2)
            self.light_surfaces[size] = surface
        return self.light_surfaces[size]

    def get_cone_mask(self, size, angle=90):
        key = (size, angle)
        if key not in self.light_surfaces:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.arc(surface, (255, 255, 255, 255), (0, 0, size, size), 
                            math.radians(-angle/2), math.radians(angle/2), size//2)
            self.light_surfaces[key] = surface
        return self.light_surfaces[key]

    def update_masked_light(self, view_radius, angle):
        size = min(view_radius * 2, self.max_light_size)
        scale_factor = size / (view_radius * 2)

        if self.current_view_radius != view_radius:
            self.current_view_radius = view_radius
            circle_light = self.get_circle_light(size)
            cone_mask = self.get_cone_mask(size)
            
            rotated_mask = pygame.transform.rotate(cone_mask, angle)
            self.current_masked_light = circle_light.copy()
            
            mask_rect = rotated_mask.get_rect(center=(size // 2, size // 2))
            self.current_masked_light.blit(rotated_mask, mask_rect.topleft, special_flags=pygame.BLEND_RGBA_MULT)
        else:
            circle_light = self.get_circle_light(size)
            cone_mask = self.get_cone_mask(size)
            
            rotated_mask = pygame.transform.rotate(cone_mask, angle)
            self.current_masked_light = circle_light.copy()
            
            mask_rect = rotated_mask.get_rect(center=(size // 2, size // 2))
            self.current_masked_light.blit(rotated_mask, mask_rect.topleft, special_flags=pygame.BLEND_RGBA_MULT)

        if scale_factor < 1:
            scaled_size = (int(size * scale_factor), int(size * scale_factor))
            self.current_masked_light = pygame.transform.scale(self.current_masked_light, scaled_size)

    def cast_light(self, player):
        self.offset.x = player.rect.centerx - self.half_width + player.rect.width/2
        self.offset.y = player.rect.centery - self.half_height + player.rect.height/2

        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))

        # Update cone light
        cone_light = self.light_box.get_light(self.cone_light)
        cone_light.set_color(self.light_color, True)
        cone_light.position = [player.rect.centerx, player.rect.centery]
        cone_light.set_size(player.view_radius)

        # Update the masked light
        self.update_masked_light(player.view_radius, player.angle)
        cone_light.light_img = self.current_masked_light

        # Update circle light
        circle_light = self.light_box.get_light(self.circle_light)
        circle_light.set_color(self.light_color, True)
        circle_light.position = [player.rect.centerx, player.rect.centery]
        circle_light.set_size(player.view_radius // 5)

        self.offset.y = self.offset.y - 32*IMG_SCALE
        self.offset.x = self.offset.x - 32*IMG_SCALE

        walls = self.light_box.render(self.display_surface, list(self.offset))

        for wall in walls:
            wall.render(self.display_surface)