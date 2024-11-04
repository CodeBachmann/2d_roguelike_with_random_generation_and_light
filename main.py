import pygame, sys
from settings import WIDTH, HEIGHT, MOUSE_BUTTONS, IMG_SCALE, FULLSCREEN
from level import Level

from debug import debug

class Game:
    def __init__(self):
        
        pygame.init()
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.SCALED
            
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.mouse_buttons = MOUSE_BUTTONS

        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_buttons[event.button - 1] = True

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_buttons[event.button - 1] = False

            self.screen.fill("black")
            self.level.run(self.mouse_buttons)

            fps = self.clock.get_fps()
            debug(f'FPS: {fps:.2f}', x=self.screen.get_width() -180*IMG_SCALE, y=10*IMG_SCALE)

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
