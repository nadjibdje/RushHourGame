# BFS.py
from collections import deque
from node import Node

def bfs(initial_state, successorFn=None, isGoal=None):
    """
    BFS that accepts:
      - initial_state : RushHourPuzzle
      - successorFn(state) -> list of (action, successor_state)  [optional]
      - isGoal(state) -> bool  [optional]
    If successorFn/isGoal are None, use initial_state methods.
    Returns Node (goal) or False if none.
    """
    if successorFn is None:
        successorFn = lambda s: s.successorFunction()
    if isGoal is None:
        isGoal = lambda s: s.isGoal()

    Open = deque()
    visited = set()

    init_node = Node(state=initial_state, parent=None, action=None, g=0)
    if isGoal(init_node.state):
        return init_node

    visited.add(init_node.state.getStateKey())
    Open.append(init_node)

    while Open:
        current = Open.popleft()

        for (action, successor) in successorFn(current.state):
            key = successor.getStateKey()
            if key in visited:
                continue

            child = Node(state=successor, parent=current, action=action, g=current.g + 1)

            if isGoal(child.state):
                return child

            visited.add(key)
            Open.append(child)

    return False
