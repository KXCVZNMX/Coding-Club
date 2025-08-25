import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Window")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()


