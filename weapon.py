import pygame



class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, damage, groups):
        super().__init__(groups)
        self.image
        self.name = name
        self.damage = damage
