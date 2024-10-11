
WIDTH = 1320
HEIGHT = 720
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

NUM_MELEE = 1
NUM_RANGED = 1
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

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}
