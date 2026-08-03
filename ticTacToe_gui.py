import tkinter as tk
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="#2C3E50")  # Sleek dark background
        self.root.resizable(False, False)
        
        self.starting_player = "X"
        self.turn = self.starting_player
        self.board = [" " for _ in range(9)]
        self.buttons = []
        self.game_over = False
        
        # Win counters
        self.score_x = 0
        self.score_o = 0
        self.last_winner = None
        self.last_loser = None
        
        # Status Label showing whose turn it is or who won
        self.status_label = tk.Label(
            self.root, 
            text="X's Turn", 
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
        
        # Reset Scores Button
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
        control_frame.pack(pady=10)
        
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

        # Settings Frame (Compact dropdown and info icon)
        settings_frame = tk.Frame(self.root, bg="#2C3E50")
        settings_frame.pack(pady=(0, 5))
        
        mode_label = tk.Label(
            settings_frame,
            text="First Turn:",
            font=("Helvetica", 10, "bold"),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        mode_label.grid(row=0, column=0, padx=(0, 5))
        
        # OptionMenu for starting modes
        self.start_mode = tk.StringVar(value="Alternate")
        mode_menu = tk.OptionMenu(
            settings_frame,
            self.start_mode,
            "Alternate",
            "Random",
            "Loser Starts",
            command=self.on_mode_change
        )
        mode_menu.config(
            font=("Helvetica", 9, "bold"),
            bg="#34495E",
            fg="#ECF0F1",
            activebackground="#1ABC9C",
            activeforeground="#ECF0F1",
            relief="flat",
            highlightthickness=0,
            padx=5,
            pady=2,
            width=12  # Fixed width to prevent layout shifting when options change
        )
        mode_menu["menu"].config(
            font=("Helvetica", 9),
            bg="#34495E",
            fg="#ECF0F1",
            activebackground="#1ABC9C",
            activeforeground="#ECF0F1"
        )
        mode_menu.grid(row=0, column=1, padx=(0, 5))
        
        # Info icon
        self.info_label = tk.Label(
            settings_frame,
            text="ⓘ",
            font=("Helvetica", 12, "bold"),
            bg="#2C3E50",
            fg="#95A5A6",
            cursor="hand2"
        )
        self.info_label.grid(row=0, column=2)
        self.info_label.bind("<Enter>", self.show_tooltip)
        self.info_label.bind("<Leave>", self.hide_tooltip)
        
        # Tooltip description label
        self.desc_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 9, "italic"),
            bg="#2C3E50",
            fg="#BDC3C7"
        )
        self.desc_label.pack(pady=(0, 10))

        # Bind mouse wheel scrolling on the dropdown menu and label to cycle selections
        mode_menu.bind("<MouseWheel>", self.handle_mouse_wheel)
        mode_label.bind("<MouseWheel>", self.handle_mouse_wheel)

        # Bind click event to the main root window to reset after the game ends
        self.root.bind("<Button-1>", self.handle_global_click)

    def make_move(self, idx):
        # If the game is already over, a click resets the game
        if self.game_over:
            self.reset_game()
            return

        # Check if the square is empty
        if self.board[idx] == " ":
            self.board[idx] = self.turn
            
            # Stylize X and O differently
            color = "#3498DB" if self.turn == "X" else "#E67E22"
            
            # Update button visually without changing standard state to 'disabled'
            # (Matches active background/foreground to standard colors so hover states lock stably)
            self.buttons[idx].config(
                text=self.turn, 
                fg=color,
                activebackground="#34495E",
                activeforeground=color
            )
            
            # Check for win or draw
            if self.check_win(self.turn):
                self.status_label.config(text=f"{self.turn} Wins!", fg="#2ECC71")
                
                # Increment the score
                if self.turn == "X":
                    self.score_x += 1
                else:
                    self.score_o += 1
                
                self.last_winner = self.turn
                self.last_loser = "O" if self.turn == "X" else "X"
                
                self.update_score_display()
                self.game_over = True
                
            elif " " not in self.board:
                self.status_label.config(text="It's a Draw!", fg="#F1C40F")
                self.last_winner = None
                self.last_loser = None
                self.game_over = True
            else:
                # Switch turn
                self.turn = "O" if self.turn == "X" else "X"
                self.status_label.config(text=f"{self.turn}'s Turn", fg="#ECF0F1")

    def check_win(self, player):
        # 8 possible win paths
        win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
            [0, 4, 8], [2, 4, 6]             # diagonals
        ]
        return any(all(self.board[i] == player for i in state) for state in win_states)

    def handle_global_click(self, event):
        # If the game is over and the click is not on settings widgets or reset scores, reset the game
        if self.game_over:
            if event.widget in [self.reset_scores_button, self.info_label]:
                return
            self.reset_game()

    def handle_mouse_wheel(self, event):
        # Cycle through dropdown options using the mouse wheel when hovering
        options = ["Alternate", "Random", "Loser Starts"]
        current_val = self.start_mode.get()
        if current_val in options:
            idx = options.index(current_val)
            if event.delta > 0:  # Scroll Up
                new_idx = (idx - 1) % len(options)
            else:  # Scroll Down
                new_idx = (idx + 1) % len(options)
            
            new_mode = options[new_idx]
            self.start_mode.set(new_mode)
            self.on_mode_change(new_mode)

    def determine_next_starter(self):
        mode = self.start_mode.get()
        if mode == "Alternate":
            # Alternate starter from the last game
            self.starting_player = "O" if self.starting_player == "X" else "X"
            return self.starting_player
        elif mode == "Random":
            return random.choice(["X", "O"])
        elif mode == "Loser Starts":
            if self.last_loser is not None:
                return self.last_loser
            else:
                # Alternate if there was a draw
                self.starting_player = "O" if self.starting_player == "X" else "X"
                return self.starting_player
        return "X"

    def show_tooltip(self, event):
        mode = self.start_mode.get()
        descriptions = {
            "Alternate": "Alternate starting player each round.",
            "Random": "Select starting player randomly at reset.",
            "Loser Starts": "The loser of the last round starts first."
        }
        self.desc_label.config(text=descriptions.get(mode, ""))
        self.info_label.config(fg="#1ABC9C")  # Highlight 'i' icon

    def hide_tooltip(self, event):
        self.desc_label.config(text="")
        self.info_label.config(fg="#95A5A6")

    def on_mode_change(self, selected_mode):
        descriptions = {
            "Alternate": "Alternate starting player each round.",
            "Random": "Select starting player randomly at reset.",
            "Loser Starts": "The loser of the last round starts first."
        }
        self.desc_label.config(text=descriptions.get(selected_mode, ""))
        # Auto-hide tooltip description after 2 seconds
        self.root.after(2000, lambda: self.desc_label.config(text="") if self.desc_label.cget("text") == descriptions.get(selected_mode, "") else None)

    def update_score_display(self):
        self.score_label.config(text=f"X: {self.score_x}   |   O: {self.score_o}")

    def reset_scores(self):
        self.score_x = 0
        self.score_o = 0
        self.last_winner = None
        self.last_loser = None
        self.update_score_display()

    def reset_game(self):
        self.turn = self.determine_next_starter()
        self.starting_player = self.turn
        self.board = [" " for _ in range(9)]
        self.game_over = False
        self.status_label.config(text=f"{self.turn}'s Turn", fg="#ECF0F1")
        for btn in self.buttons:
            btn.config(
                text="", 
                state="normal", 
                bg="#34495E", 
                fg="#ECF0F1",
                activebackground="#1ABC9C",
                activeforeground="#ECF0F1"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
