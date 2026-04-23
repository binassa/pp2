import pygame, sys
from pygame.locals import *
import random
import os

pygame.init()

# ---------------- GAME SETTINGS ----------------
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game - Coins & Speed Upgrade")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Verdana", 20)

# ---------------- IMAGE PATH ----------------
BASE_IMG_PATH = os.path.join("images")

# ---------------- GAME VARIABLES ----------------
coins_collected = 0
speed = 5
LEVEL_UP_COINS = 5


# ---------------- ENEMY CLASS ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, speed)

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- PLAYER CLASS ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- COIN CLASS ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.coin_types = [
            (os.path.join(BASE_IMG_PATH, "coin1.png"), 1),
            (os.path.join(BASE_IMG_PATH, "coin2.png"), 3),
            (os.path.join(BASE_IMG_PATH, "coin3.png"), 5)
        ]

        self.reset()

    def reset(self):
        self.image_path, self.value = random.choice(self.coin_types)
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, 6)

        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- OBJECTS ----------------
P1 = Player()
E1 = Enemy()
C1 = Coin()

# ---------------- GAME LOOP ----------------
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    P1.update()
    E1.move()
    C1.move()

    DISPLAYSURF.fill(WHITE)

    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    # ---------------- COIN COLLECTION ----------------
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += C1.value
        C1.reset()

    # ---------------- SPEED SYSTEM ----------------
    if coins_collected >= LEVEL_UP_COINS:
        speed += 1
        LEVEL_UP_COINS += 5

    # ---------------- SCORE ----------------
    score_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 140, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)