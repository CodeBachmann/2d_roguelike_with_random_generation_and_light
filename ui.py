import pygame
from settings import *

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # Full map setup
        self.map_surface = pygame.Surface((WIDTH, HEIGHT))
        
        # Zoom factor (adjust as needed)
        self.zoom_factor = min(WIDTH / (MAP_SIZE_X * TILE_SIZE), HEIGHT / (MAP_SIZE_Y * TILE_SIZE))
        self.map_tile_size = int(TILE_SIZE * self.zoom_factor)
        
        # Explored tiles
        self.explored_tiles = [[False for _ in range(MAP_SIZE_X)] for _ in range(MAP_SIZE_Y)]

    def display(self, tile_map):
        self.update_explored_area(tile_map)
        self.draw_map(tile_map)

    def update_explored_area(self, tile_map):
        player_tile_x = int(self.player.rect.centerx / TILE_SIZE)
        player_tile_y = int(self.player.rect.centery / TILE_SIZE)
        
        # Mark area around player as explored
        explore_radius = 5  # Adjust this value to change the exploration area
        for y in range(max(0, player_tile_y - explore_radius), min(MAP_SIZE_Y, player_tile_y + explore_radius + 1)):
            for x in range(max(0, player_tile_x - explore_radius), min(MAP_SIZE_X, player_tile_x + explore_radius + 1)):
                self.explored_tiles[y][x] = True

    def draw_map(self, tile_map):
        self.map_surface.fill('black')
        
        for y in range(MAP_SIZE_Y):
            for x in range(MAP_SIZE_X):
                map_x = x * self.map_tile_size
                map_y = y * self.map_tile_size
                
                if self.explored_tiles[y][x]:
                    if tile_map[y][x] == 'x':
                        color = 'darkgray'
                    else:
                        color = 'lightgray'
                else:
                    color = 'black'
                
                pygame.draw.rect(self.map_surface, color, 
                                 (map_x, map_y, self.map_tile_size * SCREEN_SCALE, self.map_tile_size * SCREEN_SCALE))

        # Draw player position
        player_map_x = int(self.player.rect.centerx / TILE_SIZE * self.map_tile_size)
        player_map_y = int(self.player.rect.centery / TILE_SIZE * self.map_tile_size)
        pygame.draw.circle(self.map_surface, 'red', (player_map_x, player_map_y), 
                           max(3, int(5 * self.zoom_factor)))

        # Draw the map on the main display
        self.display_surface.blit(self.map_surface, (0, 0))

    def draw_stats(self):
        # Draw 3 Bars RED for player Health, Green for Stamina, Blue for Mana
        stats_bar_lenght = 360 * IMG_SCALE 
        stats_bar_height = 21 * IMG_SCALE  

        # Calculate the health, stamina, and mana ratios
        health_ratio = self.player.actual_health / self.player.max_health
        stamina_ratio = self.player.actual_stamina / self.player.max_stamina
        mana_ratio = self.player.actual_mana / self.player.max_mana

        # Draw health bar
        pygame.draw.rect(self.display_surface, 'red', (10, 10, stats_bar_lenght * health_ratio, stats_bar_height))
        # Draw health label
        health_text = f"{int(self.player.actual_health)}/{self.player.max_health}"
        health_label = pygame.font.Font(None, 12).render(health_text, True, 'white')
        self.display_surface.blit(health_label, (50, 10))

        # Draw mana bar
        pygame.draw.rect(self.display_surface, 'blue', (10, 20, stats_bar_lenght * mana_ratio, stats_bar_height))
        # Draw mana label
        mana_text = f"{int(self.player.actual_mana)}/{self.player.max_mana}"
        mana_label = pygame.font.Font(None, 12).render(mana_text, True, 'white')
        self.display_surface.blit(mana_label, (50, 20))

        # Draw stamina bar
        pygame.draw.rect(self.display_surface, 'green', (10, 30, stats_bar_lenght * stamina_ratio, stats_bar_height))
        # Draw stamina label
        stamina_text = f"{int(self.player.actual_stamina)}/{self.player.max_stamina}"
        stamina_label = pygame.font.Font(None, 12).render(stamina_text, True, 'white')
        self.display_surface.blit(stamina_label, (50, 30))


    def draw_stats(self):
        # Draw 3 Bars RED for player Health, Green for Stamina, Blue for Mana
        stats_bar_lenght = 360 * IMG_SCALE 
        stats_bar_height = 21 * IMG_SCALE  

        # Calculate the health, stamina, and mana ratios
        health_ratio = self.player.actual_health / self.player.max_health
        stamina_ratio = self.player.actual_stamina / self.player.max_stamina
        mana_ratio = self.player.actual_mana / self.player.max_mana

        # Draw health bar
        pygame.draw.rect(self.display_surface, 'red', (10, 10, stats_bar_lenght * health_ratio, stats_bar_height))
        # Draw health label
        health_text = f"{int(self.player.actual_health)}/{self.player.max_health}"
        health_label = pygame.font.Font(None, 12).render(health_text, True, 'white')
        self.display_surface.blit(health_label, (50, 10))

        # Draw mana bar
        pygame.draw.rect(self.display_surface, 'blue', (10, 20, stats_bar_lenght * mana_ratio, stats_bar_height))
        # Draw mana label
        mana_text = f"{int(self.player.actual_mana)}/{self.player.max_mana}"
        mana_label = pygame.font.Font(None, 12).render(mana_text, True, 'white')
        self.display_surface.blit(mana_label, (50, 20))

        # Draw stamina bar
        pygame.draw.rect(self.display_surface, 'green', (10, 30, stats_bar_lenght * stamina_ratio, stats_bar_height))
        # Draw stamina label
        stamina_text = f"{int(self.player.actual_stamina)}/{self.player.max_stamina}"
        stamina_label = pygame.font.Font(None, 12).render(stamina_text, True, 'white')
        self.display_surface.blit(stamina_label, (50, 30))
        
    def draw_stats_inv(self):
        # Bar dimensions
        stats_bar_length = 360 * IMG_SCALE
        stats_bar_height = 28 * IMG_SCALE
        bar_start_y = 100 

        # Create a list of all player stats and their actual values

        stats = {
            "Health": (self.player.actual_health, self.player.max_health, 'red'),
            "Mana": (self.player.actual_mana, self.player.max_mana, 'blue'),
            "Stamina": (self.player.actual_stamina, self.player.max_stamina, 'green'),
            "Protection": (self.player.actual_prot, self.player.max_prot, 'purple'),
            "Speed": (self.player.actual_speed // IMG_SCALE, self.player.max_speed // IMG_SCALE, 'purple'),
            "Wisdom": (self.player.actual_wisdom, self.player.max_wisdom, 'purple'),
            "Dexterity": (self.player.actual_dexterity, self.player.max_dexterity, 'purple'),
            "Strength": (self.player.actual_strength, self.player.max_strength, 'purple'),
            "Endurance": (self.player.actual_endurance, self.player.max_endurance, 'purple'),
            "Intelligence": (self.player.actual_intelligence, self.player.max_intelligence, 'purple'),
            "Vigor": (self.player.actual_vigor, self.player.max_vigor, 'purple'),
            "Faith": (self.player.actual_faith, self.player.max_faith, 'purple'),
        }

        # Draw each stat bar
        for i, (stat_name, (actual, max_value, color)) in enumerate(stats.items()):
            ratio = actual / max_value if max_value > 0 else 0  # Prevent division by zero

            # Draw the stat bar
            pygame.draw.rect(self.display_surface, color, (10, bar_start_y + i * (stats_bar_height + 5), stats_bar_length * ratio, stats_bar_height))
            
            # Draw the label
            stat_text = f"{stat_name}: {int(actual)}/{int(max_value)}"
            stat_label = pygame.font.Font(None, 12).render(stat_text, True, 'white')
            self.display_surface.blit(stat_label, (50, bar_start_y + i * (stats_bar_height + 5)))

