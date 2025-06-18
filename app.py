import random
import pygame
from pygame.locals import *

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class App:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self.size = (self.width, self.height) = (800, 500)
        self.window = pygame.display.set_mode(self.size)
        self.background_color = (0, 0, 0)
        self.game_over = False #is the game over?
        self.pos = [400, 490]
        self.speed = 5
        self.rect_size = (self.rect_width, self.rect_height) = (50, 50)

    def is_running(self) -> bool:
        return self._running

    def stop_running(self):
        self._running = False

class Object:
    def __init__(self, width: int, height: int, posx: int, posy: int, speed: int):
        self.rect_size = (self.rect_width, self.rect_height) = (width, height)
        self.color = (255, 255, 255)
        self.speed = speed
        self.pos = [posx, posy]

    def update(self):
        self.pos[1] += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.pos[0], self.pos[1], self.rect_width, self.rect_height), border_radius=6)

    def is_out(self, app: App) -> bool:
        return self.pos[1] > app.height + self.rect_height

def generate_object(app: App) -> Object:
    width = random.randint(30, 100)
    height = random.randint(30, 100)
    x = random.randint(0, app.width - width)
    y = -height - random.randint(0, 200)
    speed = 5
    return Object(width, height, x, y, speed)

def run(app: App) -> None:
    pygame.init()
    pygame.display.set_caption('App')

    falling_rects = []

    clock = pygame.time.Clock()

    while app.is_running():
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                app.stop_running()

        keys = pygame.key.get_pressed()

        for rect in falling_rects:
            rect.update()

        falling_rects = [rect for rect in falling_rects if not rect.is_out(app)]

        if random.random() < 0.075:
            falling_rects.append(generate_object(app))

        if keys[K_LEFT]:
            app.pos[0] = max(0, app.pos[0] - app.speed)
        if keys[K_RIGHT]:
            app.pos[0] = min(app.width - app.rect_width, app.pos[0] + app.speed)
        if keys[K_UP]:
            app.pos[1] = max(0, app.pos[1] - app.speed)
        if keys[K_DOWN]:
            app.pos[1] = min(app.height - app.rect_height, app.pos[1] + app.speed)

        app.window.fill(app.background_color)

        for rect in falling_rects:
            rect.draw(app.window)

        pygame.draw.rect(app.window, GREEN, (app.pos[0], app.pos[1], app.rect_width, app.rect_height))

        pygame.display.flip()

        clock.tick(60)