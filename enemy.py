import pygame
from settings import *
from entity import Entity
from support import *


class Enemy(Entity):
	def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp, create_projectile, id):

		# general setup
		super().__init__(groups)
		self.sprite_type = 'enemy'

		# graphics setup
		self.import_graphics(monster_name)
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]
		self.id = id

		# movement
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-10)
		self.obstacle_sprites = obstacle_sprites
		self.view_radius = 100
		self.player_rect_center = None

		# stats
		self.monster_name = monster_name
		monster_info = monster_data[self.monster_name]
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed'] * IMG_SCALE
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius'] * IMG_SCALE
		self.notice_radius = monster_info['notice_radius'] * IMG_SCALE
		self.attack_type = monster_info['attack_type']

		# player interaction
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.trigger_death_particles = trigger_death_particles
		self.add_exp = add_exp
		self.create_projectile = create_projectile
		# invincibility timer
		self.vulnerable = True
		self.hit_time = None
		self.invincibility_duration = 300

		# sounds
		self.death_sound = pygame.mixer.Sound('audio/death.wav')
		self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
		self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
		self.death_sound.set_volume(0.6)
		self.hit_sound.set_volume(0.6)
		self.attack_sound.set_volume(0.6)

	def import_graphics(self,name):
		self.animations = {'idle':[],'move':[],'attack':[]}
		main_path = f'graphics/monsters/{name}/'
		for animation in self.animations.keys():
			self.animations[animation] = import_folder(main_path + animation)
			for x, i in enumerate(self.animations[animation]):
				img = pygame.transform.scale(i, (int(i.get_width() * IMG_SCALE), int(i.get_height() * IMG_SCALE)))
				self.animations[animation][x] = img

	def get_player_distance_direction(self):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(self.player_rect_center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)

	def get_status(self):
		distance = self.get_player_distance_direction()[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage,self.attack_type)
			self.attack_sound.play()
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction()[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			if self.status == 'attack':
				self.can_attack = False
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if not self.can_attack:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hit_time >= self.invincibility_duration:
				self.vulnerable = True


	def check_death(self):
		if self.health <= 0:
			self.create_loot_bag()
			self.kill()
			self.trigger_death_particles(self.rect.center,self.monster_name)
			self.add_exp(self.exp)
			self.death_sound.play()

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def update(self):
		self.get_status()
		self.actions()
		self.hit_reaction()
		self.move(self.speed)
	
		self.animate()
		self.cooldowns()
		self.check_death()

