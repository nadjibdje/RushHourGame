import pygame
from copy import deepcopy
from rush_hour import RushHourPuzzle
from BFS import bfs


# === CONSTANTS ===
CELL = 84
PADDING = 8
MARGIN = 40
BG = (245, 245, 245)
GRID = (210, 210, 210)
XCOLOR = (220, 70, 70)
VCOLOR = (80, 130, 210)
EXIT_COLOR = (60, 200, 100)
TXT = (32, 32, 32)

BTN_W, BTN_H = 220, 48
BTN_BG = (30, 180, 120)
BTN_BG_HOVER = (26, 160, 108)
BTN_TXT = (255, 255, 255)
BTN_RADIUS = 10


# === DRAW FUNCTION ===
def draw_board(screen, font, state: RushHourPuzzle, button_rect, info_text):
    screen.fill(BG)

    # Grid
    for r in range(state.board_height + 1):
        pygame.draw.line(screen, GRID,
                         (MARGIN, MARGIN + r * CELL),
                         (MARGIN + state.board_width * CELL, MARGIN + r * CELL), 1)
    for c in range(state.board_width + 1):
        pygame.draw.line(screen, GRID,
                         (MARGIN + c * CELL, MARGIN),
                         (MARGIN + c * CELL, MARGIN + state.board_height * CELL), 1)

    # Determine exit row (based on red car)
    try:
        X = next(v for v in state.vehicles if v["id"] == "X")
        exit_row = X["row"]
    except StopIteration:
        exit_row = state.board_height // 2

    # Draw Exit (green goal)
    exit_x = MARGIN + state.board_width * CELL - (PADDING // 2)
    exit_y = MARGIN + exit_row * CELL + PADDING
    exit_h = CELL - 2 * PADDING
    pygame.draw.rect(screen, EXIT_COLOR, (exit_x, exit_y, 12, exit_h), border_radius=6)

    # Draw Vehicles with padding
    for v in state.vehicles:
        color = XCOLOR if v["id"] == "X" else VCOLOR
        r, c = v["row"], v["col"]
        if v["orientation"] == "H":
            x = MARGIN + c * CELL + PADDING
            y = MARGIN + r * CELL + PADDING
            w = v["length"] * CELL - 2 * PADDING
            h = CELL - 2 * PADDING
        else:
            x = MARGIN + c * CELL + PADDING
            y = MARGIN + r * CELL + PADDING
            w = CELL - 2 * PADDING
            h = v["length"] * CELL - 2 * PADDING

        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, color, rect, border_radius=16)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=16)

        label = font.render(v["id"], True, (255, 255, 255))
        screen.blit(label, (rect.x + 8, rect.y + 6))

    # Draw Restart button
    mx, my = pygame.mouse.get_pos()
    is_hover = button_rect.collidepoint(mx, my)
    pygame.draw.rect(screen, BTN_BG_HOVER if is_hover else BTN_BG, button_rect, border_radius=BTN_RADIUS)
    txt = font.render("Restart", True, BTN_TXT)
    screen.blit(txt, (button_rect.x + (BTN_W - txt.get_width()) // 2, button_rect.y + (BTN_H - txt.get_height()) // 2))

    # Info text BELOW the button
    if info_text:
        info = font.render(info_text, True, TXT)
        info_x = button_rect.centerx - info.get_width() // 2
        info_y = button_rect.bottom + 10
        screen.blit(info, (info_x, info_y))


# === MAIN FUNCTION ===
def run_ui():
    # Load puzzle
    puzzle = RushHourPuzzle(csv_file="examples/1.csv")

    # Solve using BFS
    print("Solving with BFS...")
    node = bfs(puzzle, RushHourPuzzle.successorFunction, RushHourPuzzle.isGoal)
    if not node:
        print("No solution found.")
        return

    path = node.getPath()
    print(f"Solution found with {len(path) - 1} steps.")

    # Setup Pygame
    pygame.init()
    font = pygame.font.SysFont(None, 26)

    # Window height now bigger to fit bottom text
    W = MARGIN * 2 + puzzle.board_width * CELL
    H = MARGIN * 2 + puzzle.board_height * CELL + BTN_H
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Rush Hour — BFS Visualizer")
    clock = pygame.time.Clock()

    # State
    step = 0
    playing = True
    STEP_DELAY = 800  # milliseconds
    last_step_time = pygame.time.get_ticks()

    # Button
    button_rect = pygame.Rect(
        MARGIN + (puzzle.board_width * CELL - BTN_W) // 2,
        MARGIN + puzzle.board_height * CELL + 8,
        BTN_W, BTN_H
    )

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    step = 0
                    playing = True
                    last_step_time = current_time

        # Auto-advance steps
        if playing and current_time - last_step_time >= STEP_DELAY:
            if step < len(path) - 1:
                step += 1
                last_step_time = current_time
            else:
                playing = False

        # Display
        # Display
        info = f"Step: {step}/{len(path) - 1}"
        if not playing:
            info += "  |  Done!"

        # Draw everything
        draw_board(screen, font, path[step], button_rect, None)

        # Draw info text next to Restart button
        info_surf = font.render(info, True, TXT)
        info_x = button_rect.right + 20  # spacing to the right of button
        info_y = button_rect.centery - info_surf.get_height() // 2
        screen.blit(info_surf, (info_x, info_y))


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    run_ui()
