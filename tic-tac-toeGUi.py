import tkinter as tk
from tkinter import messagebox

def check_winner(board, player):
    win_pos = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    for pos in win_pos:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == player:
            return True
    return False

def is_draw(board):
    return all(cell != "" for cell in board)

def minimax(board, depth, is_ai):
    if check_winner(board, "O"):
        return 10 - depth
    if check_winner(board, "X"):
        return depth - 10
    if is_draw(board):
        return 0

    if is_ai:
        best_score = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth+1, False)
                board[i] = ""
                if score > best_score:
                    best_score = score
        return best_score
    else:
        best_score = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth+1, True)
                board[i] = ""
                if score < best_score:
                    best_score = score
        return best_score

def ai_move():
    best_score = -100
    best_move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    if best_move != -1:
        board[best_move] = "O"
        buttons[best_move].config(text="O", state="disabled")
        if check_winner(board, "O"):
            messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
            reset()
        elif is_draw(board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset()

def click(i):
    if board[i] == "":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")
        if check_winner(board, "X"):
            messagebox.showinfo("Tic-Tac-Toe", "You win!")
            reset()
        elif is_draw(board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset()
        else:
            ai_move()

def reset():
    for i in range(9):
        board[i] = ""
        buttons[i].config(text="", state="normal")

root = tk.Tk()
root.title("Tic-Tac-Toe\n(You: X | AI: O)")

board = [""] * 9
buttons = []

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", width=5, height=2, font=("Arial", 24),
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

reset_btn = tk.Button(root, text="Reset", width=10, command=reset)
reset_btn.pack(pady=10)

root.mainloop()
