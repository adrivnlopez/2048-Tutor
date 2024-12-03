from tkinter import Frame, Label, CENTER, messagebox
import random
import logic
import constants as c

def gen():
    return random.randint(0, c.GRID_LEN - 1)

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid(padx=50, pady=50)  
        
        # title or header frame
        self.title_frame = Frame(self.master)
        self.title_frame.grid(pady=(20, 10)) 
        
        # title label
        title_label = Label(self.title_frame, text="2048 Game", font=("Verdana", 24, "bold"))
        title_label.grid()

        # frame for potential side information or controls
        self.info_frame = Frame(self.master)
        self.info_frame.grid(row=0, column=1, padx=20, sticky='n')
        
        # score label as an example of additional feature space
        self.score_label = Label(self.info_frame, text="Score: 0", font=("Verdana", 16))
        self.score_label.grid(pady=10)

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
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        # Increased background size slightly to accommodate more padding
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
        # Simple scoring mechanism: sum of all numbers on the grid
        return sum(sum(row) for row in self.matrix)

    def key_down(self, event):
        key = event.keysym
        print(event)
        if key == c.KEY_QUIT: 
            self.quit()
        if key == c.KEY_BACK and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
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

game_grid = GameGrid()