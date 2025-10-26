import csv
from copy import deepcopy

class RushHourPuzzle:
    def __init__(self,csv_file=None):
        self.board_height = 0
        self.board_width = 0
        self.vehicles = [] 
        self.walls = []     
        self.board = []     
        if csv_file:
            self.setVehicles(csv_file)
            self.setBoard()

    def setVehicles(self, csv_file):
        """Reads the CSV and generates vehicles and walls lists; sets board dimensions."""
        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            
            # First row = board size
            first_row = next(reader)
            self.board_height, self.board_width = map(int, first_row)

            # Read remaining rows
            for row in reader:
                row = [cell.strip() for cell in row if cell.strip()]
                if not row:
                    continue
                if row[0] == "#":
                    c,r = int(row[1]), int(row[2])
                    self.walls.append((r, c))
                else:
                    vid = row[0]
                    c,r = int(row[1]), int(row[2])
                    orientation = row[3]
                    length = int(row[4])
                    vehicle = {"id": vid, "row": r, "col": c, "orientation": orientation, "length": length}
                    self.vehicles.append(vehicle)

    def setBoard(self):
        # Initialize empty board
        self.board = [[" " for _ in range(self.board_width)] for _ in range(self.board_height)]

        # Place walls
        for r, c in self.walls:
            if 0 <= r < self.board_height and 0 <= c < self.board_width:
                self.board[r][c] = "#"

        # Place vehicles
        for v in self.vehicles:
            r, c = v["row"], v["col"]
            length = v["length"]
            orientation = v["orientation"]
            can_place = True

            # Check bounds and overlap
            for i in range(length):
                r_pos = r + i if orientation == "V" else r
                c_pos = c + i if orientation == "H" else c
                if r_pos >= self.board_height or c_pos >= self.board_width or self.board[r_pos][c_pos] != " ":
                    can_place = False
                    break

            # Place vehicle if possible
            if can_place:
                for i in range(length):
                    r_pos = r + i if orientation == "V" else r
                    c_pos = c + i if orientation == "H" else c
                    self.board[r_pos][c_pos] = v["id"]
            else:
                print(f"Cannot place vehicle {v['id']} at ({r},{c})!")

    def isGoal(self):
        for v in self.vehicles:
            if v["id"] == "X":
                if v["orientation"] != "H":
                    return False
                c = v["col"]
                length = v["length"] 
                if (c == self.board_width - length):
                    return True
        return False
        
    def printBoard(self):
        print("\nBoard:")
        print("   " + " ".join(f"{c}" for c in range(self.board_width)))
        print("  " + "--" * self.board_width)
        for r in range(self.board_height):
            row_str = f"{r}| " + " ".join(self.board[r])
            print(row_str)

    def successorFunction(self):
        successors = []
        for v in self.vehicles:
            vid = v["id"]
            r, c = v["row"], v["col"]
            length = v["length"]
            orientation = v["orientation"]

            if orientation == "H":
                if c + length < self.board_width and self.board[r][c + length] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["col"] += 1
                            break
                    new_puzzle.setBoard()
                    action = f"Move {vid} right"
                    successors.append((action, new_puzzle))
                if c - 1 >= 0 and self.board[r][c - 1] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["col"] -= 1
                            break
                    new_puzzle.setBoard()
                    action = f"Move {vid} left"
                    successors.append((action, new_puzzle))

            elif orientation == "V":
                if r + length < self.board_height and self.board[r + length][c] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["row"] += 1
                            break
                    new_puzzle.setBoard()
                    action = f"Move {vid} down"
                    successors.append((action, new_puzzle))
                    
                if r - 1 >= 0 and self.board[r - 1][c] == " ":
                    new_puzzle = deepcopy(self)
                    for nv in new_puzzle.vehicles:
                        if nv["id"] == vid:
                            nv["row"] -= 1
                            break
                    new_puzzle.setBoard()
                    action = f"Move {vid} up"
                    successors.append((action, new_puzzle))

        return successors
    
    def getStateKey(self):
        return tuple(tuple(row) for row in self.board)