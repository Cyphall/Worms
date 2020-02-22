import math
import random

import pygame

from Enums import *
from Grenade import Grenade
from Rocket import Rocket
from Worm import Worm


class Level:
	def __init__(self, screen):
		self.screen = screen
		self.running = True
		
		self.blue_worms = []
		self.red_worms = []
		
		# noinspection PyArgumentList
		self.blue_worms.append(Worm(Team.BLUE, pygame.Vector2(600, 300)))
		# noinspection PyArgumentList
		self.red_worms.append(Worm(Team.RED, pygame.Vector2(700, 300)))
		# noinspection PyArgumentList
		self.blue_worms.append(Worm(Team.BLUE, pygame.Vector2(800, 300)))
		# noinspection PyArgumentList
		self.red_worms.append(Worm(Team.RED, pygame.Vector2(900, 300)))
		
		self.background = pygame.image.load("assets/background.png")
		self.foreground = pygame.image.load("assets/foreground.png").convert_alpha()
		
		self.mask_image = pygame.image.load("assets/mask.png").convert_alpha()
		self.mask = None
		self.masked_foreground = None
		self.recalculate_mask()
		
		self.active_worm = self.worms()[0]
		self.active_worm.walking_credits = 200
		self.last_blue = -1
		self.last_red = -1
		self.projectile = None
		self.state = GameState.WF_PLAYER_ACTION
		self.current_team = self.active_worm.team
		
		self.skip_next_round_end_check = False
		
		self.original_wind_arrow = pygame.image.load("assets/wind_arrow.png").convert_alpha()
		self.wind = None
		self.wind_arrow = None
		self.wind_font = pygame.font.Font("assets/font.ttf", 40)
		self.game_over_font = pygame.font.Font("assets/font.ttf", 80)
		self.wind_text = None
		self.randomize_wind()
		
		self.clock = pygame.time.Clock()
	
	# noinspection PyArgumentList
	def loop(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.state == GameState.WF_PLAYER_ACTION:
						# noinspection PyArgumentList
						mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
						direction = mouse_pos - self.active_worm.position
						direction.scale_to_length(10)
						if event.button == pygame.BUTTON_LEFT:
							# noinspection PyArgumentList
							self.projectile = Rocket(pygame.Vector2(self.active_worm.position), direction)
							self.state = GameState.WF_WEAPON_ACTION_END
						elif event.button == pygame.BUTTON_RIGHT:
							# noinspection PyArgumentList
							self.projectile = Grenade(pygame.Vector2(self.active_worm.position), direction)
							self.state = GameState.WF_WEAPON_ACTION_END
			
			self.draw_terrain()
			
			for worm in self.worms():
				worm.update(self.mask, worm == self.active_worm, self.state)
			
			if self.state == GameState.WF_WEAPON_ACTION_END:
				if self.projectile.update(self.mask, self.wind):
					pygame.draw.circle(self.mask_image, (0, 0, 0, 0), self.projectile.position, self.projectile.explosion_radius)
					self.recalculate_mask()
					self.state = GameState.WF_ROUND_END
					self.skip_next_round_end_check = True
					for worm in self.worms():
						worm_center = worm.image.get_rect().center
						worm_centered_pos = worm.position + pygame.Vector2(worm_center[0], worm_center[1])
						projectile_center = self.projectile.image.get_rect().center
						projectile_centered_pos = self.projectile.position + pygame.Vector2(projectile_center[0], projectile_center[1])
						knockback_direction = pygame.Vector2(worm_centered_pos.x - projectile_centered_pos.x, worm_centered_pos.y - projectile_centered_pos.y)
						distance = knockback_direction.magnitude()
						safe_distance = self.projectile.explosion_radius + 10
						if distance < safe_distance:
							interaction_multiplier = ((safe_distance - distance) / safe_distance)
							worm.health -= self.projectile.damages * interaction_multiplier
							worm.velocity += (knockback_direction / distance) * 10 * interaction_multiplier
							if worm.health <= 0:
								if worm.team == Team.RED:
									index = self.red_worms.index(worm)
									self.red_worms.remove(worm)
									if self.last_red >= index:
										self.last_red -= 1
								else:
									index = self.blue_worms.index(worm)
									self.blue_worms.remove(worm)
									if self.last_blue >= index:
										self.last_blue -= 1
				self.projectile.draw(self.screen)
			
			for worm in self.worms():
				worm.draw2(self.screen, worm == self.active_worm)
			
			wind_arrow_center = self.wind_arrow.get_rect().center
			self.screen.blit(self.wind_arrow, (1500 - wind_arrow_center[0], 50 - wind_arrow_center[1]))
			self.screen.blit(self.wind_text, (1490, 90))
			
			if self.skip_next_round_end_check:
				self.skip_next_round_end_check = False
			elif self.state == GameState.WF_ROUND_END:
				for worm in self.worms():
					if worm.velocity.x != 0 or worm.velocity.y != 0:
						break
				else:
					self.state = GameState.WF_PLAYER_ACTION
					
					if len(self.red_worms) + len(self.blue_worms) == 0:
						self.win(None)
						break
					elif len(self.red_worms) == 0:
						self.win(Team.BLUE)
						break
					elif len(self.blue_worms) == 0:
						self.win(Team.RED)
						break
					
					if self.active_worm.team == Team.BLUE:
						if self.active_worm in self.blue_worms:
							self.last_blue = self.blue_worms.index(self.active_worm)
						self.active_worm = self.red_worms[(self.last_red + 1) % len(self.red_worms)]
					else:
						if self.active_worm in self.red_worms:
							self.last_red = self.red_worms.index(self.active_worm)
						self.active_worm = self.blue_worms[(self.last_blue + 1) % len(self.blue_worms)]
					
					self.active_worm.walking_credits = 250
					
					self.current_team = self.active_worm.team
					self.randomize_wind()
			
			pygame.display.flip()
			self.clock.tick(60)
	
	def randomize_wind(self):
		# noinspection PyArgumentList
		self.wind = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
		if self.wind.x == 0 and self.wind.y == 0:
			# noinspection PyArgumentList
			self.wind = pygame.Vector2(0.001, 0.001)
		angle = math.degrees(math.atan2(-self.wind.y, self.wind.x))
		self.wind_arrow = pygame.transform.rotate(self.original_wind_arrow, angle)
		self.wind_text = self.wind_font.render(str(int(self.wind.magnitude())), True, pygame.Color("yellow3"))
	
	def win(self, team: Team = None):
		if team == Team.BLUE:
			game_over_text = self.game_over_font.render("Team Blue won!", True, (0, 94, 255, 255))
		elif team == Team.RED:
			game_over_text = self.game_over_font.render("Team Red won!", True, pygame.Color("red"))
		else:
			game_over_text = self.game_over_font.render("Draw! Nobody is alive!", True, pygame.Color("white"))
		center = game_over_text.get_rect().center
		self.screen.blit(game_over_text, (800 - center[0], 450 - center[1]))
		pygame.display.flip()
		event = pygame.event.wait()
		while event.type not in (pygame.MOUSEBUTTONDOWN, pygame.QUIT):
			event = pygame.event.wait()
		self.running = False
	
	def worms(self):
		return self.blue_worms + self.red_worms
	
	def draw_terrain(self):
		self.screen.blit(self.background, (0, 0))
		self.screen.blit(self.masked_foreground, (0, 0))
	
	def recalculate_mask(self):
		self.mask = pygame.mask.from_surface(self.mask_image)
		self.masked_foreground = self.foreground.copy()
		self.masked_foreground.blit(self.mask_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
