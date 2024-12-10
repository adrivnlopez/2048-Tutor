from tkinter import Frame, Label, CENTER, messagebox, Button
import random
import logic
import constants as c
from ai_logic import GameAI

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid(padx=50, pady=50)  
        
        # bottom padding
        self.title_frame = Frame(self.master)
        self.title_frame.grid(pady=(20, 50)) 
        
        # game title
        title_label = Label(self.title_frame, text="2048 Game", font=("Verdana", 24, "bold"))
        title_label.grid()

        # padding for side assets
        self.info_frame = Frame(self.master)
        self.info_frame.grid(row=0, column=1, padx=40, sticky='n')
        
        # score label
        self.score_label = Label(self.info_frame, text="Score: 0", font=("Verdana", 16))
        self.score_label.grid(pady=10)

        # hint toggle 
        self.ai_hint_button = Button(
            self.info_frame, 
            text="Show AI Hint", 
            command=self.toggle_hint,
            font=("Verdana", 14)
        )
        self.ai_hint_button.grid(pady=10)

        # hint label
        self.hint_label = Label(
            self.info_frame, 
            text="", 
            font=("Verdana", 12),
            wraplength=200
        )
        self.hint_label.grid(pady=10)

        # auto play toggle 
        self.auto_play_button = Button(
            self.info_frame, 
            text="Start AI Play", 
            command=self.toggle_autoplay,
            font=("Verdana", 14)
        )
        self.auto_play_button.grid(pady=10)
        
        # play again
        self.play_again_button = Button(
            self.info_frame, 
            text="Play Again/Restart", 
            command=self.reset_game, 
            font=("Verdana", 14)
        )
        self.play_again_button.grid(pady=10)

        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.score = 0
        self.ai = GameAI()  # Initialize the AI
        self.hint_mode = False  # track  hint mode
        self.auto_play_mode = False  # track play mode
        self.update_grid_cells()
        
        # Initial AI hint
        self.update_hint()

        self.mainloop()


    def toggle_hint(self): 
        self.hint_mode = not self.hint_mode
        
        if self.hint_mode:
            self.ai_hint_button.configure(text="Hide AI Hint")
            self.update_hint()
        else:
            self.ai_hint_button.configure(text="Show AI Hint")
            self.hint_label.configure(text="")


    def toggle_autoplay(self):
        self.auto_play_mode = not self.auto_play_mode
        
        if self.auto_play_mode:
            # stop hint mode if it's on
            if self.hint_mode:
                self.toggle_hint()
            
            self.auto_play_button.configure(text="Stop Auto Play")
            self.run_autoplay()
        else:
            self.auto_play_button.configure(text="Start Auto Play")
            self.hint_label.configure(text="")

    def update_hint(self):
        if self.hint_mode:
            # Get best move
            best_move = self.ai.get_best_move(self.matrix)
            
            if best_move:
                # Update hint label
                self.hint_label.configure(text=f"Recommended Move: {best_move.capitalize()}")
            else:
                self.hint_label.configure(text="No recommended move")


    def run_autoplay(self):
        """Automatically run AI moves if AI play mode is on"""
        if not self.auto_play_mode:
            return

        # Get best move
        best_move = self.ai.get_best_move(self.matrix)
        
        if best_move:
            # Execute the move
            if best_move == 'up':
                self.matrix, done = logic.up(self.matrix)
            elif best_move == 'down':
                self.matrix, done = logic.down(self.matrix)
            elif best_move == 'left':
                self.matrix, done = logic.left(self.matrix)
            elif best_move == 'right':
                self.matrix, done = logic.right(self.matrix)
            
            # Add a new tile if move was successful
            if done:
                self.matrix = logic.add_random_tile(self.matrix)
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                
                # Update hint label
                self.hint_label.configure(text=f"AI move: {best_move.capitalize()}")
                
                # Check game state
                game_status = logic.game_state(self.matrix)
                if game_status == 'win':
                    messagebox.showinfo("Congratulations!", "You Win!")
                    self.auto_play_mode = False
                    self.auto_play_button.configure(text="Start AI Play")
                elif game_status == 'lose':
                    messagebox.showinfo("Game Over", "You Lose!")
                    self.auto_play_mode = False
                    self.auto_play_button.configure(text="Start AI Play")
        
        # Schedule next move if AI play mode is still on
        if self.auto_play_mode:
            self.master.after(100, self.run_autoplay)  # 100ms delay between moves


    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME, width=c.SIZE + 100, height=c.SIZE + 100)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        
        # Update score
        self.score_label.configure(text=f"Score: {self.calculate_score()}")
        
        self.update_idletasks()

    def calculate_score(self):
        # Simple scoring mechanism
        return sum(sum(row) for row in self.matrix)

    def key_down(self, event):
        key = event.keysym
        print(event)
        
        # stop auto play mode if a key is pressed during auto-play
        if self.auto_play_mode:
            self.toggle_autoplay()
        
        if key == c.KEY_QUIT: 
            self.quit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
            # update hint after going back
            self.update_hint()
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_random_tile(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                
                # update hint after move
                self.update_hint()
                
                if logic.game_state(self.matrix) == 'win':
                    messagebox.showinfo("Congratulations!", "You Win!")
                    self.quit()
                if logic.game_state(self.matrix) == 'lose':
                    messagebox.showinfo("Game Over", "You Lose!")
                    self.quit()

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2
        
    def reset_game(self):
        # Reset the game matrix
        self.matrix = logic.new_game(c.GRID_LEN)
    
        # Update the grid display manually
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_value = self.matrix[i][j]
                self.grid_cells[i][j].configure(
                    text=str(new_value) if new_value != 0 else "",
                    bg=c.BACKGROUND_COLOR_DICT.get(new_value, c.BACKGROUND_COLOR_CELL_EMPTY)
                )
    
        # Reset the score
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

game_grid = GameGrid()