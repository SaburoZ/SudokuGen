# Sudoku Game

A simple Sudoku game implemented in Python using Tkinter for the graphical user interface. The game allows users to fill in a randomly generated Sudoku grid while keeping track of correct entries and errors.

## Features

- Randomly generated Sudoku puzzles with sizes ranging from 5 to 10.
- Interactive GUI for user input with feedback on correctness.
- Streak tracking for horizontal and vertical sequences of correct entries.
- Visual indicators for correct (black) and incorrect (light red) answers.
- Completion message displayed upon solving the puzzle.

## Technologies Used

- **Python**: Programming language for implementation.
- **Tkinter**: Standard GUI toolkit for Python.
- **Random**: Module to generate random cell values.

## File Structure

```
sudoku_game/
├── gui.py             # Main file for the GUI
├── game_logic.py      # Logic for handling user interactions
└── sudoku.py          # Sudoku grid generation and tracking
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sudoku_game.git
   cd sudoku_game
   ```

2. Ensure you have Python installed on your system.

3. Run the game:
   ```bash
   python gui.py
   ```

## How to Play

- Left-click on a cell to fill it in. 
- Right-click on a cell to temporarily mark it.
- The game will track your correct entries and errors.
- A completion message will appear when you correctly fill in all cells.
