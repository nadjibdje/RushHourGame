# rush_hour.py
import csv
from copy import deepcopy

class RushHourPuzzle:
    def __init__(self, csv_file=None):
        self.board_height = 0
        self.board_width = 0
        self.vehicles = []  # List of vehicle dicts: {"id","row","col","orientation","length"}
        self.walls = []     # List of (row, col)
        self.board = []     # 2D board matrix
        if csv_file:
            self.setVehicles(csv_file)
            self.setBoard()

    def setVehicles(self, csv_file):
        """Reads CSV: first row -> height,width ; next rows -> vehicles or walls.
        Vehicle row format expected: id, col, row, orientation(H/V), length
        Wall row format expected: '#', col, row
        """
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            # first non-empty row -> board dims
            first_row = None
            for row in reader:
                row = [c.strip() for c in row if c.strip() != ""]
                if row:
                    first_row = row
                    break
            if not first_row:
                raise ValueError("CSV vide ou mal formatté")
            self.board_height, self.board_width = map(int, first_row)

            # remaining rows
            for row in reader:
                row = [c.strip() for c in row if c.strip() != ""]
                if not row:
                    continue
                if row[0] == "#":
                    c, r = int(row[1]), int(row[2])
                    self.walls.append((r, c))
                else:
                    vid = row[0]
                    c, r = int(row[1]), int(row[2])
                    orientation = row[3].upper()
                    length = int(row[4])
                    vehicle = {"id": vid, "row": r, "col": c, "orientation": orientation, "length": length}
                    self.vehicles.append(vehicle)

    def setBoard(self):
        # create empty board
        self.board = [[" " for _ in range(self.board_width)] for _ in range(self.board_height)]

        # walls
        for r, c in self.walls:
            if 0 <= r < self.board_height and 0 <= c < self.board_width:
                self.board[r][c] = "#"

        # vehicles (place them if possible)
        for v in self.vehicles:
            r, c = v["row"], v["col"]
            length = v["length"]
            orient = v["orientation"]
            can_place = True
            coords = []
            for i in range(length):
                rr = r + i if orient == "V" else r
                cc = c + i if orient == "H" else c
                if not (0 <= rr < self.board_height and 0 <= cc < self.board_width):
                    can_place = False
                    break
                if self.board[rr][cc] != " ":
                    can_place = False
                    break
                coords.append((rr, cc))
            if can_place:
                for (rr, cc) in coords:
                    self.board[rr][cc] = v["id"]
            else:
                # warning but continue
                print(f"Warning: cannot place vehicle {v['id']} at ({r},{c})")

    def isGoal(self):
        # Goal: red car 'X' is horizontal and its rightmost cell reaches board_width
        for v in self.vehicles:
            if v["id"] == "X":
                if v["orientation"] != "H":
                    return False
                c = v["col"]
                length = v["length"]
                # rightmost column index of X is c + length - 1 ; goal when equals board_width - 1
                if c + length == self.board_width:
                    return True
        return False

    def printBoard(self):
        # print columns
        print("\nBoard:")
        print("   " + " ".join(str(c) for c in range(self.board_width)))
        print("  " + "--" * self.board_width)
        for r in range(self.board_height):
            print(f"{r}| " + " ".join(self.board[r]))
        print("  " + "--" * self.board_width)

    def successorFunction(self):
        """Return list of (action_str, new_state) for moving each vehicle by one step if possible."""
        successors = []
        for v in self.vehicles:
            vid = v["id"]
            r, c = v["row"], v["col"]
            length = v["length"]
            orient = v["orientation"]

            if orient == "H":
                # move right
                if c + length < self.board_width and self.board[r][c + length] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["col"] += 1
                            break
                    new_puzzle.setBoard()
                    action = (vid, "R")
                    successors.append((action, new_puzzle))
                # move left
                if c - 1 >= 0 and self.board[r][c - 1] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["col"] -= 1
                            break
                    new_puzzle.setBoard()
                    action = (vid, "L")
                    successors.append((action, new_puzzle))

            else:  # V
                # move down
                if r + length < self.board_height and self.board[r + length][c] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["row"] += 1
                            break
                    new_puzzle.setBoard()
                    action = (vid, "D")
                    successors.append((action, new_puzzle))
                # move up
                if r - 1 >= 0 and self.board[r - 1][c] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["row"] -= 1
                            break
                    new_puzzle.setBoard()
                    action = (vid, "U")
                    successors.append((action, new_puzzle))

        return successors

    def getStateKey(self):
        """Return compact state key: tuple of (id,row,col) sorted by id.
           Faster and robust vs using full board matrix."""
        key = tuple((v["id"], v["row"], v["col"]) for v in sorted(self.vehicles, key=lambda x: x["id"]))
        return key
