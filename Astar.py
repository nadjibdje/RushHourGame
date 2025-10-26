# a.py
import heapq
from node import Node

def astar(initial_state, heuristic, successorFn, isGoal):
    """
    A* search.
    - initial_state: RushHourPuzzle
    - heuristic: function(state) -> number (h)
    - successorFn(state) -> list of (action, successor)  [optional]
    - isGoal(state) -> bool  [optional]
    Returns goal Node or None.
    """
    start = Node(initial_state, None, None, 0)
    start.setF(heuristic)

    open_list = []
    heapq.heappush(open_list, (start.f, start))
    g_costs = {initial_state.getStateKey(): 0}
    closed = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        cur_key = current.state.getStateKey()
        if cur_key in closed:
            continue

        if isGoal(current.state):
            return current

        closed.add(cur_key)

        for action, succ in successorFn(current.state):
            succ_key = succ.getStateKey()
            g_new = current.g + 1

            if succ_key in g_costs and g_new >= g_costs[succ_key]:
                continue

            child = Node(succ, current, action, g_new)
            child.setF(heuristic)

            g_costs[succ_key] = g_new

            heapq.heappush(open_list, (child.f, child))

    return None


# =========================
#        Heuristics
# =========================
def h1(state):
    """Distance in columns from rightmost cell of X to the board right edge (number of empty squares)."""
    red = next(v for v in state.vehicles if v["id"] == "X")
    distance = state.board_width - (red["col"] + red["length"])
    return distance

def h2(state):
    """h1 + number of distinct vehicles blocking the exit row in front of X."""
    red = next(v for v in state.vehicles if v["id"] == "X")
    y = red["row"]
    blocking_ids = set()
    for x in range(red["col"] + red["length"], state.board_width):
        cell = state.board[y][x]
        if cell != " " and cell != "#":
            blocking_ids.add(cell)
    return h1(state) + len(blocking_ids)

def can_vehicle_move(state, vehicle):
    """Check if a vehicle has at least one free move (used by h3)."""
    r, c = vehicle["row"], vehicle["col"]
    length, orient = vehicle["length"], vehicle["orientation"]

    if orient == "H":
        # left
        if c - 1 >= 0 and state.board[r][c - 1] == " ":
            return True
        # right
        if c + length < state.board_width and state.board[r][c + length] == " ":
            return True
    else:
        # up
        if r - 1 >= 0 and state.board[r - 1][c] == " ":
            return True
        # down
        if r + length < state.board_height and state.board[r + length][c] == " ":
            return True
    return False

def h3(state):
    """
    Improved heuristic: h2 + penalty for blocking vehicles that are themselves blocked.
    Encourages moves that free blockers.
    """
    red = next(v for v in state.vehicles if v["id"] == "X")
    y = red["row"]
    blocking_ids = set()
    penalty = 0
    for x in range(red["col"] + red["length"], state.board_width):
        cell = state.board[y][x]
        if cell != " " and cell != "#":
            blocking_ids.add(cell)

    # For each blocking vehicle, check if it can move at all in current state
    for bid in blocking_ids:
        vehicle = next(v for v in state.vehicles if v["id"] == bid)
        if not can_vehicle_move(state, vehicle):
            penalty += 1

    return h1(state) + len(blocking_ids) + penalty