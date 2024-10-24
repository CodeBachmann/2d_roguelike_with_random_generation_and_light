
# USE TO IMPROVE FPS BUT LOSE QUALITY
FULLSCREEN = False
QUALITY_NUM = 1
WIDTH = int(660 * QUALITY_NUM)
HEIGHT = int(WIDTH / 1.83)
TILE_SIZE = int(WIDTH / 20.625)
FPS = 60
IMG_SCALE = TILE_SIZE / 96
SCREEN_SCALE = 64 / TILE_SIZE
HITBOX_OFFSET = {
	'player': -16,
	'object': -40,
	'grass': -10,
	'invisible': 0}

MAP_SIZE_X = 65
MAP_SIZE_Y = MAP_SIZE_X
ROOM_COUNT = MAP_SIZE_X // 5
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 12

NUM_MELEE = 0
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

    'Fighter': {
        'hp': 500, 'mana': 50, 'stamina': 80, 'prot': 0, 'speed': 6, 'wisdom': 10, 'dexterity': 11, 'strength': 11, 'endurance': 10,
        'intelligence': 9, 'vigor': 14, 'faith': 8, 'level': 5
    },

    'Mage': {
         'hp': 500, 'mana': 50, 'stamina': 80, 'prot': 0, 'speed': 6, 'wisdom': 15, 'dexterity': 11, 'strength': 9, 'endurance': 8,
        'intelligence': 15, 'vigor': 8, 'faith': 8, 'level': 3
    },

    'Rogue': {
        'hp': 500, 'mana': 50, 'stamina': 80, 'prot': 0, 'speed': 6, 'wisdom': 9, 'dexterity': 14, 'strength': 12, 'endurance': 11,
        'intelligence': 9, 'vigor': 11, 'faith': 9, 'level': 4
    },

    'Priest': {
        'hp': 500, 'mana': 50, 'stamina': 80, 'prot': 0, 'speed': 6, 'wisdom': 11, 'dexterity': 8, 'strength': 12, 'endurance': 9,
        'intelligence': 8, 'vigor': 11, 'faith': 14, 'level': 2
    }

}

# weapons 
weapon_data = {
	'sword': {'cooldown': 500, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 800, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 400, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 300, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 350, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
	'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'exp':120,'damage':120,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}


projectile_data = {
    'fireball': {'image_path': 'graphics/particles/flame/fire.png', 'missile': True, 'width': 32,
                  'height': 32, 'movable': True, 'speed_modifier': 1.5, 'range': 400, 'dispersion': 0,
                    'initial_color': (255, 0, 0), 'final_color': (255, 255, 0), 'type': 'arc', 'shield': False, 'chain_length': 60},

    'sword': {'image_path': 'graphics/weapons/sword/full.png', 'missile': False, 'width': 32, 
              'height': 32, 'movable': True, 'speed_modifier': 1, 'range': 300, 'dispersion': 0,
                'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'arc', 'shield': False, 'chain_length': 60},

    'lance': {'image_path': 'graphics/weapons/lance/full.png', 'missile': False, 'width': 32, 
              'height': 32, 'movable': True, 'speed_modifier': 1, 'range': 100, 'dispersion': 0,
                'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'arc', 'shield': False, 'chain_length': 60},

    'axe': {'image_path': 'graphics/weapons/axe/full.png', 'missile': False, 'width': 32,
             'height': 32, 'movable': True, 'speed_modifier': 1, 'range': 100, 'dispersion': 0,
               'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'arc', 'shield': False, 'chain_length': 60},

    'rapier': {'image_path': 'graphics/weapons/rapier/full.png', 'missile': False, 'width': 32, 
               'height': 32, 'movable': True, 'speed_modifier': 1, 'range': 100, 'dispersion': 0,
                 'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'bar', 'shield': False, 'chain_length': 60},

    'sai': {'image_path': 'graphics/weapons/sai/full.png', 'missile': False, 'width': 32,
             'height': 32, 'movable': True, 'speed_modifier': 1, 'range': 100, 'dispersion': 0, 
             'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'bar', 'shield': False, 'chain_length': 60},

    'slash': {
        'image_path': "None", 'missile': True, 'width': 16, 'height': 16, 'movable': True,
        'speed_modifier': 0.2, 'range': 100, 'dispersion': 0, 'initial_color': (255, 255, 255),
          'final_color': (255, 255, 255), 'type': 'cone', 'shield': False, 'chain_length': 60},

    'buckler': {'image_path': 'graphics/weapons/wood_buckler/Wood_Buckler.png', 'missile': False, 'width': 32,
                'height': 5, 'movable': False, 'speed_modifier': 1, 'range': 0, 'dispersion': 0,
                'initial_color': (255, 255, 255), 'final_color': (255, 255, 255), 'type': 'bar', 'shield': True, 'chain_length': 30}}

# INVENTORY

WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 102, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
GOLD = (255,215,0)

#game settings/options
BGCOLOR = DARKGREY
STATPOSX = 50
UIHEIGTH = int(350*IMG_SCALE)
INVTILESIZE = 28
GRIDWIDTH = int(WIDTH / TILE_SIZE)
GRIDHEIGHT = int(HEIGHT / TILE_SIZE)