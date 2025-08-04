import pygame
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Window")

pos = [400, 300]

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        pos[1] -= 5
    if keys[K_DOWN]:
        pos[1] += 5
    if keys[K_LEFT]:
        pos[0] -= 5
    if keys[K_RIGHT]:
        pos[0] += 5

    window.fill(BLACK)

    pygame.draw.rect(window, WHITE, (pos[0], pos[1], 50, 50))
    pygame.display.flip()

pygame.quit()
