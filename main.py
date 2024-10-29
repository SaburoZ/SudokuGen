import tkinter as tk
from random import choice
from tkinter import messagebox


class Sudoku:
    def __init__(self, size):
        self.size = size
        self.grid_data = []
        self.vertical_streaks = [[] for _ in range(self.size)]
        self.horizontal_streaks = []
        self.total_correct = 0

    def generate_grid(self):
        if self.size > 10:
            return 'The grid is too big, it must be under 11 cells'
        elif self.size < 5:
            return 'The grid is too small, it must be over 4 cells'

        self.grid_data = []
        vertical_list = [0 for _ in range(self.size)]

        # Create the grid and calculate the vertical and horizontal streaks
        for i in range(self.size):
            row_data = []
            point = 0
            horizontal_streak = []

            for f in range(self.size):
                options = [0, 1, 1]
                rand_int = choice(options)
                row_data.append(rand_int)

                if rand_int == 1:
                    self.total_correct += 1
                    point += 1
                    vertical_list[f] += 1
                else:
                    if point > 0:
                        horizontal_streak.append(point)
                    point = 0

                    if vertical_list[f] > 0:
                        self.vertical_streaks[f].append(vertical_list[f])
                        vertical_list[f] = 0

            # Store horizontal streaks for the row
            if point > 0:
                horizontal_streak.append(point)
            self.horizontal_streaks.append(horizontal_streak)

            self.grid_data.append(row_data)

        # Add remaining vertical streaks
        for f in range(self.size):
            if vertical_list[f] > 0:
                self.vertical_streaks[f].append(vertical_list[f])

        return self.grid_data


def update_button(r, c, buttons, grid_data, errors_var, correct_var, sudoku, update_score):
    current_bg = buttons[r][c].cget("bg")
    if current_bg == "white" and grid_data[r][c] == 1:
        buttons[r][c].config(bg="black", fg="white")
        correct_var.set(correct_var.get() + 1)
        check_completion(sudoku, correct_var)
    elif current_bg == "white" and grid_data[r][c] != 1:
        buttons[r][c].config(bg="red", fg="red")
        errors_var.set(errors_var.get() + 1)
        update_score()
    elif current_bg == "black":
        return


def check_completion(sudoku, correct_var):
    if correct_var.get() == sudoku.total_correct:
        messagebox.showinfo("Game Complete", "Congratulations! You've completed the puzzle!")


def right_click_button(event, r, c, buttons):
    if buttons[r][c].cget("bg") == "white":
        buttons[r][c].config(bg="light blue", fg="white")
    elif buttons[r][c].cget("bg") == "light blue":
        buttons[r][c].config(bg="white", fg="black")  # Toggle off if clicked again


def display_sudoku(size):
    sudoku = Sudoku(size)
    grid_data = sudoku.generate_grid()

    # Main window
    root = tk.Tk()
    root.title("Sudoku Grid")
    root.configure(bg="#D2B48C")

    # A frame to hold the grid and add padding
    frame = tk.Frame(root, bg="#D2B48C", padx=10, pady=10)
    frame.pack(padx=10, pady=(0, 10))

    buttons = []
    errors_var = tk.IntVar(value=0)  # Track errors using a Tkinter variable
    correct_var = tk.IntVar(value=0)

    # Top section (for vertical streaks)
    for row in range(5):
        for col in range(size):
            if row < len(sudoku.vertical_streaks[col]):
                value = sudoku.vertical_streaks[col][row]
            else:
                value = ""
            label = tk.Label(frame, text=value, width=3, height=1, font=("Consolas", 15), bg="#D2B48C")
            label.grid(row=row + 2, column=col, sticky="n")

    # Display initial score label
    score_label = tk.Label(frame, text=f"❌:{errors_var.get()}", width=8, height=1, font=("Consolas", 15), bg="#D2B48C")
    score_label.grid(row=3, column=size)

    # Update score display dynamically
    def update_score():
        score_label.config(text=f"❌:{errors_var.get()}")

    # Create a grid of buttons and the right-side horizontal streak labels
    for r in range(size):
        row_buttons = []
        for c in range(size):
            button = tk.Button(
                frame,
                text=" ",
                width=4,
                height=2,
                font=("Consolas", 15),
                bg="white",
                fg="black",
                relief=tk.FLAT,
                command=lambda r=r, c=c: update_button(r, c, buttons, grid_data, errors_var, correct_var, sudoku, update_score)
            )
            button.grid(row=r + 5, column=c, padx=1, pady=1)  # Padding between buttons
            button.bind("<Button-3>", lambda e, r=r, c=c: right_click_button(e, r, c, buttons))
            row_buttons.append(button)

        # Horizontal streaks on the right side
        horizontal_streak = " ".join(map(str, sudoku.horizontal_streaks[r]))
        label = tk.Label(frame, text=horizontal_streak, width=7, height=2, font=("Consolas", 15), bg="#D2B48C")
        label.grid(row=r + 5, column=size, sticky="w", padx=5)
        buttons.append(row_buttons)

    # Start the Tkinter main loop
    root.mainloop()


# Display the Sudoku grid in a window
display_sudoku(5)

