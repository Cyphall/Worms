import math

import pygame

from Sprite import Sprite


class Rocket(Sprite):
	def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
		self.original_image = pygame.image.load("assets/rocket.png")
		
		# noinspection PyArgumentList
		self.velocity = velocity
		
		self.mask = None
		self.image = None
		self.recalculate_image()
		
		self.damages = 55
		self.explosion_radius = 90
		
		# noinspection PyTypeChecker
		super().__init__(self.image, position)
	
	def recalculate_image(self):
		angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
		
		self.image = pygame.transform.rotate(self.original_image, angle)
		self.mask = pygame.mask.from_surface(self.image)
	
	def update(self, mask: pygame.Mask, wind: pygame.Vector2, screen: pygame.Surface):
		self.velocity.y += 0.2
		
		self.velocity += (wind - self.velocity) / 100
		
		self.position += self.velocity
		self.recalculate_image()
		
		return mask.overlap(self.mask, (int(self.position.x), int(self.position.y)))
