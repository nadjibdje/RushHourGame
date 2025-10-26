import pygame
from rush_hour import RushHourPuzzle
from BFS import bfs
from a import astar, h3  # on utilise h3 par défaut, tu peux changer

# === CONSTANTS ===
csv_file = "examples/2-c.csv"
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
BTN_BG_DISABLED = (160, 160, 160)
BTN_TXT = (255, 255, 255)
BTN_RADIUS = 10


# === DRAW FUNCTION ===
def draw_board(screen, font, state: RushHourPuzzle):
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

    # Draw Walls
    for (r, c) in state.walls:
        x = MARGIN + c * CELL + PADDING
        y = MARGIN + r * CELL + PADDING
        w = CELL - 2 * PADDING
        h = CELL - 2 * PADDING
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, (80, 80, 80), rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=10)

    # Draw Vehicles
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


# === BUTTON DRAW ===
def draw_button(screen, font, rect, text, enabled=True):
    mx, my = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mx, my)
    color = BTN_BG_DISABLED if not enabled else (BTN_BG_HOVER if is_hover else BTN_BG)
    pygame.draw.rect(screen, color, rect, border_radius=BTN_RADIUS)
    txt = font.render(text, True, BTN_TXT)
    screen.blit(txt, (rect.x + (rect.width - txt.get_width()) // 2,
                      rect.y + (rect.height - txt.get_height()) // 2))


# === MAIN FUNCTION ===
def run_ui():
    puzzle = RushHourPuzzle(csv_file=csv_file)

    pygame.init()
    font = pygame.font.SysFont(None, 26)

    W = MARGIN * 2 + puzzle.board_width * CELL
    H = MARGIN * 2 + puzzle.board_height * CELL + BTN_H + 20
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Rush Hour — Solver Visualizer")
    clock = pygame.time.Clock()

    # Buttons
    bfs_btn = pygame.Rect(W // 2 - BTN_W - 10, MARGIN + puzzle.board_height * CELL + 8, BTN_W, BTN_H)
    astar_btn = pygame.Rect(W // 2 + 10, MARGIN + puzzle.board_height * CELL + 8, BTN_W, BTN_H)
    restart_btn = pygame.Rect(W // 2 - BTN_W // 2, MARGIN + puzzle.board_height * CELL + 8, BTN_W, BTN_H)

    # States
    path = None
    step = 0
    playing = False
    solving = False
    algo = None
    STEP_DELAY = 800
    last_step_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # === BFS Button ===
                if bfs_btn.collidepoint(event.pos) and not solving and not playing:
                    solving = True
                    algo = "BFS"
                    print("Solving with BFS...")
                    node = bfs(puzzle, RushHourPuzzle.successorFunction, RushHourPuzzle.isGoal)
                    if node:
                        path = node.getPath()
                        print(f"BFS found solution in {len(path) - 1} steps.")
                    else:
                        print("No solution found.")
                    solving = False
                    playing = True
                    step = 0

                # === A* Button ===
                elif astar_btn.collidepoint(event.pos) and not solving and not playing:
                    solving = True
                    algo = "A*"
                    print("Solving with A* (h3)...")
                    node = astar(puzzle, h3)
                    if node:
                        path = node.getPath()
                        print(f"A* found solution in {len(path) - 1} steps.")
                    else:
                        print("No solution found.")
                    solving = False
                    playing = True
                    step = 0

                # === Restart Button ===
                elif path and restart_btn.collidepoint(event.pos) and not solving:
                    puzzle = RushHourPuzzle(csv_file=csv_file)
                    path = None
                    algo = None
                    playing = False
                    solving = False
                    step = 0

        # Auto-advance steps
        if playing and not solving and path and current_time - last_step_time >= STEP_DELAY:
            if step < len(path) - 1:
                step += 1
                last_step_time = current_time
            else:
                playing = False

        # === DRAW ===
        draw_board(screen, font, puzzle if not path else path[step])

        if not path:
                draw_button(screen, font, bfs_btn, "Solve with BFS", enabled=not solving)
                draw_button(screen, font, astar_btn, "Solve with A*", enabled=not solving)
        else:
                draw_button(screen, font, restart_btn, "Restart", enabled=not solving)
                info = f"{algo} | Step: {step}/{len(path) - 1}"
                info_surf = font.render(info, True, TXT)
                screen.blit(info_surf, (restart_btn.right + 20, restart_btn.centery - info_surf.get_height() // 2))

                if not playing:
                    done_surf = font.render("Done!", True, TXT)
                    screen.blit(done_surf, (restart_btn.right + 20, restart_btn.centery + info_surf.get_height()))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    run_ui()
