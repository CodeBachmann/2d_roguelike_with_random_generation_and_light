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
        # Initialize map with non-walkable tiles ('x')
        game_map = [['x' for _ in range(MAP_SIZE_X)] for _ in range(MAP_SIZE_Y)]

        rooms = []

        # Function to carve a room
        def carve_room(x1, y1, x2, y2):
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    game_map[y][x] = ' '

        def carve_horizontal_corridor(x1, x2, y):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                # Randomize the corridor width (1 to 3 tiles)
                width = random.randint(1, 3)
                # Randomize the vertical position within the width
                offset = random.randint(0, width - 1)
                
                for i in range(width):
                    current_y = y - offset + i
                    if 0 <= current_y < MAP_SIZE_Y:
                        game_map[current_y][x] = ' '
                
                # Occasionally add some randomness to the path
                if random.random() < 0.2:  # 20% chance to shift
                    y += random.choice([-1, 0, 1])
                    y = max(1, min(y, MAP_SIZE_Y - 2))  # Keep within bounds

        def carve_vertical_corridor(y1, y2, x):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                # Randomize the corridor width (1 to 3 tiles)
                width = random.randint(1, 3)
                # Randomize the horizontal position within the width
                offset = random.randint(0, width - 1)
                
                for i in range(width):
                    current_x = x - offset + i
                    if 0 <= current_x < MAP_SIZE_X:
                        game_map[y][current_x] = ' '
                
                # Occasionally add some randomness to the path
                if random.random() < 0.2:  # 20% chance to shift
                    x += random.choice([-1, 0, 1])
                    x = max(1, min(x, MAP_SIZE_X - 2))  # Keep within bounds

        # Create random rooms
        for _ in range(ROOM_COUNT):
            room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)
            room = (room_x, room_y, room_x + room_width, room_y + room_height)
            
            # Carve the room
            carve_room(*room)
            rooms.append(room)

        # Connect the rooms with corridors
        for i in range(1, len(rooms)):
            x1, y1, _, _ = rooms[i - 1]
            x2, y2, _, _ = rooms[i]

            # Randomly decide whether to do horizontal or vertical first
            if random.choice([True, False]):
                carve_horizontal_corridor(x1, x2, y1)
                carve_vertical_corridor(y1, y2, x2)
            else:
                carve_vertical_corridor(y1, y2, x1)
                carve_horizontal_corridor(x1, x2, y2)

        # Optional: add a random walk to add more paths
        def random_walk(steps):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Down, Up, Right, Left
            x, y = random.randint(1, MAP_SIZE_X - 2), random.randint(1, MAP_SIZE_Y - 2)

            for _ in range(steps):
                direction = random.choice(directions)
                new_x, new_y = x + direction[0], y + direction[1]

                if 1 <= new_x < MAP_SIZE_X - 1 and 1 <= new_y < MAP_SIZE_Y - 1:
                    game_map[new_y][new_x] = ' '
                    x, y = new_x, new_y

        random_walk((MAP_SIZE_X * MAP_SIZE_Y) // 10)

        for x in range(MAP_SIZE_X):
            game_map[0][x] = 'x'
            game_map[MAP_SIZE_Y - 1][x] = 'x'
        for y in range(MAP_SIZE_Y):
            game_map[y][0] = 'x'
            game_map[y][MAP_SIZE_X - 1] = 'x'

        return game_map

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
        place_entity('m', NUM_MELEE)
        place_entity('r', NUM_RANGED)
        place_entity('o', NUM_OBJECT)
        place_entity('t', NUM_TREASURE)
        
        # Place player
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if is_valid_position(x, y):
                entity_map[y][x] = 'p'
                break

        return entity_map
    
    def generate_light_map(self):
        coordinates = []
        for y, row in enumerate(self.grid_map):
            for x, col in enumerate(row):
                if col == 'x':  # Check if the current tile is ' ' (representing 0)
                    coordinates.append([x, y])  # Append the coordinates to the list
        return coordinates