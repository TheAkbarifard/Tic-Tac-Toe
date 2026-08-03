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
        
        # Status Label showing whose turn it is or who won
        self.status_label = tk.Label(
            self.root, 
            text="Player X's Turn", 
            font=("Helvetica", 16, "bold"), 
            bg="#2C3E50", 
            fg="#ECF0F1"
        )
        self.status_label.pack(pady=15)
        
        # Grid Frame to hold the 3x3 board
        grid_frame = tk.Frame(self.root, bg="#2C3E50")
        grid_frame.pack(padx=20, pady=5)
        
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
            
        # Reset Button to play again
        self.reset_button = tk.Button(
            self.root, 
            text="Restart Game", 
            font=("Helvetica", 12, "bold"), 
            bg="#E74C3C", 
            fg="#ECF0F1",
            activebackground="#C0392B", 
            activeforeground="#ECF0F1",
            relief="flat",
            padx=10,
            pady=5,
            command=self.reset_game
        )
        self.reset_button.pack(pady=15)

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
