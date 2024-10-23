import pygame as pg
import sys
import random
from settings_inv import *
from sprites import *
from inventory import *

class Game():
	def __init__(self):
		pg.init()
		pg.font.init()
		self.myfont = pg.font.SysFont('Calibri', 25)
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()

	def new(self):
		# start a new game
		self.all_sprites = pg.sprite.Group()

	def run(self):
		# game loop
		while True:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def quit(self):
		sys.exit()

	def update(self):
		# game loop update
		self.all_sprites.update()
		self.player.update()
		self.all_coins.update()

	def events(self):
		# game loop events
		for event in pg.event.get():
        # check for closing window
			if event.type == pg.QUIT:
				self.quit()
			
			if self.inventory.display_inventory:
				if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
					mouse_pos = pg.mouse.get_pos()
					self.inventory.checkSlot(self.screen, mouse_pos)

				elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
					self.inventory.moveItem(self.screen)

				elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
					self.inventory.placeItem(self.screen)




	def draw_player_stats(self):
		self.hp = self.myfont.render(f"{self.player.hp}" , False, RED)
		self.prot = self.myfont.render(f"{self.player.prot}" , False, WHITE)
		self.atk = self.myfont.render(f"{self.player.atk}" , False, WHITE)
		self.coins = self.myfont.render(f"{self.player.p_coins}" , False, GOLD)

		self.hpimg = pg.image.load('img/heart.png').convert_alpha()
		self.protimg = pg.image.load('img/upg_shieldSmall.png').convert_alpha()
		self.atkimg = pg.image.load('img/upg_dagger.png').convert_alpha()
		self.coinimg = pg.image.load('img/coin1.png').convert_alpha()

		self.screen.blit(self.hp,(STATPOSX,25))
		self.screen.blit(self.prot,(STATPOSX,75))
		self.screen.blit(self.atk,(STATPOSX,125))
		self.screen.blit(self.coins,(STATPOSX,175))
		self.screen.blit(self.hpimg,(STATPOSX-50,5))
		self.screen.blit(self.protimg,(STATPOSX-50,55))
		self.screen.blit(self.atkimg,(STATPOSX-50,105))
		self.screen.blit(self.coinimg,(STATPOSX-55,155))

	def draw(self):
		# game loop draw
		self.screen.fill(BGCOLOR)
		self.draw_grid()
		self.all_sprites.draw(self.screen)
		self.inventory.draw(self.screen)
		self.draw_player_stats()
		# flipping display after drawing
		pg.display.flip()

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		pass

g = Game()
while True:
	g.new()

pg.quit()