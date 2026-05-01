import pygame, sys
from pygame.locals import *
import random
import os
from persistence import add_score

pygame.init()
pygame.mixer.init()

# ---------------- GAME SETTINGS ----------------
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# ---------------- COLORS ----------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
YELLOW = (255, 255, 0)
ORANGE = (255, 140, 0)
BLUE = (0, 100, 255)
PURPLE = (150, 0, 200)
GREEN = (0, 180, 0)

font = pygame.font.SysFont("Verdana", 20)
small_font = pygame.font.SysFont("Verdana", 14)

# ---------------- PATHS ----------------
BASE_IMG_PATH = os.path.join(os.path.dirname(__file__),"assets/", "images")

# ---------------- LANES ----------------
lanes = [100, 200, 300]

# ---------------- ROAD ----------------
road_y = 0


# ---------------- ENEMY CLASS ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "enemy.png"))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.choice(lanes), -80)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- PLAYER CLASS ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "player.png"))
        self.rect = self.image.get_rect()

        self.current_lane = 1
        self.rect.center = (lanes[self.current_lane], 520)

    def move_left(self):
        if self.current_lane > 0:
            self.current_lane -= 1
            self.rect.centerx = lanes[self.current_lane]

    def move_right(self):
        if self.current_lane < len(lanes) - 1:
            self.current_lane += 1
            self.rect.centerx = lanes[self.current_lane]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- COIN CLASS ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.coin_types = [
            (os.path.join(BASE_IMG_PATH, "coin1.png"), 1),
            (os.path.join(BASE_IMG_PATH, "coin2.png"), 3),
            (os.path.join(BASE_IMG_PATH, "coin3.png"), 5)
        ]

        self.speed = speed
        self.reset()

    def reset(self):
        self.image_path, self.value = random.choice(self.coin_types)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(lanes), -150)

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- OBSTACLE CLASS ----------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, speed, player_lane):
        super().__init__()

        self.type = random.choice(["oil", "barrier", "pothole", "speed_bump"])

        if self.type == "oil":
            self.image = pygame.Surface((55, 35))
            self.image.fill(BLACK)

        elif self.type == "barrier":
            self.image = pygame.Surface((65, 35))
            self.image.fill(ORANGE)

        elif self.type == "speed_bump":
            self.image = pygame.Surface((65, 25))
            self.image.fill(YELLOW)

        else:
            self.image = pygame.Surface((55, 35))
            self.image.fill((40, 40, 40))

        self.rect = self.image.get_rect()
        self.speed = speed

        # Safe spawn: do not spawn directly in player's lane
        lane = random.choice(lanes)
        while lane == lanes[player_lane]:
            lane = random.choice(lanes)

        self.rect.center = (lane, -100)

    def move(self):
        self.rect.move_ip(0, self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        text = small_font.render(self.type, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))


# ---------------- POWER-UP CLASS ----------------
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((40, 40))

        if self.type == "nitro":
            self.image.fill(BLUE)

        elif self.type == "shield":
            self.image.fill(PURPLE)

        else:
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = 5000
        self.rect.center = (random.choice(lanes), -120)

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.timeout

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        letter = self.type[0].upper()
        text = small_font.render(letter, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))


# ---------------- DRAW ROAD ----------------
def draw_road(screen, enemy_speed):
    global road_y

    screen.fill(GRAY)

    for x in [150, 250]:
        y = road_y
        while y < SCREEN_HEIGHT:
            pygame.draw.rect(screen, WHITE, (x, y, 8, 40))
            y += 80

    road_y += enemy_speed

    if road_y >= 80:
        road_y = 0


# ---------------- DIFFICULTY ----------------
def get_difficulty(settings):
    if settings["difficulty"] == "easy":
        return 4, 3000, 7000

    if settings["difficulty"] == "hard":
        return 7, 1600, 4500

    return 5, 2200, 6000


