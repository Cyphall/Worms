import pygame

from Sprite import Sprite


class Grenade(Sprite):
	timer_font = None
	
	def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):
		# noinspection PyTypeChecker
		super().__init__(pygame.image.load("assets/grenade.png"), position)
		if Grenade.timer_font is None:
			Grenade.timer_font = pygame.font.Font("assets/font.ttf", 24)
		self.velocity = velocity
		
		self.mask = pygame.mask.from_surface(self.image)
		
		self.damages = 50
		self.explosion_radius = 70
		
		self.countdown = 180
	
	def draw(self, screen: pygame.Surface):
		super().draw(screen)
		timer = Grenade.timer_font.render(str(round(self.countdown / 60, 1)), True, (255, 255, 255))
		# noinspection PyArgumentList
		screen.blit(timer, self.position + pygame.Vector2(-5, -40))
	
	def update(self, mask: pygame.Mask, wind: pygame.Vector2, screen: pygame.Surface):
		self.velocity.y += 0.15
		self.position += self.velocity
		
		intersection = mask.overlap(self.mask, (int(self.position.x), int(self.position.y)))
		if intersection is not None:
			self.position -= self.velocity
			self.velocity = self.velocity.reflect(self.estimate_terrain_normal(mask, intersection, screen)) * 0.5
		
		self.countdown -= 1
		return self.countdown == 0
	
	# noinspection PyArgumentList
	def estimate_terrain_normal(self, mask: pygame.Mask, intersection: tuple, screen: pygame.Surface):
		if self.velocity.length() < 0.2:
			return pygame.Vector2(0, -1)
		
		position = pygame.Vector2(intersection)
		CW_vector = pygame.Vector2(self.velocity).normalize() * 10
		CCW_vector = pygame.Vector2(self.velocity).normalize() * 10
		
		rotation_step = 10
		
		found = False
		while not found:
			CW_vector.rotate_ip(rotation_step)
			abs_vector = position + CW_vector
			pixel = (int(abs_vector[0]), int(abs_vector[1]))
			Grenade.draw_debug(position, CW_vector, (255, 0, 0), screen)
			if 0 <= pixel[0] < mask.get_size()[0] and 0 <= pixel[1] < mask.get_size()[1]:
				found = mask.get_at(pixel) == 0
			else:
				found = True
		
		found = False
		while not found:
			CCW_vector.rotate_ip(-rotation_step)
			abs_vector = position + CCW_vector
			pixel = (int(abs_vector[0]), int(abs_vector[1]))
			Grenade.draw_debug(position, CCW_vector, (0, 255, 0), screen)
			if 0 <= pixel[0] < mask.get_size()[0] and 0 <= pixel[1] < mask.get_size()[1]:
				found = mask.get_at(pixel) == 0
			else:
				found = True
		
		CCW_to_CW = CW_vector - CCW_vector
		normal = pygame.Vector2(-CCW_to_CW[1], CCW_to_CW[0]).normalize()
		
		Grenade.draw_debug(position, normal, (0, 0, 255), screen)
		
		return normal
	
	@staticmethod
	def draw_debug(center: pygame.Vector2, vec: pygame.Vector2, color, screen: pygame.Surface):
		return
		pygame.draw.line(screen, color, center, center + vec)
		
		for event in pygame.event.get():
			pass
		
		pygame.display.update()
