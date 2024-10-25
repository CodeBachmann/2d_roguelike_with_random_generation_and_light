#!/usr/bin/python3.4
import pygame, sys, math, random
from typing import Dict
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
        
        # Light Power
        #self.light_color = [v * 0.90 for v in LIGHT_COLOR]
        self.light_color = LIGHT_COLOR
        self.default_light_img = self.create_default_light(40)
        

        self.current_view_radius = 0
        self.current_masked_light = None
        self.max_light_size = 1024  # Maximum size for light surfaces
        self.light_surfaces = {}  # Cache for light surfaces

        #Torches
        self.torch_lights = {}  # Dictionary to store torch lights
        self.torch_flicker_timers = {}  # Dictionary to store flicker timers for each torch
        self.torch_base_radius = 100  # Base radius for torch lights
        self.torch_flicker_speed = 0.15  # Speed of the flicker effect
        self.torch_color_shift_speed = 0.05  # Speed of the color shift effect

        #Player Vision
        self.cone = True
        self.circle = True
        self.cone_light = self.light_box.add_light(lighting.Light([0, 0], 40, self.default_light_img, self.light_color))
        self.circle_light = self.light_box.add_light(lighting.Light([0, 0], 40, self.default_light_img, self.light_color))

        #Generate Walls
        lighting.generate_walls(self.light_box, light_map, TILE_SIZE)

    def create_default_light(self, size):
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 255), (size, size), size)
        return surface
    
    def add_torch(self, x, y):
        torch_id = self.light_box.add_light(lighting.Light([x, y], self.torch_base_radius, self.default_light_img, (255, 165, 0)))  # Start with orange color
        self.torch_lights[torch_id] = (x, y)
        self.torch_flicker_timers[torch_id] = random.uniform(0, 2 * math.pi)  # Random start time for flicker effect

    def update_torch_lights(self):
        for torch_id, (x, y) in self.torch_lights.items():
            torch_light = self.light_box.get_light(torch_id)
            
            # Update flicker timer
            self.torch_flicker_timers[torch_id] += self.torch_flicker_speed
            
            # Calculate radius variation
            radius_variation = math.sin(self.torch_flicker_timers[torch_id]) * 5  # Vary radius by ±10 pixels
            new_radius = self.torch_base_radius + radius_variation
            
            # Calculate color variation (shift between orange and yellow)
            color_shift = (math.sin(self.torch_flicker_timers[torch_id] * self.torch_color_shift_speed) + 1) / 2  # Value between 0 and 1
            red = int(255 * (1 - color_shift) + 255 * color_shift)
            green = int(165 * (1 - color_shift) + 255 * color_shift)
            blue = int(0 * (1 - color_shift) + 0 * color_shift)  # Blue remains 0
            
            # Update torch light
            torch_light.set_size(int(new_radius))
            torch_light.set_color((red, green, blue))
            
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

        if scale_factor < 1:
            scaled_size = (int(size * scale_factor), int(size * scale_factor))
            self.current_masked_light = pygame.transform.scale(self.current_masked_light, scaled_size)

    

    def cast_light(self, player):
        self.offset.x = player.rect.centerx - self.half_width + player.rect.width/2
        self.offset.y = player.rect.centery - self.half_height + player.rect.height/2

        self.offset.x = max(MIN_X_OFFSET, min(self.offset.x, MAX_X_OFFSET - WIDTH))
        self.offset.y = max(MIN_Y_OFFSET, min(self.offset.y, MAX_Y_OFFSET - HEIGHT))


        if player.cone and not self.cone:
            self.cone_light = self.light_box.add_light(lighting.Light([0, 0], 40, self.default_light_img, self.light_color))
            self.cone = True

        elif player.cone:
            # Update cone light
            cone_light = self.light_box.get_light(self.cone_light)
            cone_light.set_color(self.light_color, True)
            cone_light.position = [player.rect.centerx, player.rect.centery]
            cone_light.set_size(player.view_radius)

            # Update the masked light
            self.update_masked_light(player.view_radius, player.angle)
            cone_light.light_img = self.current_masked_light

        elif self.cone:
            self.light_box.delete_light(self.cone_light)
            self.cone = False

        # Update circle light
        circle_light = self.light_box.get_light(self.circle_light)
        circle_light.set_color(self.light_color, True)
        circle_light.position = [player.rect.centerx, player.rect.centery]
        circle_light.set_size(player.view_radius // 5)



        self.offset.y = self.offset.y - 32*IMG_SCALE
        self.offset.x = self.offset.x - 32*IMG_SCALE

        for torch_id, (x, y) in self.torch_lights.items():
            torch_light = self.light_box.get_light(torch_id)
            # Adjust torch position based on player's position and camera offset
            adjusted_x = x + TILE_SIZE // 2
            adjusted_y = y + TILE_SIZE // 2
            torch_light.position = [adjusted_x, adjusted_y]
        
        self.update_torch_lights()  # Add this line to update torch lights


        walls = self.light_box.render(self.display_surface, list(self.offset))

        for wall in walls:
            wall.render(self.display_surface)