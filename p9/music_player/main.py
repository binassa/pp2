import os
import pygame
import sys  # <--- Added this
from player import MusicPlayer

# This gets the absolute path to the directory where main.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# This joins it with 'music' so Python knows exactly where to look
MUSIC_DIR = os.path.join(BASE_DIR, "music")

# Constants
WIDTH, HEIGHT = 600, 300
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREEN = (0, 255, 127)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Music Player")
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    # Use the MUSIC_DIR variable we defined above
    player = MusicPlayer(MUSIC_DIR) 
    
    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: player.play()
                if event.key == pygame.K_s: player.stop()
                if event.key == pygame.K_n: player.next_track()
                if event.key == pygame.K_b: player.prev_track()
                if event.key == pygame.K_q: running = False

        # UI Rendering
        track_text = font.render(f"Now Playing: {player.get_current_track_name()}", True, WHITE)
        status_text = font.render(f"Status: {'Playing' if player.is_playing else 'Stopped'}", True, GREEN)
        pos_text = font.render(f"Time: {player.get_progress()}s", True, WHITE)
        controls_text = font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (150, 150, 150))

        screen.blit(track_text, (50, 50))
        screen.blit(status_text, (50, 100))
        screen.blit(pos_text, (50, 150))
        screen.blit(controls_text, (50, 230))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()