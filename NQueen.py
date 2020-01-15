from tkinter import *
import time
from PIL import Image, ImageTk

root = Tk()
root.title("N-Queen")
root.resizable(False, False)


class Board():
    def __init__(self, n, x):
        self.size = n
        self.speed = x
        self.r = [None] * n
        self.board_frame = Frame(root, height=50 * n, width=50 * n)
        self.board = [[0 for i in range(n)] for j in range(n)]
        self.chess_board = Canvas(self.board_frame, height=50 * n, width=50 * n, bg="white")
        self.image = Image.open("queen.png")
        self.image = self.image.resize((50, 50), Image.ANTIALIAS)
        self.queen = ImageTk.PhotoImage(self.image)
        self.btn_play = Button(self.board_frame, text="Play", width=8, command=lambda: self.nqueen(0))
        self.btn_reset = Button(self.board_frame, text="Reset", width=8, command=lambda: self.reset())
        self.btn_back = Button(self.board_frame, text="Back", width=8, command=lambda: self.back())

    def back(self):
        # global input_frame
        input_frame.grid(row=0, column=0)
        self.board_frame.grid_forget()

    def create_board(self, n):
        for i in range(n):
            for j in range(n):
                self.chess_board.create_rectangle(i * 50, j * 50, i * 50 + 50, 50 + j * 50,
                                                  fill="brown" if (i - j) % 2 == 0 else "white", outline="")
        self.board_frame.grid(row=0, column=0)
        self.chess_board.pack()
        self.btn_play.pack(side=LEFT, pady=2,padx=2)
        self.btn_reset.pack(side=LEFT, pady=2,padx=2)
        self.btn_back.pack(side=RIGHT, pady=2,padx=2)
        # print(self.board)

    def is_safe(self, row, col):
        # Check this row on left side
        for i in range(col):
            if self.board[row][i] == 1:
                return False

        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1),
                        range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        # Check lower diagonal on left side
        for i, j in zip(range(row, self.size, 1),
                        range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False
        return True

    def reset(self):
        self.board_frame.grid_forget()
        start()

    # solver for the nqueen problem
    def nqueen(self, col):
        self.btn_play.configure(state=DISABLED)
        if col >= self.size:
            return True
        self.r[col] = self.chess_board.create_image(col * 50 + 25, 25, image=self.queen)
        time.sleep(self.speed)
        root.update()
        for i in range(self.size):
            if i > 0:
                self.chess_board.move(self.r[col], 0, 50)
                time.sleep(self.speed)
                root.update()
            if self.is_safe(i, col):
                self.board[i][col] = 1

                if self.nqueen(col + 1) == True:
                    return True

                self.board[i][col] = 0
        self.chess_board.delete(self.r[col])
        time.sleep(self.speed)
        root.update()
        return False


def value(v):
    if v == "high":
        return 0.2
    if v == "medium":
        return 0.6
    return 1


def start():
    n = min(max(int(e.get()), 4), 12)  # input by the user
    e.delete(0, END)
    e.insert(0, n)
    v = var.get()
    x = value(v)
    board = Board(n, x)
    board.create_board(n)  # create the chess board
    input_frame.grid_forget()


# frame which takes number of queen as input
input_frame = Frame(root)
label1 = Label(input_frame, text="Enter number of queens (4-12):")
label1.grid(row=0, column=0,padx=2,pady=2)
e = Entry(input_frame, width=10)
e.grid(row=0, column=1)
label2 = Label(input_frame, text="Enter speed of execution :")
label2.grid(row=1, column=0)

var = StringVar(input_frame)
var.set("medium")  # default value

option = OptionMenu(input_frame, var, "high", "medium", "low")
option.grid(row=1, column=1, pady=2)
btn_start = Button(input_frame, text="Run",width=10, command=start)
btn_start.grid(row=2, column=0,pady=2)
input_frame.grid(row=0, column=0)
root.mainloop()
