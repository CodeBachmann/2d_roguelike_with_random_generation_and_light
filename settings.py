
# USE TO IMPROVE FPS BUT LOSE QUALITY
FULLSCREEN = False
QUALITY_NUM = 1
WIDTH = int(660 * QUALITY_NUM)
HEIGHT = int(WIDTH / 1.83)
TILE_SIZE = int(WIDTH / 20.625)
print(TILE_SIZE)
FPS = 60
IMG_SCALE = TILE_SIZE / 96
SCREEN_SCALE = 64 / TILE_SIZE
HITBOX_OFFSET = {
	'player': -16,
	'object': -40,
	'grass': -10,
	'invisible': 0}

MAP_SIZE_X = 100
MAP_SIZE_Y = MAP_SIZE_X
ROOM_COUNT = int(MAP_SIZE_X /5)
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 12

NUM_MELEE = 1
NUM_RANGED = 1
NUM_OBJECT = 15
NUM_TREASURE = 5
NUM_LIGHT = 5

MIN_X_OFFSET = 0
MAX_X_OFFSET = MAP_SIZE_X * TILE_SIZE
MIN_Y_OFFSET = 0
MAX_Y_OFFSET = MAP_SIZE_Y * TILE_SIZE
LIGHT_COLOR = [255, 255, 255]
MOUSE_BUTTONS = [False, False, False, False, False]


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


projectile_data = {
    'fireball': {'image_path': 'graphics/particles/flame/fire.png', 'missile': True, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1.5},
    'sword': {'image_path': 'graphics/weapons/sword/full.png', 'missile': False, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1},
    'lance': {'image_path': 'graphics/weapons/lance/full.png', 'missile': False, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1},
    'axe': {'image_path': 'graphics/weapons/axe/full.png', 'missile': False, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1},
    'rapier': {'image_path': 'graphics/weapons/rapier/full.png', 'missile': False, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1},
    'sai': {'image_path': 'graphics/weapons/sai/full.png', 'missile': False, 'width': 32, 'height': 32, 'movable': True, 'speed_modifier': 1},
    'slash': {'image_path': None, 'missile': True, 'width': 16, 'height': 16, 'movable': False}}
