import pygame

class App:
    def __init__(self):
        self._running = True
        self.size = (self.width, self.height) = (800, 500)
        self.window = pygame.display.set_mode(self.size)
        self.background_color = (0, 0, 0)
        self.game_over = False  #is the game over?
        self.score = 0
        self.rect_size = (self.rect_width, self.rect_height) = (50, 50)

    def is_running(self) -> bool:
        return self._running

    def stop_running(self):
        self._running = False

    def reset(self):
        self.size = (self.width, self.height) = (800, 500)
        self.window = pygame.display.set_mode(self.size)
        self.background_color = (0, 0, 0)
        self.game_over = False  #is the game over?
        self.score = 0
        self.rect_size = (self.rect_width, self.rect_height) = (50, 50)

    # def update_centre(self):
    #     self.centre = (self.pos[0] + self.rect_width / 2, self.pos[1] + self.rect_height / 2)

class Player:
    def __init__(self):
        self.pos = [400, 490]
        self.speed = 5
        self.color = (0, 255, 0)

    def draw(self, window, app):
        print(self.pos, app.rect_width, app.rect_height)
        pygame.draw.rect(window, self.color, (*self.pos, app.rect_width, app.rect_height)) # idfk why ts needs a pointer


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, speed):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()