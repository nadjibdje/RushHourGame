# main.py
from rush_hour import RushHourPuzzle
from BFS import bfs
from a import astar, h1, h2, h3

def run_console_example(csv_file="examples/2e.csv"):
    puzzle = RushHourPuzzle(csv_file=csv_file)
    print("Board size:", puzzle.board_height, "x", puzzle.board_width)
    puzzle.printBoard()
    print("Is goal state?", puzzle.isGoal())

    # BFS (use methods directly)
    print("\nSolving with BFS...")
    node_bfs = bfs(puzzle)  # uses default successor/isGoal
    if node_bfs:
        actions = node_bfs.getSolution()
        print("BFS solution length (moves):", len(actions))
        for i, a in enumerate(actions):
            print(f"{i+1}: {a}")
    else:
        print("BFS didn't find a solution.")

    # A* with h1, h2, h3
    print("\nRunning A* with h1...")
    node_h1 = astar(puzzle, h1)
    if node_h1:
        print("A* (h1) solution moves:", len(node_h1.getSolution()))
    else:
        print("A* (h1) no solution.")

    print("\nRunning A* with h2...")
    node_h2 = astar(puzzle, h2)
    if node_h2:
        print("A* (h2) solution moves:", len(node_h2.getSolution()))
    else:
        print("A* (h2) no solution.")

    print("\nRunning A* with h3...")
    node_h3 = astar(puzzle, h3)
    if node_h3:
        print("A* (h3) solution moves:", len(node_h3.getSolution()))
    else:
        print("A* (h3) no solution.")


if __name__ == "__main__":
    run_console_example("examples/2-e.csv")

# function  to compare execution time  between  bothe  algorithmes

import time
from a import h3

def compare_algos(csv_path):
    print(f"\n=== {csv_path} ===")
    puzzle = RushHourPuzzle(csv_file=csv_path)

    t1 = time.time()
    node_bfs = bfs(puzzle)
    t2 = time.time()
    print(f"BFS: moves = {len(node_bfs.getSolution()) if node_bfs else 'None'}, time = {t2-t1:.2f}s")

    t3 = time.time()
    node_astar = astar(puzzle, h3)
    t4 = time.time()
    print(f"A*: moves = {len(node_astar.getSolution()) if node_astar else 'None'}, time = {t4-t3:.2f}s")

# run on all examples
examples = ["examples/1.csv","examples/2-a.csv","examples/2-b.csv","examples/2-c.csv","examples/2-d.csv","examples/2-e.csv","examples/e-f.csv"]
for ex in examples:
    compare_algos(ex)
