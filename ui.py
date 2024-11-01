import pygame
from settings import *

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # Full map setup
        self.map_surface = pygame.Surface((WIDTH, HEIGHT))
        self.bk_menu_image = pygame.transform.scale(pygame.image.load(r'graphics\stages\island.png'), (WIDTH, HEIGHT))
        
        # Zoom factor (adjust as needed)
        self.zoom_factor = min(WIDTH / (MAP_SIZE_X * TILE_SIZE), HEIGHT / (MAP_SIZE_Y * TILE_SIZE))
        self.map_tile_size = int(TILE_SIZE * self.zoom_factor)
        
        # Explored tiles
        self.explored_tiles = [[False for _ in range(MAP_SIZE_X)] for _ in range(MAP_SIZE_Y)]

        self.character_icons = {
            'Mage': pygame.transform.scale(pygame.image.load('graphics/icons/char_portrait/Mage.jpg'), (50 * IMG_SCALE, 50 * IMG_SCALE)),
            'Fighter': pygame.transform.scale(pygame.image.load('graphics/icons/char_portrait/Fighter.jpg'), (50 * IMG_SCALE, 50 * IMG_SCALE)),
            'Rogue': pygame.transform.scale(pygame.image.load('graphics/icons/char_portrait/Rogue.jpg'), (50 * IMG_SCALE, 50 * IMG_SCALE)),
            'Priest': pygame.transform.scale(pygame.image.load('graphics/icons/char_portrait/Priest.jpg'), (50 * IMG_SCALE, 50 * IMG_SCALE)),
        }

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
        stats_bar_lenght = 180 * IMG_SCALE 
        stats_bar_height = 21 * IMG_SCALE  

        # Calculate the health, stamina, and mana ratios
        health_ratio = self.player.actual_health / self.player.max_health
        stamina_ratio = self.player.actual_stamina / self.player.max_stamina
        mana_ratio = self.player.actual_mana / self.player.max_mana

        # Draw health bar
        pygame.draw.rect(self.display_surface, 'red', (10 * IMG_SCALE, 10 * IMG_SCALE, stats_bar_lenght * health_ratio, stats_bar_height))
        # Draw health label
        health_text = f"{int(self.player.actual_health)}/{self.player.max_health}"
        health_label = pygame.font.Font(None, 12).render(health_text, True, 'white')
        self.display_surface.blit(health_label, (50 * IMG_SCALE, 10 * IMG_SCALE))

        # Draw mana bar
        pygame.draw.rect(self.display_surface, 'blue', (10 * IMG_SCALE, 20 * IMG_SCALE, stats_bar_lenght * mana_ratio, stats_bar_height))
        # Draw mana label
        mana_text = f"{int(self.player.actual_mana)}/{self.player.max_mana}"
        mana_label = pygame.font.Font(None, 12).render(mana_text, True, 'white')
        self.display_surface.blit(mana_label, (50 * IMG_SCALE, 20 * IMG_SCALE   ))

        # Draw stamina bar
        pygame.draw.rect(self.display_surface, 'green', (10 * IMG_SCALE, 30 * IMG_SCALE, stats_bar_lenght * stamina_ratio, stats_bar_height))
        # Draw stamina label
        stamina_text = f"{int(self.player.actual_stamina)}/{self.player.max_stamina}"
        stamina_label = pygame.font.Font(None, 12).render(stamina_text, True, 'white')
        self.display_surface.blit(stamina_label, (50 * IMG_SCALE, 30 * IMG_SCALE))
        
    def draw_stats_inv(self):
        # Bar dimensions
        stats_bar_length = 180 * IMG_SCALE
        stats_bar_height = 21 * IMG_SCALE
        bar_start_y = 100 * IMG_SCALE

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
            pygame.draw.rect(self.display_surface, color, (10 * IMG_SCALE, bar_start_y + i * (stats_bar_height + 5), stats_bar_length * ratio, stats_bar_height))
            
            # Draw the label
            stat_text = f"{stat_name}: {int(actual)}/{int(max_value)}"
            stat_label = pygame.font.Font(None, 12).render(stat_text, True, 'white')
            self.display_surface.blit(stat_label, (50 * IMG_SCALE, bar_start_y + i * (stats_bar_height + 5)))


    def draw_game_menu(self, recruitable_characters, rooster_characters, game_stage):
        # Draw recruitable characters grid (bottom left)
        grid_start_x = 10 * IMG_SCALE
        grid_start_y = HEIGHT - 100 * IMG_SCALE  # Adjust as needed
        self.display_surface.blit(self.bk_menu_image, (0,0))
        for i, character in enumerate(recruitable_characters):
            if character_image := self.character_icons.get(character.player_class):
                # Calculate position
                pos_x = grid_start_x + (i % 5) * (50 * IMG_SCALE + 10 * IMG_SCALE)
                pos_y = grid_start_y + (i // 5) * (50 * IMG_SCALE + 10 * IMG_SCALE)
                self.display_surface.blit(character_image, (pos_x, pos_y))

                # Check for mouse click
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if pos_x <= mouse_pos[0] <= pos_x + 50 and pos_y <= mouse_pos[1] <= pos_y + 50:
                        self.transfer_character(character, recruitable_characters, rooster_characters)

        # Draw rooster characters grid (top right)
        grid_start_x_rooster = WIDTH - 200 * IMG_SCALE  # Adjust as needed
        grid_start_y_rooster = 10 * IMG_SCALE  # Adjust as needed

        for i, character in enumerate(rooster_characters):
            if character_image := self.character_icons.get(character.player_class):
                self.display_surface.blit(character_image, (grid_start_x_rooster + (i % 5) * (50 * IMG_SCALE + 10 * IMG_SCALE), grid_start_y_rooster + (i // 5) * (50 * IMG_SCALE + 10 * IMG_SCALE)))
        
        game_stage = self.draw_start_button("Map", game_stage)

        return game_stage
    

    def transfer_character(self, character, recruitable_characters, rooster_characters):
        # Remove character from recruitable list and add to rooster list
        recruitable_characters.remove(character)
        rooster_characters.append(character)

    def draw_map_stage(self, selected_character, rooster_characters, game_stage):
        # Draw selected character portrait (top right)
        grid_start_x = WIDTH - 200 * IMG_SCALE  # Adjust as needed
        grid_start_y = 10 * IMG_SCALE  # Adjust as needed

        if selected_character:
            if character_image := self.character_icons.get(
                selected_character[0].player_class
            ):
                self.display_surface.blit(character_image, (grid_start_x, grid_start_y))

        for i, character in enumerate(rooster_characters):
            if character_image := self.character_icons.get(character.player_class):
                pos_x = grid_start_x + (i % 5) * (50 * IMG_SCALE + 10 * IMG_SCALE)
                pos_y = grid_start_y + (i // 5) * (50 * IMG_SCALE + 10 * IMG_SCALE)
                self.display_surface.blit(character_image, (pos_x, pos_y))

                # Check for mouse click
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if pos_x <= mouse_pos[0] <= pos_x + 50 * IMG_SCALE and pos_y <= mouse_pos[1] <= pos_y + 50 * IMG_SCALE:
                        if selected_character:  # Check if selected_character is not empty
                            # Switch places of selected_character and the clicked character
                            rooster_characters.remove(character)
                            rooster_characters.append(selected_character[0])
                            selected_character.remove(selected_character[0])
                            selected_character.append(character)  # Update selected_character to the clicked character
                        else:
                            self.transfer_character(character, rooster_characters, selected_character)  # Return the selected character

        game_stage = self.draw_start_button("Load", game_stage)

        return game_stage  # Return the current game stage if no character is selected


    def draw_start_button(self, next_stage, actual_stage):

        button_width = 60 * IMG_SCALE
        button_height = 30 * IMG_SCALE
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT - 200 * IMG_SCALE  # Adjust as needed
        button_color = 'blue'
        pygame.draw.rect(self.display_surface, button_color, (button_x, button_y, button_width, button_height))

        # Draw button text
        font = pygame.font.Font(None, int(36 * IMG_SCALE))
        button_text = font.render("Change State", True, 'white')
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.display_surface.blit(button_text, text_rect)

        # Check for button click
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                return next_stage
        
        return actual_stage