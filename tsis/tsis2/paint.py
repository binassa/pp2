import pygame
import math
from datetime import datetime
from tools import flood_fill


WIDTH = 640
HEIGHT = 480
TOOLBAR_HEIGHT = 80
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT


def draw_shape(surface, mode, color, start_pos, end_pos, thickness):
    x1, y1 = start_pos
    x2, y2 = end_pos

    if mode == "line":
        pygame.draw.line(surface, color, start_pos, end_pos, thickness)

    elif mode == "square":
        size = min(abs(x2 - x1), abs(y2 - y1))
        if x2 < x1:
            x1 -= size
        if y2 < y1:
            y1 -= size
        pygame.draw.rect(surface, color, (x1, y1, size, size), thickness)

    elif mode == "rectangle":
        rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        rect.normalize()
        pygame.draw.rect(surface, color, rect, thickness)

    elif mode == "circle":
        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        pygame.draw.circle(surface, color, start_pos, radius, thickness)

    elif mode == "right_triangle":
        pygame.draw.polygon(surface, color, [
            start_pos,
            (x1, y2),
            (x2, y2)
        ], thickness)

    elif mode == "equilateral_triangle":
        side = abs(x2 - x1)
        height = int((math.sqrt(3) / 2) * side)

        direction = 1 if x2 >= x1 else -1

        pygame.draw.polygon(surface, color, [
            (x1, y1),
            (x1 + direction * side, y1),
            (x1 + direction * side // 2, y1 - height)
        ], thickness)

    elif mode == "rhombus":
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        pygame.draw.polygon(surface, color, [
            (mid_x, y1),
            (x2, mid_y),
            (mid_x, y2),
            (x1, mid_y)
        ], thickness)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint with Tools")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 12)
    text_font = pygame.font.SysFont("Arial", 16)

    canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
    canvas.fill((0, 0, 0))

    color = (0, 0, 255)
    mode = "pencil"
    thickness = 5

    drawing = False
    start_pos = None
    prev_pos = None

    typing = False
    text_pos = None
    current_text = ""

    while True:
        mouse_pos = pygame.mouse.get_pos()
        canvas_mouse_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # ---------------- KEYBOARD ----------------
            if event.type == pygame.KEYDOWN:

                # Save with Ctrl + S
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"paint_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print("Saved:", filename)

                # Text typing
                elif typing:
                    if event.key == pygame.K_RETURN:
                        canvas.blit(text_font.render(current_text, True, color), text_pos)
                        typing = False
                        current_text = ""

                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        current_text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]

                    else:
                        current_text += event.unicode

                else:
                    # Tools
                    if event.key == pygame.K_p:
                        mode = "pencil"
                    elif event.key == pygame.K_l:
                        mode = "line"
                    elif event.key == pygame.K_e:
                        mode = "eraser"
                    elif event.key == pygame.K_f:
                        mode = "fill"
                    elif event.key == pygame.K_x:
                        mode = "text"
                    elif event.key == pygame.K_s:
                        mode = "square"
                    elif event.key == pygame.K_a:
                        mode = "rectangle"
                    elif event.key == pygame.K_c:
                        mode = "circle"
                    elif event.key == pygame.K_t:
                        mode = "right_triangle"
                    elif event.key == pygame.K_q:
                        mode = "equilateral_triangle"
                    elif event.key == pygame.K_r:
                        mode = "rhombus"

                    # Brush sizes
                    elif event.key == pygame.K_1 and (pygame.key.get_mods() & pygame.KMOD_SHIFT) :
                        thickness = 2
                    elif event.key == pygame.K_2 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        thickness = 5
                    elif event.key == pygame.K_3 and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        thickness = 10

                    # Colors
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
                if event.button == 1 and event.pos[1] > TOOLBAR_HEIGHT:
                    pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                    if mode == "fill":
                        flood_fill(canvas, pos, color)

                    elif mode == "text":
                        typing = True
                        text_pos = pos
                        current_text = ""

                    else:
                        drawing = True
                        start_pos = pos
                        prev_pos = pos

            # ---------------- MOUSE MOTION ----------------
            if event.type == pygame.MOUSEMOTION:
                if drawing and event.pos[1] > TOOLBAR_HEIGHT:
                    current_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                    if mode == "pencil":
                        pygame.draw.line(canvas, color, prev_pos, current_pos, thickness)
                        prev_pos = current_pos

                    elif mode == "eraser":
                        pygame.draw.line(canvas, (0, 0, 0), prev_pos, current_pos, thickness)
                        prev_pos = current_pos

            # ---------------- MOUSE UP ----------------
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    drawing = False
                    end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                    if mode not in ["pencil", "eraser"]:
                        draw_shape(canvas, mode, color, start_pos, end_pos, thickness)

                    start_pos = None
                    prev_pos = None

        # ---------------- DRAW SCREEN ----------------
        screen.fill((40, 40, 40))

        # Toolbar
        pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

        line1 = "tools: P=Pencil | L=Line | E=Eraser | F=Fill | X=Text | S=Square | A=Rectangle | C=Circle"
        line2 = "shapes: T=Right Triangle | Q=Equilateral Triangle | R=Rhombus | Ctrl+S=Save"
        line3 = "size: shift+1=Small | shift+2=Medium | shift+3=Large     colors: 1=Red | 2=Green | 3=Blue | 4=White | 5=Yellow"

        screen.blit(font.render(line1, True, (0, 0, 0)), (10, 8))
        screen.blit(font.render(line2, True, (0, 0, 0)), (10, 30))
        screen.blit(font.render(line3, True, (0, 0, 0)), (10, 52))

        # Canvas
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Live preview for line and shapes
        if drawing and mode not in ["pencil", "eraser"]:
            preview = canvas.copy()
            draw_shape(preview, mode, color, start_pos, canvas_mouse_pos, thickness)
            screen.blit(preview, (0, TOOLBAR_HEIGHT))

        # Text preview
        if typing:
            pygame.draw.rect(screen, (255, 255, 255), (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT, 2, 25))
            text_surface = text_font.render(current_text, True, color)
            screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

        # Current status
        status = f"Tool: {mode} | Color: {color} | Size: {thickness}px"
        screen.blit(font.render(status, True, (255, 255, 255)), (10, HEIGHT - 20))

        pygame.display.flip()
        clock.tick(60)


main()