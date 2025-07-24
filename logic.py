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


def render_end_screen(app: App, high_score: int):
    while True:
        app.window.fill(BLACK)

        # Render messages
        title = FONT.render("Game Over", True, WHITE)
        restart_msg = SMALL_FONT.render("Press R to Restart", True, WHITE)
        quit_msg = SMALL_FONT.render("Press Q or ESC to Quit", True, WHITE)
        score_msg = SMALL_FONT.render(f"Score {app.score}", True, WHITE)
        high_score_msg = SMALL_FONT.render(f"High score {high_score}", True, WHITE)
        # Position messages
        app.window.blit(title, title.get_rect(              center=(app.width // 2, 480 // 2 - 60)))
        app.window.blit(restart_msg, restart_msg.get_rect(  center=(app.width // 2, 480 // 2)))
        app.window.blit(quit_msg, quit_msg.get_rect(        center=(app.width // 2, 480 // 2 + 40)))
        app.window.blit(score_msg, score_msg.get_rect(      center=(app.width // 2, 480 // 2 + 70)))
        app.window.blit(high_score_msg, score_msg.get_rect( center=(app.width // 2 - 20, 480 // 2 + 100)))

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
    player = Player()

    while app.is_running():
        if app.game_over:
            with open("highscore.txt", "r") as f:
                high_score = int(f.readline())

            if app.score > high_score:
                high_score = app.score

            with open("highscore.txt", "w") as f:
                f.write(str(high_score))

            render_end_screen(app, high_score)
            player = Player()
            app.reset()
            blocks.empty()

            continue

        app.score += 1

        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                app.stop_running()

        keys = pygame.key.get_pressed()

        if random.random() < spawn_chance:
            x = random.randrange(0, app.width - app.rect_width)
            blocks.add(Block(x, -app.rect_height,
                             app.rect_width, app.rect_height,
                             WHITE, random.randrange(player.speed - 1, player.speed + 1)))

        if keys[K_LEFT]:
            player.pos[0] = max(0, player.pos[0] - player.speed)
        if keys[K_RIGHT]:
            player.pos[0] = min(app.width - app.rect_width, player.pos[0] + player.speed)
        if keys[K_UP]:
            player.pos[1] = max(0, player.pos[1] - player.speed)
        if keys[K_DOWN]:
            player.pos[1] = min(app.height - app.rect_height, player.pos[1] + player.speed)

        blocks.update()

        win = app.window
        win.fill(app.background_color)

        blocks.draw(win)
        player.draw(win, app)

        score_msg = SMALL_FONT.render(f"Score: {app.score}", True, WHITE)
        app.window.blit(score_msg, score_msg.get_rect(center=(60, 30)))

        pygame.display.flip()

        player_rect = pygame.Rect(*player.pos, app.rect_width, app.rect_height)
        if blocks and any(sprite.rect.colliderect(player_rect) for sprite in blocks):
            app.game_over = True

        clock.tick(60)
