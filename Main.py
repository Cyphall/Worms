import pygame

from Level import Level

pygame.init()
screen = pygame.display.set_mode((1600, 900))

level = Level(screen)
level.loop()
