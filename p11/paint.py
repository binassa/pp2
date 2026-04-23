import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint with Shapes")
    clock = pygame.time.Clock()

    # Default settings
    color = (0, 0, 255)
    mode = 'pen'

    drawing = False
    start_pos = None
    prev_pos = None

    screen.fill((0, 0, 0))  # background

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            # ---------------- KEY CONTROLS ----------------
            if event.type == pygame.KEYDOWN:

                # TOOL SELECTION
                if event.key == pygame.K_p:
                    mode = 'pen'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'right_triangle'
                elif event.key == pygame.K_q:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_r:
                    mode = 'rhombus'

                # COLOR SELECTION
                elif event.key == pygame.K_1:
                    color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)
                elif event.key == pygame.K_4:
                    color = (255, 255, 255)
                elif event.key == pygame.K_5:
                    color = (255, 255, 0)

            # ---------------- MOUSE DOWN ----------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    prev_pos = event.pos

            # ---------------- MOUSE UP ----------------
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    prev_pos = None

                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    # ---------------- SHAPES ----------------

                    # SQUARE
                    if mode == 'square':
                        size = min(abs(x2 - x1), abs(y2 - y1))
                        rect = pygame.Rect(x1, y1, size, size)
                        pygame.draw.rect(screen, color, rect, 2)

                    # RIGHT TRIANGLE
                    elif mode == 'right_triangle':
                        pygame.draw.polygon(screen, color, [
                            start_pos,
                            (x1, y2),
                            (x2, y2)
                        ], 2)

                    # EQUILATERAL TRIANGLE
                    elif mode == 'equilateral_triangle':
                        side = abs(x2 - x1)
                        height = int((math.sqrt(3) / 2) * side)

                        pygame.draw.polygon(screen, color, [
                            start_pos,
                            (x1 + side, y1),
                            (x1 + side // 2, y1 - height)
                        ], 2)

                    # RHOMBUS
                    elif mode == 'rhombus':
                        mid_x = (x1 + x2) // 2
                        mid_y = (y1 + y2) // 2

                        pygame.draw.polygon(screen, color, [
                            (mid_x, y1),
                            (x2, mid_y),
                            (mid_x, y2),
                            (x1, mid_y)
                        ], 2)

            # ---------------- DRAWING (PEN + ERASER) ----------------
            if event.type == pygame.MOUSEMOTION:
                if drawing:

                    # PEN (smooth line)
                    if mode == 'pen':
                        pygame.draw.line(screen, color, prev_pos, event.pos, 3)
                        prev_pos = event.pos

                    # ERASER (black line)
                    elif mode == 'eraser':
                        pygame.draw.line(screen, (0, 0, 0), prev_pos, event.pos, 10)
                        prev_pos = event.pos

        pygame.display.flip()
        clock.tick(60)

main()