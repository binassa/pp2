import pygame
from persistence import load_settings
from ui import main_menu, username_screen, leaderboard_screen, settings_screen, game_over_screen
from racer import play_game

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lane Based Racer")


def main():
    settings = load_settings()

    while True:
        choice = main_menu(screen)

        if choice == "play":
            username = username_screen(screen)

            if username is None:
                break

            while True:
                result, score, distance, coins = play_game(screen, username, settings)

                if result == "quit":
                    return

                action = game_over_screen(screen, score, distance, coins)

                if action == "retry":
                    continue

                if action == "menu":
                    break

                if action == "quit":
                    return

        elif choice == "leaderboard":
            result = leaderboard_screen(screen)

            if result == "quit":
                return

        elif choice == "settings":
            result = settings_screen(screen, settings)
            settings = load_settings()

            if result == "quit":
                return

        elif choice == "quit":
            return


main()
pygame.quit()