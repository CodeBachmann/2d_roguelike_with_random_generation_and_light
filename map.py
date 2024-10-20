import random
from pygame import transform
from settings import *  # Make sure this import works with your project structure
from support import load_images_from_folder

FLOOR = 'Floor'
TOP_WALL = 'Top_Wall'
RIGHT_WALL = 'Right_Wall'
LEFT_WALL = 'Left_Wall'
BOT_LEFT = 'Bot_Left'
BOT_RIGHT = 'Bot_Right'
NULL = 'Null'
BOT_WALL = 'Bot_Wall'

class Map:
    def __init__(self):
        self.width = MAP_SIZE_X
        self.height = MAP_SIZE_Y
        self.tile_size = TILE_SIZE
        self.map_name = 'Dungeon' 
        self.grid_map = self.generate_tile_map()  # New variable to store the grid version
        self.entity_map = self.generate_entity_map()
        self.color_map = self.generate_color_map()
        self.light_map = self.generate_light_map()


    def generate_color_map(self):
        # Cavern dungeon palette
        floor_colors = [
            (100, 80, 60),  # Brown
            (80, 70, 60),   # Dark beige
            (70, 60, 50),   # Darker brown
            (90, 75, 55),   # Light brown
        ]
        wall_colors = [
            (10, 10, 10),   # Dark gray
            (5, 5, 5),   # Gray
            (0, 0, 0),   # Light gray
            (15, 15, 15),   # Darker gray
        ]

        color_map = []
        for row in self.grid_map:
            color_row = []
            for tile in row:
                if tile == 'x':
                    color_row.append(random.choice(wall_colors))
                else:
                    color_row.append(random.choice(floor_colors))
            color_map.append(color_row)

        return color_map

    def load_tiles(self, folder_path):
        tiles = {
            FLOOR: [], TOP_WALL: [], RIGHT_WALL: [], LEFT_WALL: [], BOT_WALL: [],
            BOT_LEFT: [], BOT_RIGHT: [], NULL: []
        }
        
        # Load all images from the folder once
        all_images = load_images_from_folder(folder_path)  # Load all images at once
        
        for image, filename in all_images:  # Unpack the tuple
            for tile_type in tiles.keys():
                if filename.startswith(tile_type):
                    image = transform.scale(image, (self.tile_size, self.tile_size))  # Scale the image
                    tiles[tile_type].append(image)
        
        return tiles

    def generate_tile_map(self):
        # Initialize the map with empty spaces
        tile_map = [['e' for _ in range(self.width)] for _ in range(self.height)]
        
        # Create random rooms
        num_rooms = ROOM_COUNT
        rooms = []
        for _ in range(num_rooms):
            room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            
            # Fill room with floor tiles
            for i in range(y, y + room_height):
                for j in range(x, x + room_width):
                    tile_map[i][j] = ' '
            
            rooms.append((x, y, room_width, room_height))
        
        # Create corridors between rooms
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i + 1]
            
            # Find center points of rooms
            cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
            cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2
            
            # Horizontal corridor
            for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                tile_map[cy1][x] = ' '
            
            # Vertical corridor
            for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                tile_map[y][cx2] = ' '
        
        # Add walls around rooms and corridors
        for y in range(self.height):
            for x in range(self.width):
                if tile_map[y][x] == ' ':
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.height and 0 <= nx < self.width:
                            if tile_map[ny][nx] == 'e':
                                tile_map[ny][nx] = 'x'
        
        return tile_map 

    def generate_entity_map(self):
        entity_map = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        def is_valid_position(x, y):
            if self.grid_map[y][x] != ' ' or entity_map[y][x] != ' ':
                return False
            
            # Check for adjacent 'x' tiles
            top = self.grid_map[y-1][x] if y > 0 else 'x'
            bottom = self.grid_map[y+1][x] if y < self.height - 1 else 'x'
            left = self.grid_map[y][x-1] if x > 0 else 'x'
            right = self.grid_map[y][x+1] if x < self.width - 1 else 'x'
            
            if (top == 'x' and bottom == 'x') or (left == 'x' and right == 'x'):
                return False
            
            return True

        def place_entity(entity_type, count):
            placed = 0
            while placed < count:
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                if is_valid_position(x, y):
                    entity_map[y][x] = entity_type
                    placed += 1

        # Place entities
        place_entity('391', NUM_MELEE)
        place_entity('390', NUM_RANGED)
        place_entity('o', NUM_OBJECT)
        place_entity('t', NUM_TREASURE)
        place_entity('l', NUM_LIGHT)
        
        # Place player
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if is_valid_position(x, y):
                entity_map[y][x] = '394'
                break

        return entity_map
    
    def generate_light_map(self):
        coordinates = []
        for y, row in enumerate(self.grid_map):
            for x, col in enumerate(row):
                if col == 'x':  # Check if the current tile is ' ' (representing 0)
                    coordinates.append([x, y])  # Append the coordinates to the list
        return coordinates