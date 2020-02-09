import pygame
from pygame.locals import *

from src.Enums import *
from src.Sprite import Sprite


class Worm(Sprite):
	health_font = None
	walking_credits_font = None
	
	def __init__(self, team: Team, position: pygame.Vector2):
		if Worm.health_font is None:
			Worm.health_font = pygame.font.Font("../assets/font.ttf", 24)
		if Worm.walking_credits_font is None:
			Worm.walking_credits_font = pygame.font.Font("../assets/font.ttf", 12)
		self.left_image = pygame.image.load("../assets/worm.png").convert_alpha()
		self.right_image = pygame.transform.flip(self.left_image, True, False)
		
		super().__init__(self.left_image, position)
		
		self.team = team
		self.mask = pygame.mask.from_surface(self.image)
		# noinspection PyArgumentList
		self.velocity = pygame.Vector2(0, 0)
		self.is_grounded = False
		self.direction = Direction.LEFT
		self.health = 100
		self.walking_credits = 0
	
	def update(self, mask: pygame.Mask, is_active: bool, state: GameState):
		if is_active:
			if state == GameState.WF_PLAYER_ACTION:
				if is_pressed(K_q) and self.walking_credits > 0:
					if self.is_grounded:
						self.velocity.x = -1
					else:
						self.velocity.x = max(self.velocity.x - 0.05, -1)
					self.image = self.left_image
				elif is_pressed(K_d) and self.walking_credits > 0:
					if self.is_grounded:
						self.velocity.x = 1
					else:
						self.velocity.x = min(self.velocity.x + 0.05, 1)
					self.image = self.right_image
				if is_pressed(K_SPACE) and self.is_grounded:
					self.velocity.y = -3.5
			if (self.velocity.x != 0 or self.velocity.y != 0) and self.walking_credits > 0:
				self.walking_credits -= 1
		
		if self.velocity.x != 0:
			count = 0
			while mask.overlap(self.mask, (int(self.position.x + self.velocity.x), int(self.position.y - count))) is not None:
				count += 1
				if count > 2:
					break
			
			if count > 2:
				self.velocity.x = 0
			
			self.position.x += self.velocity.x
			
			if count <= 2:
				self.position.y -= count
		
		self.velocity.y += 0.15
		
		self.is_grounded = False
		if mask.overlap(self.mask, (int(self.position.x), int(self.position.y + self.velocity.y))) is not None:
			if self.velocity.y > 0:
				self.is_grounded = True
			self.velocity.y = 0
		
		if self.is_grounded:
			self.velocity.x = 0
			self.velocity.y = 0
		
		self.position.y += self.velocity.y
	
	def draw2(self, screen: pygame.Surface, is_active: bool):
		super().draw(screen)
		health = Worm.health_font.render(str(int(self.health)), True, pygame.Color("red") if self.team == Team.RED else (0, 94, 255, 255))
		# noinspection PyArgumentList
		screen.blit(health, self.position + pygame.Vector2(-5, -40))
		if is_active:
			walking_credits = Worm.walking_credits_font.render(str(self.walking_credits), True, pygame.Color("red") if self.team == Team.RED else (0, 94, 255, 255))
			# noinspection PyArgumentList
			screen.blit(walking_credits, self.position + pygame.Vector2(0, -15))


def is_pressed(key: int):
	return pygame.key.get_pressed()[key]
