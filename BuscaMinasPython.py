import tkinter as tk
import random
from tkinter import messagebox

class Buscaminas:
    def __init__(self, root, rows, cols, mines):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0] * cols for _ in range(rows)]
        self.discovered = [[False] * cols for _ in range(rows)]
        self.flags = [[False] * cols for _ in range(rows)]
        self.create_board()
        self.create_gui()

    def create_board(self):
        # Colocar minas aleatorias
        mine_positions = random.sample(range(self.rows * self.cols), self.mines)
        for position in mine_positions:
            row, col = divmod(position, self.cols)
            self.board[row][col] = -1  # -1 indica una mina
            for i in range(row-1, row+2):
                for j in range(col-1, col+2):
                    if 0 <= i < self.rows and 0 <= j < self.cols and self.board[i][j] != -1:
                        self.board[i][j] += 1

    def create_gui(self):
        self.buttons = [[tk.Button(self.root, text=" ", width=3, height=2,
                                   command=lambda row=row, col=col: self.click(row, col))
                         for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].grid(row=row, column=col)
                self.buttons[row][col].bind("<Button-3>", lambda event, row=row, col=col: self.mark_mine(row, col))

    def click(self, row, col):
        if self.board[row][col] == -1:
            self.show_mines()
            messagebox.showinfo("¡Perdiste!", "Has tocado una mina. ¡Juego terminado!")
            self.root.destroy()
        else:
            self.discover_cells(row, col)
            self.check_win()

    def mark_mine(self, row, col):
        if not self.discovered[row][col]:
            if not self.flags[row][col]:
                self.buttons[row][col].config(text="🚩", state=tk.DISABLED, relief=tk.SUNKEN)
                self.flags[row][col] = True
            else:
                self.buttons[row][col].config(text=" ", state=tk.NORMAL, relief=tk.RAISED)
                self.flags[row][col] = False

    def discover_cells(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols) or self.discovered[row][col]:
            return

        self.discovered[row][col] = True
        self.buttons[row][col].config(text=str(self.board[row][col]), state=tk.DISABLED, relief=tk.SUNKEN)

        if self.board[row][col] == 0:
            for i in range(row-1, row+2):
                for j in range(col-1, col+2):
                    self.discover_cells(i, j)

    def show_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.buttons[row][col].config(text="💣", state=tk.DISABLED, relief=tk.SUNKEN)

    def check_win(self):
        undiscovered_count = sum(row.count(False) for row in self.discovered)
        if undiscovered_count == self.mines:
            messagebox.showinfo("¡Ganaste!", "Has encontrado todas las minas. ¡Juego terminado!")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Buscaminas")
    game = Buscaminas(root, rows=8, cols=8, mines=10)
    root.mainloop()
