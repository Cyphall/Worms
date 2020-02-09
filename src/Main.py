import pygame

from src.Level import Level

pygame.init()
screen = pygame.display.set_mode((1600, 900), pygame.DOUBLEBUF)

level = Level(screen)
level.loop()
