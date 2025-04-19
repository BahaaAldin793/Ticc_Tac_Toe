import tkinter as tk
import math
import random
from functools import partial
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Ultimate Edition")
        self.root.resizable(False, False)
        
        
        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff" 
        self.win_color = "#4CAF50"  
        self.x_color = "#2196F3"    
        self.o_color = "#F44336"    
        self.draw_color = "#FF9800" 
        self.disabled_color = "#E0E0E0"
        
        self.root.config(bg=self.bg_color)
        
        
        self.stats = {"X": 0, "O": 0, "Draw": 0}
        
        
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.player_symbol = "X"  
        self.ai_symbol = "O"      
        self.difficulty = "Hard"  
        
        
        self.create_symbol_selection()
    
    def create_symbol_selection(self):
        
        self.symbol_window = tk.Toplevel(self.root)
        self.symbol_window.title("Choose Your Symbol")
        self.symbol_window.resizable(False, False)
        self.symbol_window.grab_set()  
        
        tk.Label(self.symbol_window, text="Choose your symbol:", 
                font=("Arial", 14)).pack(pady=20)
        
        frame = tk.Frame(self.symbol_window)
        frame.pack(pady=10)
        
        
        tk.Button(frame, text="X", font=("Arial", 24, "bold"), 
                 fg=self.x_color, width=3, relief="raised",
                 command=lambda: self.set_player_symbol("X")).pack(side=tk.LEFT, padx=20)
        
        
        tk.Button(frame, text="O", font=("Arial", 24, "bold"), 
                 fg=self.o_color, width=3, relief="raised",
                 command=lambda: self.set_player_symbol("O")).pack(side=tk.LEFT, padx=20)
    
    def set_player_symbol(self, symbol):
        
        self.player_symbol = symbol
        self.ai_symbol = "O" if symbol == "X" else "X"
        self.symbol_window.destroy()
        self.create_widgets()
        self.update_status()
        
        
        if self.ai_symbol == "X":
            self.current_player = "X"
            self.root.after(500, self.ai_move)
    
    def create_widgets(self):
        
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.grid(row=0, column=0, padx=20, pady=10)
        
       
        self.buttons = [[tk.Button(self.board_frame, text="", font=("Arial", 32, "bold"), 
                         height=1, width=3, bg=self.button_color,
                         relief="ridge", borderwidth=3,
                         command=partial(self.make_move, r, c))
                         for c in range(3)] for r in range(3)]
        
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c, padx=5, pady=5)
        
       
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), 
                                   bg=self.bg_color, fg="#333333")
        self.status_label.grid(row=1, column=0, pady=(10, 5))
        
        
        self.control_frame = tk.Frame(self.root, bg=self.bg_color)
        self.control_frame.grid(row=2, column=0, pady=5)
        
        
        self.restart_button = tk.Button(self.control_frame, text="New Game", font=("Arial", 12), 
                                      bg="#607D8B", fg="white", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="Hard")
        self.difficulty_menu = tk.OptionMenu(self.control_frame, self.difficulty_var, 
                                           "Easy", "Medium", "Hard", 
                                           command=self.set_difficulty)
        self.difficulty_menu.config(font=("Arial", 10), bg="#E0E0E0")
        self.difficulty_menu.pack(side=tk.LEFT, padx=5)
        
       
        self.stats_frame = tk.Frame(self.root, bg=self.bg_color)
        self.stats_frame.grid(row=3, column=0, pady=(10, 20))
        
        tk.Label(self.stats_frame, text="Stats:", font=("Arial", 12, "bold"), bg=self.bg_color).pack(side=tk.LEFT)
        
        self.stats_labels = {
            "X": tk.Label(self.stats_frame, text="Player 1: 0", font=("Arial", 10), bg=self.bg_color, fg=self.x_color),
            "O": tk.Label(self.stats_frame, text="Player 2: 0", font=("Arial", 10), bg=self.bg_color, fg=self.o_color),
            "Draw": tk.Label(self.stats_frame, text="Draws: 0", font=("Arial", 10), bg=self.bg_color, fg=self.draw_color)
        }
        
        for label in self.stats_labels.values():
            label.pack(side=tk.LEFT, padx=10)
    
    def set_difficulty(self, level):
        
        self.difficulty = level
    
    def make_move(self, row, col):
        
        if self.board[row][col] == "":
           
            symbol = self.current_player
            
          
            self.board[row][col] = symbol
            color = self.x_color if symbol == "X" else self.o_color
            self.buttons[row][col].config(text=symbol, state=tk.DISABLED, 
                                        disabledforeground=color)
            
          
            if self.check_winner():
                self.handle_win(symbol)
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
        
        depth_limit = {"Easy": 1, "Medium": 3, "Hard": 9}[self.difficulty]
        best_score = -math.inf
        best_move = None
        
       
        if self.difficulty == "Easy" and random.random() < 0.3:
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
        color = self.o_color if self.ai_symbol == "O" else self.x_color
        self.buttons[r][c].config(text=self.ai_symbol, state=tk.DISABLED, 
                                disabledforeground=color)
        
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
       
        if board is None:
            board = self.board
            
       
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
      
        if board is None:
            board = self.board
        return all(cell != "" for row in board for cell in row) and not self.check_winner(board)
    
    def handle_win(self, winner):
       
        self.highlight_winner()
        self.stats[winner] += 1
        self.update_stats_display()
        
        if winner == self.player_symbol:
            self.status_label.config(text="You Win!", fg=self.x_color if winner == "X" else self.o_color)
        else:
            self.status_label.config(text="AI Wins!", fg=self.o_color if winner == "O" else self.x_color)
        
        self.disable_all_buttons()
    
    def handle_draw(self):
       
        self.stats["Draw"] += 1
        self.update_stats_display()
        self.status_label.config(text="It's a Draw!", fg=self.draw_color)
        self.disable_all_buttons()
    
    def highlight_winner(self):
        
        winning_cells = []
        board = self.board
        
      
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "":
                winning_cells.extend([(i, 0), (i, 1), (i, 2)])
            if board[0][i] == board[1][i] == board[2][i] != "":
                winning_cells.extend([(0, i), (1, i), (2, i)])
        
        if board[0][0] == board[1][1] == board[2][2] != "":
            winning_cells.extend([(0, 0), (1, 1), (2, 2)])
        if board[0][2] == board[1][1] == board[2][0] != "":
            winning_cells.extend([(0, 2), (1, 1), (2, 0)])
        
       
        for r, c in set(winning_cells):
            self.buttons[r][c].config(bg=self.win_color)
    
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
                                        bg=self.button_color, fg="black")
        
        self.update_status()
        
        if self.ai_symbol == "X":
            for r in range(3):
                for c in range(3):
                    self.buttons[r][c].config(state=tk.DISABLED)
            self.root.after(500, self.ai_move)
    
    def update_status(self):
        if self.current_player == self.player_symbol:
            self.status_label.config(text="Your Turn!", fg=self.x_color if self.player_symbol == "X" else self.o_color)
        else:
            self.status_label.config(text="AI is thinking...", fg="#333333")
    
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