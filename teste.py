import pygame
import random

#screen ratios
screen_width = 1920
screen_height = 1080
fps = 60
fps_timer =  pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))

#colours
player_colour = (0, 134, 179)
main_enemy_colour = (255, 0, 0)
black = 000000
pygame.cursors.ball

#enemies
enemies_list = []

#timer

#Player
class Player:

    def __init__(self):
        self.x = screen_width / 2
        self.y = screen_height / 2
        self.width = 50
        self.height = 50

        cursor = pygame.image.load("graphics\\weapons\\sword\\full.png")
        new_cursor = pygame.transform.scale(cursor, (16,16))
        self.cursor = new_cursor

        self.health = 8

    def draw_player(self, mouse_pos):
        rect_properties =  pygame.Rect([mouse_pos[0] - 25 + 8, mouse_pos[1] - 25 + 8, self.width, self.height])
        pygame.draw.rect(screen, player_colour, rect_properties)
    
    def player_cursor(self):
        pygame.mouse.set_visible(False)
        cursor = pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        screen.blit(self.cursor, mouse_pos)


class Enemy():
    
    def __init__(self):
        self.width = 50
        self.height = 50

        self.xval = random.randint(0, 1920)
        self.yval = random.randint(0,1080)


        self.rect = pygame.Rect(self.xval, self.yval, self.width, self.height)
  
    def draw_enemy(self, screen):
        pygame.draw.rect(screen, main_enemy_colour, self.rect)

    def create_enemy_list(self):
        global enemies_list

    def create_enemy(self):
        new_enemy = Enemy()
        enemies_list.append(new_enemy)

    def spawn_enemy(self):
        pass

player = Player()
enemy = Enemy()


game_loop = True
last_spawn_time = pygame.time.get_ticks()
enemy.create_enemy_list()
spawn_duration = 2000



while game_loop == True:
    screen.fill(black)

    #mouse
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
      

    if current_time - last_spawn_time >= spawn_duration:
        enemy.create_enemy()  # Spawn a new enemy
        last_spawn_time = current_time  # Reset the timer    

    for new_enemy in enemies_list:
        new_enemy.draw_enemy(screen)

    
    #actions
    player.draw_player(mouse_pos)
    player.player_cursor()

    
    
    pygame.display.update()
    fps_timer.tick(fps)
    


pygame.quit()
