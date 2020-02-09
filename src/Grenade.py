import pygame

from src.Sprite import Sprite


class Grenade(Sprite):
	def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
		# noinspection PyTypeChecker
		super().__init__(pygame.image.load("../assets/grenade.png"), position)
		self.velocity = velocity
		
		self.mask = pygame.mask.from_surface(self.image)
		
		self.damages = 50
		self.explosion_radius = 70
	
	def update(self, mask: pygame.Mask, wind: pygame.Vector2):
		self.velocity.y += 0.15
		self.position += self.velocity
		
		return mask.overlap(self.mask, (int(self.position.x), int(self.position.y)))
