import pygame
from persistence import load_leaderboard, save_settings

WIDTH = 400
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

pygame.font.init()
font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 16)


# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text = font.render(self.text, True, BLACK)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# ---------------- USERNAME SCREEN ----------------
def username_screen(screen):
    name = ""
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        title = font.render("Enter your name:", True, BLACK)
        screen.blit(title, (90, 200))

        box = pygame.Rect(80, 260, 240, 40)
        pygame.draw.rect(screen, GRAY, box)
        pygame.draw.rect(screen, BLACK, box, 2)

        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (90, 265))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


# ---------------- MAIN MENU ----------------
def main_menu(screen):
    buttons = [
        Button("Play", 100, 180, 200, 50),
        Button("Leaderboard", 100, 250, 200, 50),
        Button("Settings", 100, 320, 200, 50),
        Button("Quit", 100, 390, 200, 50)
    ]

    while True:
        screen.fill(WHITE)

        title = font.render("RACER GAME", True, BLACK)
        screen.blit(title, (110, 100))

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            for button in buttons:
                if button.clicked(event):
                    return button.text.lower()

        pygame.display.update()


# ---------------- LEADERBOARD ----------------
def leaderboard_screen(screen):
    back = Button("Back", 120, 520, 160, 50)

    while True:
        screen.fill(WHITE)

        title = font.render("Top 10 Scores", True, BLACK)
        screen.blit(title, (100, 40))

        scores = load_leaderboard()

        y = 100
        for i, s in enumerate(scores):
            text = small_font.render(
                f"{i+1}. {s['name']} | {s['score']} | {s['distance']}m",
                True,
                BLACK
            )
            screen.blit(text, (30, y))
            y += 35

        back.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back.clicked(event):
                return "menu"

        pygame.display.update()


# ---------------- SETTINGS ----------------
def settings_screen(screen, settings):
    sound_btn = Button("Sound", 100, 200, 200, 50)
    difficulty_btn = Button("Difficulty", 100, 280, 200, 50)
    back_btn = Button("Back", 100, 380, 200, 50)

    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        title = font.render("Settings", True, BLACK)
        screen.blit(title, (130, 100))

        sound_btn.draw(screen)
        difficulty_btn.draw(screen)
        back_btn.draw(screen)

        screen.blit(small_font.render(f"Sound: {settings['sound']}", True, BLACK), (120, 250))
        screen.blit(small_font.render(f"Difficulty: {settings['difficulty']}", True, BLACK), (120, 330))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if difficulty_btn.clicked(event):
                i = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(i + 1) % 3]
                save_settings(settings)

            if back_btn.clicked(event):
                return "menu"

        pygame.display.update()


# ---------------- GAME OVER ----------------
def game_over_screen(screen, score, distance, coins):
    retry = Button("Retry", 100, 360, 200, 50)
    menu = Button("Main Menu", 100, 430, 200, 50)

    while True:
        screen.fill(WHITE)

        title = font.render("GAME OVER", True, BLACK)
        screen.blit(title, (120, 150))

        screen.blit(small_font.render(f"Score: {score}", True, BLACK), (130, 230))
        screen.blit(small_font.render(f"Distance: {int(distance)}", True, BLACK), (130, 260))
        screen.blit(small_font.render(f"Coins: {coins}", True, BLACK), (130, 290))

        retry.draw(screen)
        menu.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry.clicked(event):
                return "retry"

            if menu.clicked(event):
                return "menu"

        pygame.display.update()