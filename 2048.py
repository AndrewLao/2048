import tkinter as tk
import random

EMPTY_COLOR = "#8eaba8"

LABEL_FONT = ("Verdana", 20)

TITLE_FONT = ("Verdana", 40, "bold")

TILE_COLORS = {2: "#daeddf", 4: "#9ae3ae", 8: "#6ce68d", 16: "#42ed71", 32: "#17e650", 64: "#17c246", 128: "#149938",
               256: "#107d2e", 512: "#0e6325", 1024: "#0b4a1c", 2048: "#031f0a", 4096: "#000000", 8192: "#000000"}
LABEL_COLORS = {2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08", 32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0", 2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0"}


class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")

        self.main_grid = tk.Frame(self, bg="#a6bdbb", bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.make_interface()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def make_interface(self):
        self.cells = []
        for i in range(4):
            rows = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg=EMPTY_COLOR, width=150, height=150)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=EMPTY_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                rows.append(cell_data)
            self.cells.append(rows)

        # score
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=TITLE_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=LABEL_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        # initialize
        self.matrix = [[0] * 4 for _ in range(4)]
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=TILE_COLORS[2])
        self.cells[row][col]["number"].configure(bg=TILE_COLORS[2], fg=LABEL_COLORS[2], text="2", font=LABEL_FONT)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=TILE_COLORS[2])
        self.cells[row][col]["number"].configure(bg=TILE_COLORS[2], fg=LABEL_COLORS[2], text="2", font=LABEL_FONT)
        self.score = 0

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # add new tile 2 or 4 randomly
    def add_new(self):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = random.choice([2, 4])

    def update_interface(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=EMPTY_COLOR)
                    self.cells[i][j]["number"].configure(bg=EMPTY_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=TILE_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=TILE_COLORS[cell_value], fg=LABEL_COLORS[cell_value], text=str(cell_value), font=LABEL_FONT
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new()
        self.update_interface()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new()
        self.update_interface()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new()
        self.update_interface()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new()
        self.update_interface()
        self.game_over()

    def move_checks(self):
        for i in range(4):  # horizontal moves exist?
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        for i in range(3):  # vertical moves exist?
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Win!", bg=EMPTY_COLOR, fg=LABEL_COLORS[8192], font=TITLE_FONT).pack()
        elif any(0 in row for row in self.matrix) and not self.move_checks():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="You Lose!", bg=EMPTY_COLOR, fg=LABEL_COLORS[8192], font=TITLE_FONT).pack()


def main():
    Game()


if __name__ == "__main__":
    main()