# ---------------- MAIN GAME FUNCTION ----------------
def play_game(screen, username, settings):
    global road_y

    road_y = 0

    coins_collected = 0
    distance = 0
    finish_distance = 3000

    base_speed, obstacle_delay, powerup_delay = get_difficulty(settings)

    enemy_speed = base_speed
    coin_speed = base_speed + 1
    LEVEL_UP_COINS = 5

    active_power = None
    power_start_time = 0
    power_duration = 4000
    shield_active = False
    power_bonus = 0

    last_obstacle_time = pygame.time.get_ticks()
    last_powerup_time = pygame.time.get_ticks()

    P1 = Player()
    E1 = Enemy(enemy_speed)
    C1 = Coin(coin_speed)

    obstacles = []
    powerups = []

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit", 0, 0, 0

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    P1.move_left()

                if event.key == K_RIGHT:
                    P1.move_right()

        # ---------------- DISTANCE + SCORE ----------------
        distance += enemy_speed * 0.08
        remaining_distance = max(0, finish_distance - distance)

        score = coins_collected * 10 + int(distance) + power_bonus

        # ---------------- DIFFICULTY SCALING ----------------
        if distance > 700:
            obstacle_delay = max(700, obstacle_delay - 1)

        if distance > 1500:
            enemy_speed = max(enemy_speed, base_speed + 2)

        # ---------------- SPAWN OBSTACLES ----------------
        if current_time - last_obstacle_time > obstacle_delay:
            obstacles.append(Obstacle(enemy_speed, P1.current_lane))
            last_obstacle_time = current_time

        # ---------------- SPAWN POWER UPS ----------------
        if current_time - last_powerup_time > powerup_delay:
            powerups.append(PowerUp(coin_speed))
            last_powerup_time = current_time

        # ---------------- NITRO TIMER ----------------
        if active_power == "nitro":
            if current_time - power_start_time > power_duration:
                enemy_speed -= 3
                active_power = None

        # ---------------- MOVE OBJECTS ----------------
        E1.speed = enemy_speed
        C1.speed = coin_speed

        E1.move()
        C1.move()

        for obstacle in obstacles[:]:
            obstacle.speed = enemy_speed
            obstacle.move()

            if obstacle.rect.top > SCREEN_HEIGHT:
                obstacles.remove(obstacle)

        for powerup in powerups[:]:
            powerup.speed = coin_speed
            powerup.move()

            if powerup.rect.top > SCREEN_HEIGHT or powerup.expired():
                powerups.remove(powerup)

        # ---------------- DRAW ----------------
        draw_road(screen, enemy_speed)

        P1.draw(screen)
        E1.draw(screen)
        C1.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        for powerup in powerups:
            powerup.draw(screen)

        # ---------------- COIN COLLECTION ----------------
        if pygame.sprite.collide_rect(P1, C1):
            coins_collected += C1.value
            C1.reset()

        # ---------------- SPEED SYSTEM WHEN N COINS ----------------
        if coins_collected >= LEVEL_UP_COINS:
            enemy_speed += 1
            LEVEL_UP_COINS += 5

        # ---------------- POWER-UP COLLECTION ----------------
        for powerup in powerups[:]:
            if pygame.sprite.collide_rect(P1, powerup):

                # Only one power-up can be active at a time
                if active_power is None:

                    if powerup.type == "nitro":
                        active_power = "nitro"
                        power_start_time = current_time
                        enemy_speed += 3
                        power_bonus += 50

                    elif powerup.type == "shield":
                        active_power = "shield"
                        shield_active = True
                        power_bonus += 30

                    elif powerup.type == "repair":
                        if obstacles:
                            obstacles.pop(0)
                        power_bonus += 20

                powerups.remove(powerup)

        # ---------------- OBSTACLE COLLISION ----------------
        for obstacle in obstacles[:]:
            if pygame.sprite.collide_rect(P1, obstacle):

                # Speed bump only slows down, not game over
                if obstacle.type == "speed_bump":
                    enemy_speed = max(3, enemy_speed - 1)
                    obstacles.remove(obstacle)

                elif shield_active:
                    shield_active = False
                    active_power = None
                    obstacles.remove(obstacle)

                else:
                    add_score(username, score, distance)
                    return "game_over", score, distance, coins_collected

        # ---------------- ENEMY COLLISION ----------------
        if pygame.sprite.collide_rect(P1, E1):

            if shield_active:
                shield_active = False
                active_power = None
                E1.reset()

            else:
                add_score(username, score, distance)
                return "game_over", score, distance, coins_collected

        # ---------------- FINISH ----------------
        if distance >= finish_distance:
            score += 500
            add_score(username, score, distance)
            return "game_over", score, distance, coins_collected

        # ---------------- HUD ----------------
        score_text = font.render(f"Score: {score}", True, WHITE)
        coins_text = font.render(f"Coins: {coins_collected}", True, WHITE)
        speed_text = font.render(f"Speed: {enemy_speed}", True, WHITE)
        distance_text = font.render(f"Dist: {int(distance)}m", True, WHITE)
        remaining_text = font.render(f"Left: {int(remaining_distance)}m", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 35))
        screen.blit(speed_text, (10, 60))
        screen.blit(distance_text, (10, 85))
        screen.blit(remaining_text, (10, 110))

        # ---------------- POWER-UP DISPLAY ----------------
        if active_power == "nitro":
            remaining = max(0, (power_duration - (current_time - power_start_time)) // 1000)
            power_text = small_font.render(f"Power: Nitro {remaining}s", True, YELLOW)

        elif active_power == "shield":
            power_text = small_font.render("Power: Shield", True, YELLOW)

        else:
            power_text = small_font.render("Power: None", True, WHITE)

        screen.blit(power_text, (190, 10))

        pygame.display.update()
        FramePerSec.tick(FPS)