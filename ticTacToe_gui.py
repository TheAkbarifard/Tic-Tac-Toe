import tkinter as tk

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#2C3E50")  # Sleek dark background
        self.root.resizable(False, False)
        
        self.turn = "X"
        self.board = [" " for _ in range(9)]
        self.buttons = []
        
        # Win counters
        self.score_x = 0
        self.score_o = 0
        
        # Status Label showing whose turn it is or who won
        self.status_label = tk.Label(
            self.root, 
            text="Player X's Turn", 
            font=("Helvetica", 16, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        )
        self.status_label.pack(pady=10)
        
        # Scoreboard Display Frame
        score_frame = tk.Frame(self.root, bg="#2C3E50")
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            score_frame, 
            text="X: 0   |   O: 0", 
            font=("Helvetica", 14, "bold"), 
            bg="#34495E", 
            fg="#ECF0F1",
            padx=20,
            pady=6,
            relief="flat"
        )
        self.score_label.grid(row=0, column=0, padx=(0, 10))
        
        # Reset Scores Button (Placed directly next to the scoreboard)
        self.reset_scores_button = tk.Button(
            score_frame, 
            text="Reset Scores", 
            font=("Helvetica", 10, "bold"), 
            bg="#95A5A6", 
            fg="#ECF0F1",
            activebackground="#7F8C8D", 
            activeforeground="#ECF0F1",
            relief="flat",
            padx=8,
            pady=4,
            command=self.reset_scores
        )
        self.reset_scores_button.grid(row=0, column=1)
        
        # Grid Frame to hold the 3x3 board
        grid_frame = tk.Frame(self.root, bg="#2C3E50")
        grid_frame.pack(padx=20, pady=10)
        
        # Create 3x3 Buttons grid
        for i in range(9):
            btn = tk.Button(
                grid_frame, 
                text="", 
                font=("Helvetica", 24, "bold"), 
                width=5, 
                height=2, 
                bg="#34495E", 
                fg="#ECF0F1",
                activebackground="#1ABC9C", 
                activeforeground="#ECF0F1",
                relief="flat",
                command=lambda idx=i: self.make_move(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.buttons.append(btn)
            
        # Control Buttons Frame
        control_frame = tk.Frame(self.root, bg="#2C3E50")
        control_frame.pack(pady=15)
        
        # Reset Game Button
        self.reset_button = tk.Button(
            control_frame, 
            text="Restart Game", 
            font=("Helvetica", 12, "bold"), 
            bg="#E74C3C", 
            fg="#ECF0F1",
            activebackground="#C0392B", 
            activeforeground="#ECF0F1",
            relief="flat",
            padx=15,
            pady=5,
            command=self.reset_game
        )
        self.reset_button.pack()

    def make_move(self, idx):
        # Check if the square is empty
        if self.board[idx] == " ":
            self.board[idx] = self.turn
            
            # Stylize X and O differently
            color = "#3498DB" if self.turn == "X" else "#E67E22"
            self.buttons[idx].config(
                text=self.turn, 
                fg=color,
                state="disabled",
                disabledforeground=color
            )
            
            # Check for win or draw
            if self.check_win(self.turn):
                self.status_label.config(text=f"Player {self.turn} Wins!", fg="#2ECC71")
                
                # Increment the score
                if self.turn == "X":
                    self.score_x += 1
                else:
                    self.score_o += 1
                self.update_score_display()
                self.disable_board()
                
            elif " " not in self.board:
                self.status_label.config(text="It's a Draw!", fg="#F1C40F")
            else:
                # Switch turn
                self.turn = "O" if self.turn == "X" else "X"
                self.status_label.config(text=f"Player {self.turn}'s Turn", fg="#ECF0F1")

    def check_win(self, player):
        # 8 possible win paths
        win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        return any(all(self.board[i] == player for i in state) for state in win_states)

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def update_score_display(self):
        self.score_label.config(text=f"X: {self.score_x}   |   O: {self.score_o}")

    def reset_scores(self):
        self.score_x = 0
        self.score_o = 0
        self.update_score_display()

    def reset_game(self):
        self.turn = "X"
        self.board = [" " for _ in range(9)]
        self.status_label.config(text="Player X's Turn", fg="#ECF0F1")
        for btn in self.buttons:
            btn.config(
                text="", 
                state="normal", 
                bg="#34495E", 
                fg="#ECF0F1"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
