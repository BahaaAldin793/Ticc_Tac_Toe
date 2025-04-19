import tkinter as tk
import math
import random
from functools import partial

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)
        
        # Colors from tictactoe.py
        self.colors = {
            "bg": "#343434",  # Dark gray background
            "button": "#343434",  # Dark gray buttons
            "win": "#646464",  # Light gray for winning cells
            "x": "#4584b6",  # Blue for X
            "o": "#ffde57",  # Yellow for O
            "text": "white"  # White text
        }
        self.root.config(bg=self.colors["bg"])
        
        self.stats = {"X": 0, "O": 0, "Draw": 0}
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.player_symbol = "X"
        self.ai_symbol = "O"
        
        self.create_symbol_selection()
    
    def create_symbol_selection(self):
        self.symbol_window = tk.Toplevel(self.root)
        self.symbol_window.title("Choose Symbol")
        self.symbol_window.resizable(False, False)
        self.symbol_window.config(bg=self.colors["bg"])
        self.symbol_window.grab_set()
        
        tk.Label(self.symbol_window, text="Choose X or O:", font=("Consolas", 20), 
                bg=self.colors["bg"], fg=self.colors["text"]).pack(pady=10)
        frame = tk.Frame(self.symbol_window, bg=self.colors["bg"])
        frame.pack(pady=5)
        
        for symbol in ["X", "O"]:
            tk.Button(frame, text=symbol, font=("Consolas", 50, "bold"), 
                     fg=self.colors[symbol.lower()], bg=self.colors["bg"],
                     width=4, height=1,
                     command=lambda s=symbol: self.set_player_symbol(s)).pack(side=tk.LEFT, padx=10)
    
    def set_player_symbol(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        self.symbol_window.destroy()
        self.create_widgets()
        self.update_status()
        if self.ai_symbol == "X":
            self.root.after(500, self.ai_move)
    
    def create_widgets(self):
        self.board_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.board_frame.pack(pady=10)
        
        self.buttons = [[tk.Button(self.board_frame, text="", font=("Consolas", 50, "bold"), 
                         height=1, width=4, bg=self.colors["button"], fg=self.colors["x"],
                         command=partial(self.make_move, r, c))
                         for c in range(3)] for r in range(3)]
        
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c, padx=2, pady=2)
        
        self.status_label = tk.Label(self.root, text="", font=("Consolas", 20), 
                                   bg=self.colors["bg"], fg=self.colors["text"])
        self.status_label.pack(pady=5)
        
        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(pady=5)
        
        tk.Button(control_frame, text="Restart", font=("Consolas", 20), 
                 bg=self.colors["bg"], fg=self.colors["text"],
                 command=self.restart_game).pack(side=tk.LEFT, padx=5)
        
        stats_frame = tk.Frame(self.root, bg=self.colors["bg"])
        stats_frame.pack(pady=5)
        
        self.stats_labels = {
            "X": tk.Label(stats_frame, text="You: 0", font=("Consolas", 20), 
                         bg=self.colors["bg"], fg=self.colors["x"]),
            "O": tk.Label(stats_frame, text="AI: 0", font=("Consolas", 20), 
                         bg=self.colors["bg"], fg=self.colors["o"]),
            "Draw": tk.Label(stats_frame, text="Draws: 0", font=("Consolas", 20), 
                           bg=self.colors["bg"], fg=self.colors["text"])
        }
        
        for label in self.stats_labels.values():
            label.pack(side=tk.LEFT, padx=5)
    
    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state=tk.DISABLED, 
                                        disabledforeground=self.colors[self.current_player.lower()])
            
            if self.check_winner():
                self.handle_win(self.current_player)
                return
                
            if self.is_draw():
                self.handle_draw()
                return
                
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_status()

            if self.current_player == self.ai_symbol:
                for r in range(3):
                    for c in range(3):
                        self.buttons[r][c].config(state=tk.DISABLED)
                self.root.after(500, self.ai_move)
    
    def ai_move(self):
        self.status_label.config(text="AI is thinking...")
        self.root.update()
        
        depth_limit = 3
        best_score = -math.inf
        best_move = None
        
        if random.random() < 0.2:
            empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
            if empty_cells:
                best_move = random.choice(empty_cells)
        else:
            for r in range(3):
                for c in range(3):
                    if self.board[r][c] == "":
                        self.board[r][c] = self.ai_symbol
                        score = self.minimax(self.board, 0, False, -math.inf, math.inf, depth_limit)
                        self.board[r][c] = ""
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
        
        self.root.after(500, lambda: self.execute_ai_move(best_move))
    
    def execute_ai_move(self, move):
        if move is None:
            return
            
        r, c = move
        self.board[r][c] = self.ai_symbol
        self.buttons[r][c].config(text=self.ai_symbol, state=tk.DISABLED, 
                                disabledforeground=self.colors[self.ai_symbol.lower()])
        
        if self.check_winner():
            self.handle_win(self.ai_symbol)
            return
            
        if self.is_draw():
            self.handle_draw()
            return
            
        self.current_player = self.player_symbol
        self.update_status()
        
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.buttons[r][c].config(state=tk.NORMAL)
    
    def minimax(self, board, depth, is_maximizing, alpha, beta, depth_limit):
        winner = self.check_winner(board)
        if winner == self.player_symbol:
            return -10 + depth
        if winner == self.ai_symbol:
            return 10 - depth
        if self.is_draw(board) or depth >= depth_limit:
            return 0
        
        if is_maximizing:
            max_eval = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = self.ai_symbol
                        eval = self.minimax(board, depth+1, False, alpha, beta, depth_limit)
                        board[r][c] = ""
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            return max_eval
            return max_eval
        else:
            min_eval = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = self.player_symbol
                        eval = self.minimax(board, depth+1, True, alpha, beta, depth_limit)
                        board[r][c] = ""
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            return min_eval
            return min_eval
    
    def check_winner(self, board=None):
        board = board or self.board
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        return None
    
    def is_draw(self, board=None):
        board = board or self.board
        return all(cell != "" for row in board for cell in row) and not self.check_winner(board)
    
    def handle_win(self, winner):
        self.highlight_winner()
        self.stats[winner] += 1
        self.update_stats_display()
        self.status_label.config(text=f"{'You' if winner == self.player_symbol else 'AI'} Wins!", 
                               fg=self.colors[winner.lower()])
        self.disable_all_buttons()
    
    def handle_draw(self):
        self.stats["Draw"] += 1
        self.update_stats_display()
        self.status_label.config(text="It's a Draw!", fg=self.colors["text"])
        self.disable_all_buttons()
    
    def highlight_winner(self):
        winning_cells = []
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                winning_cells.extend([(i, 0), (i, 1), (i, 2)])
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                winning_cells.extend([(0, i), (1, i), (2, i)])
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            winning_cells.extend([(0, 0), (1, 1), (2, 2)])
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            winning_cells.extend([(0, 2), (1, 1), (2, 0)])
        for r, c in set(winning_cells):
            self.buttons[r][c].config(bg=self.colors["win"])
    
    def disable_all_buttons(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state=tk.DISABLED)
    
    def restart_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", state=tk.NORMAL, 
                                        bg=self.colors["button"], fg=self.colors["x"])
        self.update_status()
        if self.ai_symbol == "X":
            for r in range(3):
                for c in range(3):
                    self.buttons[r][c].config(state=tk.DISABLED)
            self.root.after(500, self.ai_move)
    
    def update_status(self):
        if self.current_player == self.player_symbol:
            self.status_label.config(text="Your Turn!", 
                                   fg=self.colors[self.player_symbol.lower()])
        else:
            self.status_label.config(text="AI is thinking...", fg=self.colors["text"])
    
    def update_stats_display(self):
        player_stat = self.stats['X'] if self.player_symbol == 'X' else self.stats['O']
        ai_stat = self.stats['O'] if self.ai_symbol == 'O' else self.stats['X']
        self.stats_labels["X"].config(text=f"You: {player_stat}")
        self.stats_labels["O"].config(text=f"AI: {ai_stat}")
        self.stats_labels["Draw"].config(text=f"Draws: {self.stats['Draw']}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()