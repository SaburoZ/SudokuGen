import tkinter as tk
from tkinter import messagebox
from models.sudoku import Sudoku
from typing import List, Callable

class SudokuGUI:
    """Handles the graphical user interface for the Sudoku game."""

    CELL_COLORS = {
        'default': {'bg': "white", 'fg': "black"},
        'marked': {'bg': "black", 'fg': "white"},
        'error': {'bg': "red", 'fg': "red"},
        'hint': {'bg': "light blue", 'fg': "white"}
    }

    def __init__(self, size: int):
        self.sudoku = Sudoku(size)
        self.grid_data = self.sudoku.generate_grid()
        self.buttons: List[List[tk.Button]] = []
        self.setup_window()

    def setup_window(self):
        """Initializes the main window and frame."""
        self.root = tk.Tk()
        self.root.title("Sudoku Grid")
        self.root.configure(bg="#D2B48C")
        
        self.frame = tk.Frame(self.root, bg="#D2B48C", padx=10, pady=10)
        self.frame.pack(padx=10, pady=(0, 10))
        
        self.errors_var = tk.IntVar(value=0)
        self.correct_var = tk.IntVar(value=0)
        
        self.create_vertical_streaks()
        self.create_score_label()
        self.create_grid()

    def create_vertical_streaks(self):
        """Creates labels for vertical streaks."""
        for row in range(5):
            for col in range(self.sudoku.size):
                value = (self.sudoku.vertical_streaks[col][row] 
                        if row < len(self.sudoku.vertical_streaks[col]) else "")
                self.create_label(value, row + 2, col)

    def create_score_label(self):
        """Creates and positions the score label."""
        self.score_label = self.create_label(f"❌:{self.errors_var.get()}", 3, self.sudoku.size)

    def update_score(self):
        """Updates the displayed error count."""
        self.score_label.config(text=f"❌:{self.errors_var.get()}")

    def create_grid(self):
        """Creates the main grid of buttons."""
        for row in range(self.sudoku.size):
            row_buttons = []
            for col in range(self.sudoku.size):
                button = self.create_grid_button(row, col)
                row_buttons.append(button)
            
            # Add horizontal streak labels
            streak_text = " ".join(map(str, self.sudoku.horizontal_streaks[row]))
            self.create_label(streak_text, row + 5, self.sudoku.size, sticky="w", padx=5)
            self.buttons.append(row_buttons)

    def create_grid_button(self, row: int, col: int) -> tk.Button:
        """Creates a single grid button with proper configuration."""
        button = tk.Button(
            self.frame,
            text=" ",
            width=4,
            height=2,
            font=("Consolas", 15),
            **self.CELL_COLORS['default'],
            relief=tk.FLAT,
            command=lambda: self.handle_left_click(row, col)
        )
        button.grid(row=row + 5, column=col, padx=1, pady=1)
        button.bind("<Button-3>", lambda e: self.handle_right_click(row, col))
        return button

    def create_label(self, text: str, row: int, col: int, **kwargs) -> tk.Label:
        """Creates a label with standard styling."""
        label = tk.Label(
            self.frame, 
            text=text, 
            width=7 if 'width' not in kwargs else kwargs['width'],
            height=2 if 'height' not in kwargs else kwargs['height'],
            font=("Consolas", 15),
            bg="#D2B48C"
        )
        label.grid(row=row, column=col, **kwargs)
        return label

    def handle_left_click(self, row: int, col: int):
        """Handles left-click events on grid buttons."""
        button = self.buttons[row][col]
        current_bg = button.cget("bg")
        
        if current_bg != "white":
            return
            
        if self.grid_data[row][col] == 1:
            button.config(**self.CELL_COLORS['marked'])
            self.correct_var.set(self.correct_var.get() + 1)
            self.check_completion()
        else:
            button.config(**self.CELL_COLORS['error'])
            self.errors_var.set(self.errors_var.get() + 1)
            self.update_score()

    def handle_right_click(self, row: int, col: int):
        """Handles right-click events on grid buttons."""
        button = self.buttons[row][col]
        current_bg = button.cget("bg")
        
        if current_bg == "white":
            button.config(**self.CELL_COLORS['hint'])
        elif current_bg == "light blue":
            button.config(**self.CELL_COLORS['default'])

    def check_completion(self):
        """Checks if the puzzle has been completed."""
        if self.correct_var.get() == self.sudoku.total_correct:
            messagebox.showinfo("Game Complete", "Congratulations! You've completed the puzzle!")

    def run(self):
        """Starts the game."""
        self.root.mainloop()