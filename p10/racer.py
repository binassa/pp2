import pygame, sys
from pygame.locals import *
import random
import os

pygame.init()

# Game settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Game with Coins")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Font
font = pygame.font.SysFont("Verdana", 20)

# ---------------- IMAGE PATH ----------------
BASE_IMG_PATH = os.path.join("photos")

# Coin counter
coins_collected = 0


# ---------------- ENEMY ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 8)

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- PLAYER ----------------
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


# ---------------- COIN ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_IMG_PATH, "coin.png"))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
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

    # ---------------- COIN COLLISION ----------------
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += 1
        C1.reset()

    # ---------------- SCORE ----------------
    coin_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 130, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)