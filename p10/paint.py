import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    radius = 5
    mode = 'pen'  # pen, rect, circle, eraser

    drawing = False
    start_pos = None
    prev_pos = None  # IMPORTANT for smooth lines

    screen.fill((0, 0, 0))  # background once

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:

                # tools
                if event.key == pygame.K_p:
                    mode = 'pen'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # colors
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    prev_pos = event.pos  # FIX for smooth drawing

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    prev_pos = None  # reset

                    # draw shapes only when mouse released
                    if mode == 'rect':
                        rect = pygame.Rect(
                            start_pos,
                            (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
                        )
                        pygame.draw.rect(screen, color, rect, 2)

                    elif mode == 'circle':
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        r = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(screen, color, start_pos, r, 2)

            if event.type == pygame.MOUSEMOTION:
                if drawing:

                    if mode == 'pen':
                        pygame.draw.line(screen, color, prev_pos, event.pos, radius * 2)
                        prev_pos = event.pos

                    elif mode == 'eraser':
                        pygame.draw.line(screen, (0, 0, 0), prev_pos, event.pos, radius * 2)
                        prev_pos = event.pos

        pygame.display.flip()
        clock.tick(60)

main()