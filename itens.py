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
        self.image = pygame.image.load("loot_bag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * IMG_SCALE, self.image.get_height() * IMG_SCALE))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox = self.rect.inflate(0,0)

        self.looted = False
        self.loot = []
        self.loot.append(self.generate_random_item(tier))

    def update(self):
        if self.looted == True:
            self.kill()

    def generate_random_item(self, tier):
        decisions = ['weapon', 'valuable', 'consumable', 'armor']
        decision = choice(decisions)

        if decision == 'weapon':
            item_name = choice(list(weapons_data_set[tier].keys()))
            item_data = weapons_data_set[tier][item_name]
            print(*item_data)
            return Weapon(*item_data)

        # elif decision == 'valuable':
        #     item_name = choice(list(valuable_data_set.keys()))
        #     item_data = valuable_data_set[item_name]
        #     return Consumable  # Return the name or create a Valuable class if needed

        elif decision == 'consumable':
            item_name = choice(list(consumable_data_set.keys()))
            item_data = consumable_data_set[item_name]
            print(*item_data)

            return Consumable(*item_data)

        elif decision == 'armor':
            item_name = choice(list(armors_data_set[tier].keys()))
            item_data = armors_data_set[tier][item_name]
            print(*item_data)

            return Armor(*item_data)


weapons_data_set = {
    't1': {
        'sword_wood': {'img/swordWood.png', 20, 20, 'hand', 'sword', 'sword'},
        'cross_lance': {'graphics/icons/cross_lance.png', 20, 20, 'hand', 'lance','lance'},
        'dagger': {'graphics/icons/knife.png', 15, 10, 'hand', 'dagger', 'dagger'},  # Attack item
        'axe': {'graphics/icons/axe.png', 30, 20, 'hand', 'axe', 'axe'},  # Attack item
        'curved_bow': {'graphics/icons/curved_bow.png', 25, 15, 'hand', 'bow', 'bow'},  # Attack item
        'iron_shield': {'graphics/icons/iron_shield.png', 20, 40, 'right_hand', 'buckler','buckler'},  # Shield as weapon
    },
    't2': {
        'sword_steel': {'img/sword.png', 40, 40, 'hand', 'sword', 'sword'},
        'battle_axe': {'graphics/icons/double_head_war_axe.png', 50, 30, 'hand', 'axe', 'axe'},  # Attack item
        'golden_short_sword': {'graphics/icons/golden_short_sword.png', 35, 25, 'hand', 'sword', 'sword'},  # Attack item
        'great_iron_shield': {'graphics/icons/great_iron_shield.png', 30, 50, 'right_hand', 'buckler', 'buckler'},  # Shield as weapon
    },
    't3': {
        'demoniac_bow': {'graphics/icons/demoniac_bow.png', 45, 25, 'hand', 'bow', 'bow'},  # Attack item
    }
}

armors_data_set = {
    't1': {
        'chest_armor': {'img/chest.png', 10, 40, 'chest'},
        'helmet_armor': {'img/helmet.png', 10, 40, 'head'},
        'golden_helmet': {'graphics/icons/golden_helmet.png', 15, 30, 'head'},  # Support item
    },
    't2': {
        'upg_chest_armor': {'img/ipg_chest.png', 20, 80, 'chest'},
    }
}

valuable_data_set = {
    'wood': {'graphics/icons/wood.png', 1, 0},  # Valuable item
    'gold': {'graphics/icons/gold.png', 1, 0},  # Valuable item
    'iron': {'graphics/icons/iron.png', 1, 0},  # Valuable item
}

consumable_data_set = {
    'hp_potion': {'img/potionRed.png', 2, 30},
    'bread': {'graphics/icons/bread.png', 1, 10},  # Consumable item
    'banana': {'graphics/icons/banana.png', 1, 5},  # Consumable item
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