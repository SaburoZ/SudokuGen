from random import choice
from typing import List, Union

class Sudoku:
    """Represents a Sudoku puzzle grid with streak calculations."""
    
    MIN_SIZE = 5
    MAX_SIZE = 10
    
    def __init__(self, size: int):
        self.size = size
        self.grid_data: List[List[int]] = []
        self.vertical_streaks = [[] for _ in range(self.size)]
        self.horizontal_streaks: List[List[int]] = []
        self.total_correct = 0

    def validate_size(self) -> Union[str, None]:
        """Validates if the grid size is within acceptable bounds."""
        if self.size > self.MAX_SIZE:
            return f'The grid is too big, it must be under {self.MAX_SIZE + 1} cells'
        elif self.size < self.MIN_SIZE:
            return f'The grid is too small, it must be over {self.MIN_SIZE - 1} cells'
        return None

    def calculate_streaks(self, row: List[int], row_index: int, vertical_list: List[int]) -> List[int]:
        """Calculates horizontal and vertical streaks for a given row."""
        point = 0
        horizontal_streak = []

        for col_index, cell_value in enumerate(row):
            if cell_value == 1:
                self.total_correct += 1
                point += 1
                vertical_list[col_index] += 1
            else:
                if point > 0:
                    horizontal_streak.append(point)
                point = 0

                if vertical_list[col_index] > 0:
                    self.vertical_streaks[col_index].append(vertical_list[col_index])
                    vertical_list[col_index] = 0

        if point > 0:
            horizontal_streak.append(point)
            
        return horizontal_streak

    def generate_grid(self) -> Union[str, List[List[int]]]:
        """Generates a new Sudoku grid with calculated streaks."""
        if error_message := self.validate_size():
            return error_message

        self.grid_data = []
        self.total_correct = 0
        vertical_list = [0 for _ in range(self.size)]
        
        # Generate grid and calculate streaks
        for i in range(self.size):
            row_data = [choice([0, 1, 1]) for _ in range(self.size)]
            horizontal_streak = self.calculate_streaks(row_data, i, vertical_list)
            
            self.horizontal_streaks.append(horizontal_streak)
            self.grid_data.append(row_data)

        # Add remaining vertical streaks
        for col_index, count in enumerate(vertical_list):
            if count > 0:
                self.vertical_streaks[col_index].append(count)

        return self.grid_data