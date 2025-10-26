import time
from rush_hour import RushHourPuzzle
from BFS import bfs
from Astar import astar, h1, h2, h3


def run_console_example(csv_file: str = "examples/1.csv") -> None:
    """Run BFS and A* examples on a single puzzle."""
    puzzle = RushHourPuzzle(csv_file=csv_file)
    print(f"\n=== {csv_file} ===")
    print(f"Board size: {puzzle.board_height} x {puzzle.board_width}")
    puzzle.printBoard()
    print("Is goal state?", puzzle.isGoal())

    #BFS
    print("\nSolving with BFS...")
    start_time = time.perf_counter()
    node_bfs = bfs(puzzle, lambda s: s.successorFunction(), lambda s: s.isGoal())
    duration = time.perf_counter() - start_time

    if node_bfs:
        print(f"BFS solution found in {len(node_bfs.getSolution())} moves ({duration:.2f}s).")
    else:
        print(f"BFS found no solution. ({duration:.2f}s)")

    # A* with multiple heuristics
    for i, heuristic in enumerate([h1, h2, h3], start=1):
        print(f"\nRunning A* with h{i}...")
        start_time = time.perf_counter()
        node_astar = astar(puzzle, heuristic ,lambda s: s.successorFunction(), lambda s: s.isGoal())
        duration = time.perf_counter() - start_time

        if node_astar:
            print(f"A* (h{i}) solution: {len(node_astar.getSolution())} moves ({duration:.2f}s).")
        else:
            print(f"A* (h{i}) found no solution. ({duration:.2f}s)")


def compare_algos(csv_path: str) -> None:
    """Compare BFS and A* (h3) performance on a given puzzle."""
    print(f"\n=== Comparing algorithms on {csv_path} ===")
    puzzle = RushHourPuzzle(csv_file=csv_path)

    # BFS
    t1 = time.perf_counter()
    node_bfs = bfs(puzzle, lambda s: s.successorFunction(), lambda s: s.isGoal())
    t2 = time.perf_counter()
    bfs_moves = len(node_bfs.getSolution()) if node_bfs else None
    print(f"BFS: moves = {bfs_moves}, time = {t2 - t1:.2f}s")

    # A*
    t3 = time.perf_counter()
    node_astar = astar(puzzle, h3, lambda s: s.successorFunction(), lambda s: s.isGoal())
    t4 = time.perf_counter()
    astar_moves = len(node_astar.getSolution()) if node_astar else None
    print(f"A*: moves = {astar_moves}, time = {t4 - t3:.2f}s")


if __name__ == "__main__":
    run_console_example("examples/1.csv")

    examples = [
        "examples/1.csv",
        "examples/2-a.csv",
        "examples/2-b.csv",
        "examples/2-c.csv",
        "examples/2-d.csv",
        "examples/2-e.csv",
        "examples/e-f.csv",
    ]

    for ex in examples:
        compare_algos(ex)
