from inventory import Weapon, Consumable, Armor

sword_steel = Weapon('img/sword.png', 20, 20, 'hand', 'sword')
sword_wood = Weapon('img/swordWood.png', 10, 10, 'right_hand', 'sword')
hp_potion = Consumable('img/potionRed.png', 2, 30)
helmet_armor = Armor('img/helmet.png', 10, 20, 'head')
chest_armor = Armor('img/chest.png', 10, 40, 'chest')
upg_helmet_armor = Armor('img/upg_helmet.png', 10, 40, 'head')
upg_chest_armor = Armor('img/upg_chest.png', 10, 80, 'chest')