from classes import *
from pygame.locals import *
import random

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
        app.window.blit(title, title.get_rect(              center=(app.width // 2, app.height // 2 - 60)))
        app.window.blit(restart_msg, restart_msg.get_rect(  center=(app.width // 2, app.height // 2)))
        app.window.blit(quit_msg, quit_msg.get_rect(        center=(app.width // 2, app.height // 2 + 40)))
        app.window.blit(score_msg, score_msg.get_rect(      center=(app.width // 2, app.height // 2 + 70)))
        app.window.blit(high_score_msg, score_msg.get_rect( center=(app.width // 2 - 20, app.height // 2 + 100)))

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


def main():
    app = App()

    blocks = pygame.sprite.Group()
    clock = pygame.time.Clock()
    spawn_chance = 0.075
    player = Player()

    while app.is_running():
        if app.game_over:
            # Checks score
            with open("static/highscore.txt", "r") as f:
                high_score = int(f.readline())

            high_score = max(high_score, app.score)

            with open("static/highscore.txt", "w") as f:
                f.write(str(high_score))

            render_end_screen(app, high_score)

            # Reset playing field
            player = Player()
            app.reset()
            blocks.empty()

            continue

        # Adds to the score counter (1 point per frame)
        app.score += 1

        # Checks if user wants to exit
        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                app.stop_running()

        keys = pygame.key.get_pressed()

        # Spawn objects (adjust spawn_chance for more blocks)
        if random.random() < spawn_chance:
            x = random.randrange(0, app.width - app.rect_width)
            blocks.add(Block(x, -app.rect_height,
                             app.rect_width, app.rect_height,
                             WHITE, random.randrange(player.speed - 1, player.speed + 1)))

        # Movements
        if keys[K_LEFT]:
            player.pos[0] = max(0, player.pos[0] - player.speed)
        if keys[K_RIGHT]:
            player.pos[0] = min(app.width - app.rect_width, player.pos[0] + player.speed)
        if keys[K_UP]:
            player.pos[1] = max(0, player.pos[1] - player.speed)
        if keys[K_DOWN]:
            player.pos[1] = min(app.height - app.rect_height, player.pos[1] + player.speed)

        # Update every single sprite in the group
        blocks.update()

        # Renders the background
        win = app.window
        win.fill(app.background_color)

        # Renders the plyer and object
        blocks.draw(win)
        player.draw(win, app)

        # Renders the scores
        score_msg = SMALL_FONT.render(f"Score: {app.score}", True, WHITE)
        app.window.blit(score_msg, score_msg.get_rect(center=(60, 30)))

        # Update the window
        pygame.display.flip()

        # Checks collision
        player_rect = pygame.Rect(player.pos[0], player.pos[1], app.rect_width, app.rect_height)
        if blocks and any(sprite.rect.colliderect(player_rect) for sprite in blocks):
            app.game_over = True

        clock.tick(60)

if __name__ == '__main__':
    main()
