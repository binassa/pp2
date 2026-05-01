import pygame
import random
import json
import os
from datetime import datetime

from config import WIDTH, HEIGHT, CELL
from db import save_result, get_personal_best, get_top_10


class SnakeGame:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

        self.settings_file = "settings.json"
        self.settings = self.load_settings()

        self.username = ""
        self.running = True
        self.screen_state = "menu"

        self.reset_game()

    # ---------------- SETTINGS ----------------

    def load_settings(self):
        if not os.path.exists(self.settings_file):
            return {
                "snake_color": [0, 0, 0],
                "grid": True,
                "sound": True
            }

        with open(self.settings_file, "r") as file:
            return json.load(file)

    def save_settings(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    # ---------------- GAME RESET ----------------

    def reset_game(self):
        self.snake = [(300, 300)]
        self.direction = (0, 0)
        self.next_direction = (0, 0)

        self.score = 0
        self.level = 1
        self.speed = 10
        self.base_speed = 10

        self.food = None
        self.food_type = "bronze"
        self.food_spawn_time = pygame.time.get_ticks()

        self.poison = None

        self.power_up = None
        self.power_up_type = None
        self.power_spawn_time = 0
        self.power_active = None
        self.power_end_time = 0

        self.shield = False
        self.obstacles = []

        self.personal_best = 0

        self.spawn_food()
        self.spawn_poison()

    # ---------------- SPAWN HELPERS ----------------

    def random_empty_cell(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(40, HEIGHT, CELL)
            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.food
                and pos != self.poison
                and pos != self.power_up
            ):
                return pos

    def spawn_food(self):
        self.food = self.random_empty_cell()
        self.food_spawn_time = pygame.time.get_ticks()

        self.food_type = random.choice(["bronze", "silver", "gold"])

    def spawn_poison(self):
        self.poison = self.random_empty_cell()

    def spawn_power_up(self):
        if self.power_up is None:
            self.power_up = self.random_empty_cell()
            self.power_up_type = random.choice(["speed", "slow", "shield"])
            self.power_spawn_time = pygame.time.get_ticks()

    def spawn_obstacles(self):
        self.obstacles.clear()

        if self.level < 3:
            return

        count = self.level + 2

        for _ in range(count):
            pos = self.random_empty_cell()

            # Do not place obstacle too close to snake head
            head = self.snake[0]
            if abs(pos[0] - head[0]) <= CELL and abs(pos[1] - head[1]) <= CELL:
                continue

            self.obstacles.append(pos)

    # ---------------- DRAWING ----------------

    def draw_text(self, text, x, y, color=(0, 0, 0), font=None):
        if font is None:
            font = self.font

        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_button(self, text, rect):
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(self.screen, (210, 210, 210), (x, 40), (x, HEIGHT))

        for y in range(40, HEIGHT, CELL):
            pygame.draw.line(self.screen, (210, 210, 210), (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill((127, 255, 212))
        self.draw_grid()

        self.draw_text(
            f"Player: {self.username}  Score: {self.score}  Level: {self.level}  Best: {self.personal_best}",
            10,
            10,
            (0, 0, 0),
            self.small_font
        )

        # Food colors
        food_colors = {
            "bronze": (150, 75, 0),
            "silver": (192, 192, 192),
            "gold": (255, 215, 0)
        }

        pygame.draw.rect(
            self.screen,
            food_colors[self.food_type],
            (*self.food, CELL, CELL)
        )

        # Poison
        if self.poison:
            pygame.draw.rect(self.screen, (100, 0, 0), (*self.poison, CELL, CELL))

        # Power-up
        if self.power_up:
            colors = {
                "speed": (255, 100, 0),
                "slow": (0, 100, 255),
                "shield": (128, 0, 255)
            }

            pygame.draw.rect(
                self.screen,
                colors[self.power_up_type],
                (*self.power_up, CELL, CELL)
            )

        # Obstacles
        for block in self.obstacles:
            pygame.draw.rect(self.screen, (70, 70, 70), (*block, CELL, CELL))

        # Snake
        snake_color = tuple(self.settings["snake_color"])

        for segment in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*segment, CELL, CELL))

        if self.shield:
            self.draw_text("Shield ON", 480, 10, (80, 0, 150), self.small_font)

    # ---------------- MENU ----------------

    def main_menu(self):
        play_btn = pygame.Rect(200, 180, 200, 50)
        leader_btn = pygame.Rect(200, 250, 200, 50)
        settings_btn = pygame.Rect(200, 320, 200, 50)
        quit_btn = pygame.Rect(200, 390, 200, 50)

        typing = True

        while self.screen_state == "menu":
            self.screen.fill((127, 255, 212))

            self.draw_text("Snake Game", 220, 70)
            self.draw_text("Enter username:", 190, 120)
            self.draw_text(self.username, 260, 150, (0, 0, 255))

            self.draw_button("Play", play_btn)
            self.draw_button("Leaderboard", leader_btn)
            self.draw_button("Settings", settings_btn)
            self.draw_button("Quit", quit_btn)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen_state = "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        if len(self.username) < 15:
                            self.username += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_btn.collidepoint(event.pos):
                        if self.username.strip() != "":
                            self.personal_best = get_personal_best(self.username)
                            self.reset_game()
                            self.personal_best = get_personal_best(self.username)
                            self.screen_state = "game"

                    elif leader_btn.collidepoint(event.pos):
                        self.screen_state = "leaderboard"

                    elif settings_btn.collidepoint(event.pos):
                        self.screen_state = "settings"

                    elif quit_btn.collidepoint(event.pos):
                        self.running = False
                        self.screen_state = "quit"

    # ---------------- GAME LOGIC ----------------

    def update_level_speed(self):
        old_level = self.level

        self.level = self.score // 10 + 1
        self.base_speed = 10 + (self.level - 1) * 2

        if self.power_active is None:
            self.speed = self.base_speed

        if self.level != old_level:
            self.spawn_obstacles()

    def apply_power_up(self):
        now = pygame.time.get_ticks()

        if self.power_up_type == "speed":
            self.power_active = "speed"
            self.speed = self.base_speed + 6
            self.power_end_time = now + 5000

        elif self.power_up_type == "slow":
            self.power_active = "slow"
            self.speed = max(5, self.base_speed - 5)
            self.power_end_time = now + 5000

        elif self.power_up_type == "shield":
            self.shield = True

        self.power_up = None
        self.power_up_type = None

    def check_power_timer(self):
        now = pygame.time.get_ticks()

        if self.power_up and now - self.power_spawn_time > 8000:
            self.power_up = None
            self.power_up_type = None

        if self.power_active and now > self.power_end_time:
            self.power_active = None
            self.speed = self.base_speed

    def game_over(self):
        save_result(self.username, self.score, self.level)

        best = get_personal_best(self.username)

        if best > self.personal_best:
            self.personal_best = best

        self.screen_state = "game_over"

    def collision_game_over(self):
        if self.shield:
            self.shield = False
            self.snake[0] = (300, 300)
            self.direction = (0, 0)
            self.next_direction = (0, 0)
        else:
            self.game_over()

    def play_game(self):
        while self.screen_state == "game":
            self.clock.tick(self.speed)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen_state = "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.direction != (0, CELL):
                        self.next_direction = (0, -CELL)
                    elif event.key == pygame.K_s and self.direction != (0, -CELL):
                        self.next_direction = (0, CELL)
                    elif event.key == pygame.K_a and self.direction != (CELL, 0):
                        self.next_direction = (-CELL, 0)
                    elif event.key == pygame.K_d and self.direction != (-CELL, 0):
                        self.next_direction = (CELL, 0)

            self.direction = self.next_direction

            if self.direction != (0, 0):
                head_x, head_y = self.snake[0]
                new_head = (
                    head_x + self.direction[0],
                    head_y + self.direction[1]
                )

                self.snake.insert(0, new_head)

                # Normal food
                if new_head == self.food:
                    points = {
                        "bronze": 1,
                        "silver": 3,
                        "gold": 5
                    }

                    self.score += points[self.food_type]
                    self.spawn_food()
                    self.update_level_speed()

                    if random.randint(1, 4) == 1:
                        self.spawn_power_up()

                # Poison food
                elif new_head == self.poison:
                    self.spawn_poison()

                    for _ in range(2):
                        if len(self.snake) > 1:
                            self.snake.pop()

                    if len(self.snake) <= 1:
                        self.game_over()

                # Power-up
                elif self.power_up and new_head == self.power_up:
                    self.apply_power_up()
                    self.snake.pop()

                else:
                    self.snake.pop()

                # Food disappears after 8 seconds
                if pygame.time.get_ticks() - self.food_spawn_time > 8000:
                    self.spawn_food()

                # Border collision
                if (
                    new_head[0] < 0
                    or new_head[0] >= WIDTH
                    or new_head[1] < 40
                    or new_head[1] >= HEIGHT
                ):
                    self.collision_game_over()

                # Self collision
                if new_head in self.snake[1:]:
                    self.collision_game_over()

                # Obstacle collision
                if new_head in self.obstacles:
                    self.collision_game_over()

            self.check_power_timer()

            self.draw_game()
            pygame.display.update()

    # ---------------- GAME OVER SCREEN ----------------

    def game_over_screen(self):
        retry_btn = pygame.Rect(200, 300, 200, 50)
        menu_btn = pygame.Rect(200, 370, 200, 50)

        while self.screen_state == "game_over":
            self.screen.fill((127, 255, 212))

            self.draw_text("Game Over", 230, 120)
            self.draw_text(f"Final Score: {self.score}", 210, 180)
            self.draw_text(f"Level Reached: {self.level}", 210, 220)
            self.draw_text(f"Personal Best: {self.personal_best}", 210, 260)

            self.draw_button("Retry", retry_btn)
            self.draw_button("Main Menu", menu_btn)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen_state = "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_btn.collidepoint(event.pos):
                        self.reset_game()
                        self.personal_best = get_personal_best(self.username)
                        self.screen_state = "game"

                    elif menu_btn.collidepoint(event.pos):
                        self.screen_state = "menu"

    # ---------------- LEADERBOARD ----------------

    def leaderboard_screen(self):
        back_btn = pygame.Rect(220, 520, 160, 45)

        while self.screen_state == "leaderboard":
            self.screen.fill((127, 255, 212))

            self.draw_text("Leaderboard - Top 10", 180, 40)

            data = get_top_10()

            y = 100
            self.draw_text("Rank  User       Score  Level  Date", 70, y, font=self.small_font)
            y += 30

            for i, row in enumerate(data, start=1):
                username, score, level, played_at = row
                date = played_at.strftime("%Y-%m-%d")

                text = f"{i:<5} {username:<10} {score:<6} {level:<6} {date}"
                self.draw_text(text, 70, y, font=self.small_font)
                y += 30

            self.draw_button("Back", back_btn)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen_state = "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.collidepoint(event.pos):
                        self.screen_state = "menu"

    # ---------------- SETTINGS SCREEN ----------------

    def settings_screen(self):
        grid_btn = pygame.Rect(180, 160, 240, 45)
        sound_btn = pygame.Rect(180, 230, 240, 45)
        color_btn = pygame.Rect(180, 300, 240, 45)
        save_btn = pygame.Rect(180, 400, 240, 45)

        colors = [
            [0, 0, 0],
            [0, 0, 255],
            [255, 0, 0],
            [0, 150, 0],
            [255, 105, 180]
        ]

        color_index = 0

        while self.screen_state == "settings":
            self.screen.fill((127, 255, 212))

            self.draw_text("Settings", 250, 80)

            self.draw_button(f"Grid: {self.settings['grid']}", grid_btn)
            self.draw_button(f"Sound: {self.settings['sound']}", sound_btn)
            self.draw_button("Change Snake Color", color_btn)
            self.draw_button("Save & Back", save_btn)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.screen_state = "quit"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if grid_btn.collidepoint(event.pos):
                        self.settings["grid"] = not self.settings["grid"]

                    elif sound_btn.collidepoint(event.pos):
                        self.settings["sound"] = not self.settings["sound"]

                    elif color_btn.collidepoint(event.pos):
                        color_index = (color_index + 1) % len(colors)
                        self.settings["snake_color"] = colors[color_index]

                    elif save_btn.collidepoint(event.pos):
                        self.save_settings()
                        self.screen_state = "menu"

    # ---------------- MAIN LOOP ----------------

    def run(self):
        while self.running:
            if self.screen_state == "menu":
                self.main_menu()

            elif self.screen_state == "game":
                self.play_game()

            elif self.screen_state == "game_over":
                self.game_over_screen()

            elif self.screen_state == "leaderboard":
                self.leaderboard_screen()

            elif self.screen_state == "settings":
                self.settings_screen()

            elif self.screen_state == "quit":
                self.running = False

        pygame.quit()