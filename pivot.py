import math
import pygame
from settings import IMG_SCALE
from pygame import Vector2


reference_dict = {}



class SpikeBall:
    
    chain_length = 40 * IMG_SCALE
    
    def __init__(self):
        
        self.pivot = screen_center
        self.angle = 0
        
        offset = Vector2()
        offset.from_polar((self.chain_length,- 90))
        
        self.pos = self.pivot + offset
        
        self.image_orig = reference_dict['Wood_Buckler']
        self.image = self.image_orig
        self.rect = self.image.get_rect(center = self.pos)
        
    def update(self, dt):
        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        
 
        # Calculate the angle based on the mouse position relative to the pivot
        self.angle = (mouse_pos - self.pivot).angle_to(Vector2(1, 0)) - 90
        
        self.image, self.rect = self.rotate_on_pivot()
    
    def draw(self, surface):
        pygame.draw.line(surface, 'darkgray', self.pivot, self.rect.center, width = 3)
        pygame.draw.line(surface, 'black', self.pivot, self.rect.center)
        surface.blit(self.image, self.rect)

    def rotate_on_pivot(self):
        
        surf = pygame.transform.rotate(self.image_orig, self.angle)
        
        offset = self.pivot + (self.pos - self.pivot).rotate(-self.angle)
        rect = surf.get_rect(center = offset)
        
        return surf, rect


class Game:
    def __init__(self):
        pygame.init()

        self.pivot_speed = 0.2
        
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.screen = pygame.display.set_mode(screen_size)
        
        self.load_image('Wood_Buckler', colorkey = 'white')
  
        self.spikeball = SpikeBall()
  
    def load_image(self, image_name, colorkey = None):
        image = pygame.image.load(f'graphics/weapons/wood_buckler/{image_name}.png').convert_alpha()
        reference_dict[image_name] = image
  
    def update(self, dt):
        # Update the spikeball
        self.spikeball.update(dt)

        # Move the pivot based on WASD input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Move up
            self.spikeball.pivot.y -= self.pivot_speed
            self.spikeball.pos.y -= self.pivot_speed
        if keys[pygame.K_s]:  # Move down
            self.spikeball.pivot.y += self.pivot_speed
            self.spikeball.pos.y += self.pivot_speed
        if keys[pygame.K_a]:  # Move left
            self.spikeball.pivot.x -= self.pivot_speed
            self.spikeball.pos.x -= self.pivot_speed
        if keys[pygame.K_d]:  # Move right
            self.spikeball.pivot.x += self.pivot_speed
            self.spikeball.pos.x += self.pivot_speed
    def draw(self, surface):
        
        surface.fill('black')
        self.spikeball.draw(surface)
        
        pygame.display.flip()
        
    def run(self):
        
        self.running = True
        
        while self.running:
            
            dt = self.clock.tick() * .001
            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'FPS: {self.fps}')
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.update(dt)
            self.draw(self.screen)
        
        
if __name__ == '__main__':
    Game().run()