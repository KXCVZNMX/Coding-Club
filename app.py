import pygame
from pygame.locals import *

WORD_LIST = [
    "python", "game", "keyboard", "program", "typing",
    "speed", "challenge", "developer", "puzzle", "victory",
    "keyboard", "algorithm", "function", "variable", "syntax",
    "loop", "class", "object", "module", "library",
    "pygame", "surface", "event", "render", "display",
    "pixel", "vector", "sprite", "collision", "animation",
    "sound", "music", "effect", "control", "player",
    "score", "level", "difficulty", "progress", "achievement"
]

class App:
    def __init__(self):
        self._running = True
        self._display_surface = None
        self.size = (self.width, self.height) = (800, 500)
        self.window = pygame.display.set_mode(self.size)
        self.background_color = (0, 0, 0)
        self.game_over = False #is the game over?
        self.current_input = ""

    def run(self):
        pygame.init()
        pygame.display.set_caption('App')

        while self._running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self._running = False

                if event.type == KEYDOWN:
                    if self.game_over:
                        # give option to reset
                        pass

                    else:
                        if event.key == K_RETURN:
                            #check input here, and if check input returns
                            #false, make self.game_over = True, else pass
                            self.current_input = ""

                        elif event.key == K_BACKSPACE:
                            self.current_input = self.current_input[:-1]

                        elif


            self.window.fill((0, 0, 0))