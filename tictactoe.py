import tkinter

def create_symbol_selection():
    global playerX, playerO, curr_player
    
    symbol_window = tkinter.Toplevel(window)
    symbol_window.title("Choose Symbol")
    symbol_window.resizable(False, False)
    symbol_window.config(bg=color_gray)
    symbol_window.grab_set()
    
    tkinter.Label(symbol_window, text="Choose X or O:", font=("Consolas", 20), 
                 bg=color_gray, fg="white").pack(pady=10)
    frame = tkinter.Frame(symbol_window, bg=color_gray)
    frame.pack(pady=5)
    
    def set_symbol(symbol):
        global playerX, playerO, curr_player
        playerX, playerO = (symbol, "O" if symbol == "X" else "X")
        curr_player = playerX
        symbol_window.destroy()
        create_widgets()
        if curr_player == playerO:
            window.after(500, get_ai_move)
    
    for symbol in ["X", "O"]:
        tkinter.Button(frame, text=symbol, font=("Consolas", 50, "bold"), 
                      fg=color_blue if symbol == "X" else color_yellow, 
                      bg=color_gray, width=4, height=1,
                      command=lambda s=symbol: set_symbol(s)).pack(side=tkinter.LEFT, padx=10)

def create_widgets():
    global label, board, button
    
    frame = tkinter.Frame(window)
    label = tkinter.Label(frame, text=curr_player + "'s turn", font=("Consolas", 20), 
                         background=color_gray, foreground="white")
    label.grid(row=0, column=0, columnspan=3, sticky="we")
    
    board = [[tkinter.Button(frame, text="", font=("Consolas", 50, "bold"),
                           background=color_gray, foreground=color_blue, 
                           width=4, height=1,
                           command=lambda r=row, c=col: set_tile(r, c))
             for col in range(3)] for row in range(3)]
    
    for row in range(3):
        for col in range(3):
            board[row][col].grid(row=row + 1, column=col)
    
    button = tkinter.Button(frame, text="Restart", font=("Consolas", 20), 
                          background=color_gray, foreground="white", 
                          command=new_game)
    button.grid(row=4, column=0, columnspan=3, sticky="we")
    
    frame.pack()
    center_window()

def center_window():
    window.update()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def set_tile(row, column):
    global curr_player

    if game_over or board[row][column]["text"] != "":
        return

    board[row][column]["text"] = curr_player
    board[row][column].config(foreground=color_yellow if curr_player == "O" else color_blue)
    check_winner()

    if not game_over:
        curr_player = playerO if curr_player == playerX else playerX
        label["text"] = "AI is thinking..." if curr_player == playerO else curr_player + "'s turn"
        if curr_player == playerO:
            window.after(500, get_ai_move)

def get_ai_move():
    best_score, move = float('-inf'), None

    for row in range(3):
        for col in range(3):
            if board[row][col]["text"] == "":
                board[row][col]["text"] = playerO
                score = minimax(0, False, float('-inf'), float('inf'))
                board[row][col]["text"] = ""
                if score > best_score:
                    best_score, move = score, (row, col)

    if move:
        set_tile(move[0], move[1])

def minimax(depth, is_maximizing, alpha, beta):
    winner = evaluate_winner()
    if winner == playerO:
        return 10 - depth
    if winner == playerX:
        return depth - 10
    if is_board_full():
        return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    for row in range(3):
        for col in range(3):
            if board[row][col]["text"] == "":
                board[row][col]["text"] = playerO if is_maximizing else playerX
                score = minimax(depth + 1, not is_maximizing, alpha, beta)
                board[row][col]["text"] = ""
                best_score = max(best_score, score) if is_maximizing else min(best_score, score)
                if is_maximizing:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)
                if beta <= alpha:
                    return best_score
    return best_score

def evaluate_winner():
    # Check rows and columns
    for i in range(3):
        if board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"] != "":
            return board[i][0]["text"]
        if board[0][i]["text"] == board[1][i]["text"] == board[2][i]["text"] != "":
            return board[0][i]["text"]
    
    # Check diagonals
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        return board[0][0]["text"]
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        return board[0][2]["text"]
    
    return None

def is_board_full():
    return all(board[r][c]["text"] != "" for r in range(3) for c in range(3))

def check_winner():
    global turns, game_over
    turns += 1
    winner = evaluate_winner()

    if winner:
        label.config(text=f"{winner} is the winner!", foreground=color_yellow)
        highlight_winner(winner)
        game_over = True
    elif turns == 9:
        game_over = True
        label.config(text="Tie!", foreground=color_yellow)

def highlight_winner(winner):
    # Check rows and columns
    for i in range(3):
        if board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"] == winner:
            for j in range(3):
                board[i][j].config(foreground=color_yellow, background=color_light_gray)
            return
        if board[0][i]["text"] == board[1][i]["text"] == board[2][i]["text"] == winner:
            for j in range(3):
                board[j][i].config(foreground=color_yellow, background=color_light_gray)
            return
    
    # Check diagonals
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] == winner:
        for i in range(3):
            board[i][i].config(foreground=color_yellow, background=color_light_gray)
    elif board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] == winner:
        for i in range(3):
            board[i][2-i].config(foreground=color_yellow, background=color_light_gray)

def new_game():
    global turns, game_over, curr_player
    turns, game_over = 0, False
    curr_player = playerX
    label.config(text=curr_player + "'s turn", foreground="white")

    for row in range(3):
        for column in range(3):
            board[row][column].config(text="", 
                                    foreground=color_blue if curr_player == "X" else color_yellow, 
                                    background=color_gray)

# Game setup
playerX, playerO = "X", "O"
curr_player = playerX
color_blue, color_yellow = "#4584b6", "#ffde57"
color_gray, color_light_gray = "#343434", "#646464"
turns, game_over = 0, False

# Window setup
window = tkinter.Tk()
window.title("Tic Tac Toe (Player vs AI)")
window.resizable(False, False)
window.config(bg=color_gray)

create_symbol_selection()
window.mainloop()
