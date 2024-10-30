from inventory import Weapon, Consumable, Armor
import pygame
from random import choice
from settings import IMG_SCALE

class LootBag(pygame.sprite.Sprite):
    def __init__(self, groups, pos, tier, id):
        super().__init__(groups)

        self.id = id
        self.sprite_type = 'loot_bag'
        self.pos = pos
        self.image = pygame.image.load("graphics\\objects\\bags\\loot_bag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * IMG_SCALE, self.image.get_height() * IMG_SCALE))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox = self.rect.inflate(0,0)

        self.looted = False
        self.loot = []
        self.loot.append(self.generate_random_item(tier))

    def update(self):
        if self.looted == True:
            self.kill()

    def generate_random_item(self, tier, specific_item = None):
        decisions = ['consumable', 'weapon', 'armor']
        decision = choice(decisions)

        if decision == 'weapon':
            item_name = choice(list(weapons_data_set[tier].keys()))
            item_data = weapons_data_set[tier][item_name]
            print(item_data)
            return Weapon(item_data['image'], item_data['value'], item_data['attack'], item_data['type'], item_data['category'], item_data['category'])

        # elif decision == 'valuable':
        #     item_name = choice(list(valuable_data_set.keys()))
        #     item_data = valuable_data_set[item_name]
        #     return Consumable  # Return the name or create a Valuable class if needed

        elif decision == 'consumable':
            item_name = choice(list(consumable_data_set.keys()))
            item_data = consumable_data_set[item_name]
            image = item_data['image']
            value = item_data['heal']
            quantity = item_data['quantity']


            return Consumable(image, value, quantity)

        elif decision == 'armor':
            item_name = choice(list(armors_data_set[tier].keys()))
            item_data = armors_data_set[tier][item_name]
            return Armor(item_data['image'], item_data['value'], item_data['defense'], item_data['type'] )


weapons_data_set = {
    't1': {
        'sword_wood': {'image': 'img/swordWood.png', 'value': 20, 'attack': 20, 'type': 'hand', 'category': 'sword'},
        'cross_lance': {'image': 'graphics/icons/cross_lance.png', 'value': 20, 'attack': 20, 'type': 'hand', 'category': 'lance'},
        'dagger': {'image': 'graphics/icons/knife.png', 'value': 15, 'attack': 10, 'type': 'hand', 'category': 'dagger'},
        'axe': {'image': 'graphics/icons/axe.png', 'value': 30, 'attack': 20, 'type': 'hand', 'category': 'axe'},
        'curved_bow': {'image': 'graphics/icons/curved_bow.png', 'value': 25, 'attack': 15, 'type': 'hand', 'category': 'bow'},
        'wodden_shield': {'image': 'graphics/icons/wodden_shield.png', 'value': 20, 'attack': 40, 'type': 'right_hand', 'category': 'buckler'},
        'novice_staff': {'image': 'graphics/icons/novice_staff.png', 'value': 20, 'attack': 10, 'type': 'right_hand', 'category': 'staff'},
    },
    't2': {
        'sword_steel': {'image': 'img/sword.png', 'value': 40, 'attack': 40, 'type': 'hand', 'category': 'sword'},
        'iron_shield': {'image': 'graphics/icons/iron_shield.png', 'value': 20, 'attack': 40, 'type': 'right_hand', 'category': 'buckler'},
        'battle_axe': {'image': 'graphics/icons/double_head_war_axe.png', 'value': 50, 'attack': 30, 'type': 'hand', 'category': 'axe'},
        'golden_short_sword': {'image': 'graphics/icons/golden_short_sword.png', 'value': 35, 'attack': 25, 'type': 'hand', 'category': 'sword'},
        'great_iron_shield': {'image': 'graphics/icons/great_iron_shield.png', 'value': 30, 'attack': 50, 'type': 'right_hand', 'category': 'buckler'},
    },
    't3': {
        'demoniac_bow': {'image': 'graphics/icons/demoniac_bow.png', 'attack': 45, 'attack': 25, 'type': 'hand', 'category': 'bow'},
    }
}

armors_data_set = {
    't1': {
        'chest_armor': {'image': 'img/chest.png','value': 20 ,'defense': 40, 'type': 'chest'},
        'helmet_armor': {'image': 'img/helmet.png','value': 20, 'defense': 40, 'type': 'head'},
        'golden_helmet': {'image': 'graphics/icons/golden_helmet.png', 'value': 20, 'defense': 30, 'type': 'head'},
    },
    't2': {
        'upg_chest_armor': {'image': 'img/ipg_chest.png','value': 20 , 'defense': 80, 'type': 'chest'},
    }
}

valuable_data_set = {
    'wood': {'image': 'graphics/icons/wood.png', 'value': 1, 'quantity': 0},
    'gold': {'image': 'graphics/icons/gold.png', 'value': 1, 'quantity': 0},
    'iron': {'image': 'graphics/icons/iron.png', 'value': 1, 'quantity': 0},
}

consumable_data_set = {
    'hp_potion': {'image': 'img/potionRed.png', 'heal': 300, 'quantity': 2},
    'bread': {'image': 'graphics/icons/bread.png', 'heal': 100, 'quantity': 1},
    'banana': {'image': 'graphics/icons/banana.png', 'heal': 50, 'quantity': 1},
}

sword_steel = Weapon('img/sword.png', 20, 20, 'hand', 'sword', 'sword')
sword_wood = Weapon('img/swordWood.png', 20, 10, 'right_hand', 'sword', 'buckler')
hp_potion = Consumable('img/potionRed.png', 2, 30)
helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
chest_armor = Armor('img/chest.png', 10, 40, 'chest')
upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')

t1_itens = [chest_armor, helmet_armor, sword_wood]
t2_itens = [sword_steel, upg_chest_armor, upg_helmet_armor]