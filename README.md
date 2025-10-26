# Rush Hour Solver Visualizer

A Python-based visualizer for the classic **Rush Hour puzzle**, supporting both **BFS** and **A\*** algorithms. See the solution path step by step, with a simple and interactive Pygame interface.

---

## 📘 Features

- Visual representation of the Rush Hour grid with cars, trucks, and walls.
- Supports multiple solving algorithms:
  - Breadth-First Search (**BFS**)
  - A\* search with customizable heuristics.
- Road-style background with lane markings for a visually appealing experience.

---

## 🎮 Demo

![Demo screenshot](assets/demo.png)

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/nadjibdje/RushHourGame.git
cd rush-hour-visualizer
```

2. Install dependencies (Python 3.10+ recommended):

```bash
pip install -r requirements.txt
```

3. Run the visualizer:

```bash
python ui.py
```

---

## 🚀 Usage

- Use the **BFS** or **A\*** buttons to solve the puzzle automatically.
- Watch each step progress on the grid.
- Click **Restart** to reset the board.
- Customize puzzle CSV files in the `examples/` folder.

---

## 📔 CSV Puzzle Format

- Each puzzle CSV describes the initial state of the board.
- Rows represent the board grid.
- Vehicles are defined by their **ID**, **row**, **column**, **length**, and **orientation** (`H` for horizontal, `V` for vertical).

---

## 💡 Future Improvements

- Add more vehicle types and sprites.
- Adjustable animation speed.
- Save/load puzzles and solutions.


