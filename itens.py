from inventory import Weapon, Consumable, Armor
import pygame
from settings import IMG_SCALE

class LootBag(pygame.sprite.Sprite):
    def __init__(self, groups, pos, loot, id):
        super().__init__(groups)

        self.id = id
        self.sprite_type = 'loot_bag'
        self.pos = pos
        self.image = pygame.image.load("loot_bag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * IMG_SCALE, self.image.get_height() * IMG_SCALE))
        self.rect = self.image.get_rect(center = self.pos)
        self.hitbox = self.rect.inflate(0,0)

        self.looted = False
        self.loot = loot

    def update(self):
        if self.looted == True:
            self.kill()

sword_steel = Weapon('img/sword.png', 20, 20, 'hand', 'sword', 'sword')
sword_wood = Weapon('img/swordWood.png', 20, 10, 'right_hand', 'sword', 'buckler')
hp_potion = Consumable('img/potionRed.png', 2, 30)
helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
chest_armor = Armor('img/chest.png', 10, 40, 'chest')
upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')

t1_itens = [chest_armor, helmet_armor, sword_wood]
t2_itens = [sword_steel, upg_chest_armor, upg_helmet_armor]