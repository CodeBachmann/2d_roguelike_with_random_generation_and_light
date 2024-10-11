
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 64
FPS = 60
HITBOX_OFFSET = {
	'player': -16,
	'object': -40,
	'grass': -10,
	'invisible': 0}

MAP_SIZE_X = 100
MAP_SIZE_Y = 100
ROOM_COUNT = 20
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 12

NUM_MELEE = 10
NUM_RANGED = 10
NUM_OBJECT = 15
NUM_TREASURE = 5

MIN_X_OFFSET = 0
MAX_X_OFFSET = MAP_SIZE_X * TILE_SIZE
MIN_Y_OFFSET = 0
MAX_Y_OFFSET = MAP_SIZE_Y * TILE_SIZE
LIGHT_COLOR = [255, 255, 255]


from map import Map
map_generator = Map()

entity_map = map_generator.entity_map
tile_map = map_generator.grid_map
color_map = map_generator.color_map
light_map = map_generator.light_map

classes_data = {

    'fighter': {
        'hp': 180, 'mana': 30, 'speed': 6, 'dexterity': 5, 'attack': 8, 'defense': 8
    },

    'mage': {
         'hp': 100, 'mana': 100, 'speed': 4, 'dexterity': 6, 'attack': 7, 'defense': 3
    },

    'rogue': {
        'hp': 120, 'mana': 40, 'speed': 9, 'dexterity': 9, 'attack': 6, 'defense': 4
    }
}