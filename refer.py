import pygame
import sys
import random
from pygame.locals import *

# 初始化 Pygame
pygame.init()
pygame.font.init()

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("打字游戏 - 单词射击")

# 颜色定义
BACKGROUND = (20, 20, 40)
TEXT_COLOR = (220, 220, 255)
ACCENT_COLOR = (70, 130, 180)
HIGHLIGHT_COLOR = (100, 200, 255)
ERROR_COLOR = (255, 100, 100)
SUCCESS_COLOR = (100, 255, 150)
PLAYER_COLOR = (70, 200, 255)
WORD_COLORS = [
    (255, 180, 100),  # 橙色
    (180, 255, 100),  # 绿色
    (100, 200, 255),  # 蓝色
    (255, 100, 200),  # 粉色
    (200, 100, 255),  # 紫色
]

# 字体
title_font = pygame.font.SysFont("microsoftyahei", 48, bold=True)
word_font = pygame.font.SysFont("consolas", 32)
input_font = pygame.font.SysFont("consolas", 36, bold=True)
info_font = pygame.font.SysFont("microsoftyahei", 24)
game_over_font = pygame.font.SysFont("microsoftyahei", 64, bold=True)

# 单词库
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


# 游戏状态
class GameState:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.words = []
        self.current_input = ""
        self.game_over = False
        self.paused = False
        self.speed_factor = 1.0
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000  # 毫秒
        self.reset()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.words = []
        self.current_input = ""
        self.game_over = False
        self.paused = False
        self.speed_factor = 1.0
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_interval = 2000  # 毫秒

    def spawn_word(self):
        if pygame.time.get_ticks() - self.last_spawn_time > self.spawn_interval:
            word = random.choice(WORD_LIST)
            x = random.randint(100, WIDTH - 100)
            color = random.choice(WORD_COLORS)
            self.words.append({
                "text": word,
                "x": x,
                "y": -50,
                "color": color,
                "speed": random.uniform(0.5, 1.5) * self.speed_factor,
                "typed": False
            })
            self.last_spawn_time = pygame.time.get_ticks()

    def update_words(self):
        for word in self.words[:]:
            word["y"] += word["speed"]

            # 检查单词是否到达底部
            if word["y"] > HEIGHT + 50:
                self.words.remove(word)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True

    def check_input(self):
        for word in self.words:
            if word["text"] == self.current_input.lower() and not word["typed"]:
                word["typed"] = True
                self.score += len(word["text"]) * 10
                self.current_input = ""

                # 移除单词并播放成功音效
                self.words.remove(word)

                # 每得500分升一级并增加速度
                if self.score // 500 >= self.level:
                    self.level += 1
                    self.speed_factor += 0.1

                return True
        return False


# 创建游戏状态
game = GameState()


# 绘制背景
def draw_background():
    # 绘制星空背景
    screen.fill(BACKGROUND)
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

    # 绘制底部输入区域
    pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT - 80, WIDTH, 80))
    pygame.draw.line(screen, ACCENT_COLOR, (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 2)

    # 绘制标题
    title = title_font.render("打字游戏 - 单词射击", True, HIGHLIGHT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))


# 绘制游戏信息
def draw_game_info():
    # 绘制分数
    score_text = info_font.render(f"分数: {game.score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 20))

    # 绘制生命值
    lives_text = info_font.render(f"生命: {game.lives}", True, TEXT_COLOR)
    screen.blit(lives_text, (20, 60))

    # 绘制等级
    level_text = info_font.render(f"等级: {game.level}", True, TEXT_COLOR)
    screen.blit(level_text, (WIDTH - 150, 20))

    # 绘制速度
    speed_text = info_font.render(f"速度: {game.speed_factor:.1f}x", True, TEXT_COLOR)
    screen.blit(speed_text, (WIDTH - 150, 60))

    # 绘制提示
    hint_text = info_font.render("输入单词并按回车消除", True, (150, 150, 180))
    screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 120))


# 绘制输入框
def draw_input():
    # 绘制输入框背景
    input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 60, 400, 40)
    pygame.draw.rect(screen, (40, 40, 60), input_rect, border_radius=5)
    pygame.draw.rect(screen, ACCENT_COLOR, input_rect, 2, border_radius=5)

    # 绘制输入文本
    input_text = input_font.render(game.current_input, True, TEXT_COLOR)
    screen.blit(input_text, (input_rect.x + 10, input_rect.y + input_text.get_height() // 2 - 10))

    # 绘制光标
    if pygame.time.get_ticks() % 1000 < 500:
        cursor_x = input_rect.x + 10 + input_text.get_width()
        pygame.draw.line(screen, HIGHLIGHT_COLOR,
                         (cursor_x, input_rect.y + 5),
                         (cursor_x, input_rect.y + input_rect.height - 5), 2)


# 绘制单词
def draw_words():
    for word in game.words:
        text = word_font.render(word["text"], True, word["color"])
        screen.blit(text, (word["x"] - text.get_width() // 2, word["y"]))

        # 绘制下落的轨迹
        pygame.draw.line(screen, (*word["color"], 50),
                         (word["x"], word["y"] + 10),
                         (word["x"], HEIGHT), 1)


# 绘制玩家
def draw_player():
    # 绘制玩家（键盘形状）
    pygame.draw.rect(screen, PLAYER_COLOR, (WIDTH // 2 - 40, HEIGHT - 160, 80, 30), border_radius=5)

    # 绘制按键
    for i in range(5):
        pygame.draw.rect(screen, (50, 50, 70),
                         (WIDTH // 2 - 35 + i * 15, HEIGHT - 155, 10, 20), border_radius=2)


# 绘制游戏结束画面
def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    game_over_text = game_over_font.render("游戏结束", True, ERROR_COLOR)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))

    score_text = title_font.render(f"最终分数: {game.score}", True, SUCCESS_COLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

    restart_text = info_font.render("按 R 键重新开始", True, HIGHLIGHT_COLOR)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))


# 主游戏循环
clock = pygame.time.Clock()
while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if game.game_over:
                if event.key == K_r:
                    game.reset()
            else:
                if event.key == K_RETURN:
                    # 检查输入
                    if not game.check_input():
                        pass

                    game.current_input = ""
                elif event.key == K_BACKSPACE:
                    game.current_input = game.current_input[:-1]
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.unicode.isprintable() and len(game.current_input) < 20:
                    game.current_input += event.unicode

    # 游戏逻辑更新
    if not game.game_over and not game.paused:
        game.spawn_word()
        game.update_words()

    # 绘制
    draw_background()
    draw_words()
    draw_player()
    draw_game_info()
    draw_input()

    if game.game_over:
        draw_game_over()

    # 更新屏幕
    pygame.display.flip()
    clock.tick(60)