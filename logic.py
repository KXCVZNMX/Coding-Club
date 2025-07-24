import random
from pygame.locals import *
from classes import *

pygame.init()

pygame.display.set_caption('App')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("Arial", 36)
SMALL_FONT = pygame.font.SysFont("Arial", 24)


def render_end_screen(app: App):
    while True:
        app.window.fill(BLACK)

        # Render messages
        title = FONT.render("Game Over", True, WHITE)
        restart_msg = SMALL_FONT.render("Press R to Restart", True, WHITE)
        quit_msg = SMALL_FONT.render("Press Q or ESC to Quit", True, WHITE)

        # Position messages
        app.window.blit(title, title.get_rect(center=(640 // 2, 480 // 2 - 60)))
        app.window.blit(restart_msg, restart_msg.get_rect(center=(640 // 2, 480 // 2)))
        app.window.blit(quit_msg, quit_msg.get_rect(center=(640 // 2, 480 // 2 + 40)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    app.game_over = False
                    return
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()


def run(app):
    blocks = pygame.sprite.Group()
    clock = pygame.time.Clock()
    spawn_chance = 0.075

    while app.is_running():
        if app.game_over:
            render_end_screen(app)

            blocks.empty()
            app.pos = [400, 490]
            app.update_centre()
            continue


        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                app.stop_running()

        keys = pygame.key.get_pressed()


        if random.random() < spawn_chance:
            x = random.randrange(0, app.width - app.rect_width)
            blocks.add(Block(x, -app.rect_height,
                             app.rect_width, app.rect_height,
                             WHITE, random.randrange(app.speed - 1, app.speed + 1)))


        if keys[K_LEFT]:
            app.pos[0] = max(0, app.pos[0] - app.speed)
        if keys[K_RIGHT]:
            app.pos[0] = min(app.width - app.rect_width, app.pos[0] + app.speed)
        if keys[K_UP]:
            app.pos[1] = max(0, app.pos[1] - app.speed)
        if keys[K_DOWN]:
            app.pos[1] = min(app.height - app.rect_height, app.pos[1] + app.speed)


        blocks.update()


        win = app.window
        win.fill(app.background_color)
        app.update_centre()
        blocks.draw(win)
        pygame.draw.rect(win, GREEN, (*app.pos, app.rect_width, app.rect_height))
        pygame.display.flip()


        player_rect = pygame.Rect(*app.pos, app.rect_width, app.rect_height)
        if blocks and any(sprite.rect.colliderect(player_rect) for sprite in blocks):
            app.game_over = True

        clock.tick(60)
