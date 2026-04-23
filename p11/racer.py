import pygame, sys
from pygame.locals import *
import random

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

# Font for score display
font = pygame.font.SysFont("Verdana", 20)

# ---------------- GAME VARIABLES ----------------
coins_collected = 0          # total score
speed = 5                    # enemy speed starts slow
LEVEL_UP_COINS = 5          # every 5 coins → speed increases


# ---------------- ENEMY CLASS ----------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Enemy moves downward with dynamic speed
        self.rect.move_ip(0, speed)

        # Reset enemy when it goes off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- PLAYER CLASS ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        # Move left
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        # Move right
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- COIN CLASS (WITH WEIGHTS) ----------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Coin types with different weights (values)
        self.coin_types = [
            ("coin1.png", 1),   # normal coin
            ("coin2.png", 3),   # rare coin
            ("coin3.png", 5)    # very rare coin
        ]

        # Randomly choose coin type
        self.image_path, self.value = random.choice(self.coin_types)

        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

        self.reset()

    def reset(self):
        # Respawn coin at random position on top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

        # Randomize coin type again when respawning
        self.image_path, self.value = random.choice(self.coin_types)
        self.image = pygame.image.load(self.image_path)

    def move(self):
        self.rect.move_ip(0, 6)

        # Reset if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ---------------- CREATE OBJECTS ----------------
P1 = Player()
E1 = Enemy()
C1 = Coin()


# ---------------- GAME LOOP ----------------
while True:

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update player and enemy
    P1.update()
    E1.move()
    C1.move()

    # Clear screen
    DISPLAYSURF.fill(WHITE)

    # Draw objects
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    C1.draw(DISPLAYSURF)

    # ---------------- COIN COLLECTION ----------------
    if pygame.sprite.collide_rect(P1, C1):
        coins_collected += C1.value   # add coin weight (1, 3, or 5)
        C1.reset()

    # ---------------- SPEED INCREASE SYSTEM ----------------
    # Every N coins → enemy becomes faster
    if coins_collected >= LEVEL_UP_COINS:
        speed += 1
        LEVEL_UP_COINS += 5   # next upgrade threshold

    # ---------------- SCORE DISPLAY ----------------
    score_text = font.render(f"Coins: {coins_collected}", True, BLACK)
    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 140, 10))

    # Update screen
    pygame.display.update()
    FramePerSec.tick(FPS)