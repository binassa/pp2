import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, screen_width, screen_height):
        self.screen_size = (screen_width, screen_height)
        self.center = pygame.math.Vector2(screen_width // 2, screen_height // 2)
        
        # Determine the directory where this script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "images")

        # Load and scale images with error handling
        try:
            self.bg = pygame.image.load(os.path.join(img_dir, "clock.png")).convert()
            self.bg = pygame.transform.scale(self.bg, self.screen_size)
            
            self.mickey_body = pygame.image.load(os.path.join(img_dir, "mikkey.png")).convert_alpha()
            self.mickey_body = pygame.transform.scale(self.mickey_body, (380, 500)) 
            self.mickey_rect = self.mickey_body.get_rect(center=self.center)
            
            self.min_hand_orig = pygame.image.load(os.path.join(img_dir, "hand_right_centered.png")).convert_alpha()
            self.min_hand_orig = pygame.transform.scale(self.min_hand_orig, (200, 300))
            
            self.sec_hand_orig = pygame.image.load(os.path.join(img_dir, "hand_left_centered.png")).convert_alpha()
            self.sec_hand_orig = pygame.transform.scale(self.sec_hand_orig, (190, 280))
        except pygame.error as e:
            print(f"File loading error: {e}")
            pygame.quit()
            exit()

    def blit_rotate_pivot(self, surface, image, pos, originPos, angle):
        # Calculate the offset from the pivot point to the image's geometric center
        image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # Rotate the offset vector
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        
        # Calculate the new center point for the rotated image
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        
        # Rotate the actual image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        
        surface.blit(rotated_image, rotated_image_rect)

    def render(self, surface):
        surface.blit(self.bg, (0, 0))
        surface.blit(self.mickey_body, self.mickey_rect.topleft)
        
        now = datetime.datetime.now()
        
        # Logic: 360 degrees / 60 units = 6 degrees per unit
        # Minus sign makes it rotate clockwise
        min_angle = -(now.minute * 6)
        sec_angle = -(now.second * 6)

        # Pivot point logic (center-x, bottom-y)
        min_pivot = (self.min_hand_orig.get_width() // 2, self.min_hand_orig.get_height() // 2)
        sec_pivot = (self.sec_hand_orig.get_width() // 2, self.sec_hand_orig.get_height() // 2)

        self.blit_rotate_pivot(surface, self.min_hand_orig, self.center, min_pivot, min_angle)
        self.blit_rotate_pivot(surface, self.sec_hand_orig, self.center, sec_pivot, sec_angle)

def main():
    pygame.init()
    
    # Matching the scale you used in the class
    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Mouse Clock")
    
    mickey_clock = MickeyClock(WIDTH, HEIGHT)
    timer = pygame.time.Clock()
    
    running = True
    while running:
        # Check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw everything
        mickey_clock.render(screen)
        
        # Update display
        pygame.display.flip()
        
        # 60 Frames per second
        timer.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()