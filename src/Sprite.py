import pygame


class Sprite(pygame.sprite.Sprite):
	def __init__(self, image: pygame.Surface, position: pygame.Vector2):
		super().__init__()
		self.image = image
		self.position = position
	
	def draw(self, screen: pygame.Surface):
		screen.blit(self.image, self.position)
