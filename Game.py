import tkinter as tk
import random
from Snake import Snake
from Ai import AI

class Game:
    def __init__(self, size=10, scale=50):  # Added scale parameter
        self.snake = Snake(size)
        self.agent = AI()
        self.agent.load()

        self.delay = 100
        self.score = 0
        self.highscore = 0
        self.apple = [0,0,-1]
        self.gridsize = size
        self.scale = scale  # Set the scale for grid size

        self.sessions = 0
        self.training_mode = False
        if not self.training_mode:
            self.window = tk.Tk()
            self.window.title('Snake')

            #For training
            self.session_label = tk.Label(self.window, text='Sessions Completed: {}'.format(self.sessions), font=('Arial', 15))
            self.session_label.pack(anchor='w')

            #
            self.score_label = tk.Label(self.window, text='Score: {}'.format(self.score), font=('Arial', 15))
            self.score_label.pack(anchor='w')

            self.highscore_label = tk.Label(self.window, text='Highscore: {}'.format(self.highscore), font=('Arial', 15))
            self.highscore_label.pack(anchor='w')

            # Adjust the canvas size according to the scale
            self.canvas = tk.Canvas(self.window, height=size * self.scale, width=size * self.scale, bg='grey')
            self.canvas.pack()


    def addScore(self):
        self.score += 1
        self.snake.grow = True
        if self.score > self.highscore:
            self.highscore = self.score
        if not self.training_mode:
            self.score_label.config(text='Score: {}'.format(self.score))
            self.highscore_label.config(text='Highscore: {}'.format(self.highscore))

    def drawSnake(self):
        self.canvas.delete("snake")

        for [x, y] in self.snake.body:
            self.canvas.create_rectangle(
                x * self.scale, y * self.scale,
                (x + 1) * self.scale, (y + 1) * self.scale,
                fill='green', tag='snake'
            )

    def spawnApple(self):
        x = random.randint(0, self.gridsize - 1)
        y = random.randint(0, self.gridsize - 1)
        while [x, y] in self.snake.body:
            x = random.randint(0, self.gridsize - 1)
            y = random.randint(0, self.gridsize - 1)

        self.apple = [x, y, 1]
        if not self.training_mode:
            self.drawApple()

    def drawApple(self):
        self.canvas.delete("apple")
        self.canvas.create_rectangle(
            self.apple[0] * self.scale, self.apple[1] * self.scale,
            (self.apple[0] + 1) * self.scale, (self.apple[1] + 1) * self.scale,
            fill='red', tag='apple'
        )
        

    def checkCollision(self):
        head = self.snake.body[0]

        if head == self.apple[:2] and self.apple[2] == 1:
            self.addScore()
            self.apple[2] = 0
            if not self.training_mode:
                self.canvas.delete("apple")
            return 'Apple'

        if head[0] < 0 or head[0] >= self.gridsize:
            return 'Wall'
        if head[1] < 0 or head[1] >= self.gridsize:
            return 'Wall'
        if head in self.snake.body[1:]:
            return 'Wall'

    def play(self):
        if self.apple[2] != 1:
            self.spawnApple()

        currentState = self.agent.getState(self.snake.body, self.apple, self.snake.direction)
        actionIndex = self.agent.nextAction(currentState)
        self.snake.changeDirection(actionIndex)
        self.snake.move()

        collision = self.checkCollision()
        if collision == 'Wall':
            self.agent.learn(currentState, actionIndex, -10, currentState, True)
            self.agent.save()
            self.reset()

        elif collision == 'Apple':
            self.agent.learn(currentState, actionIndex, 1, self.agent.getState(self.snake.body, self.apple, self.snake.direction))
        else:
            self.agent.learn(currentState, actionIndex, 0, self.agent.getState(self.snake.body, self.apple, self.snake.direction))

        if not self.training_mode:
            self.drawSnake()
            self.window.after(self.delay, self.play)

    def reset(self):
        self.score = 0
        self.apple = [0,0,-1]
        self.snake.reset()
        self.spawnApple()
        self.sessions +=1
        if not self.training_mode:
            self.session_label.config(text='Sessions Completed: {}'.format(self.sessions))

        
        if self.training_mode:
            if game.sessions == 10000:
                print("Sessions Completed : {}".format(game.sessions))
            if game.sessions == 20000:
                print("Sessions Completed : {}".format(game.sessions))
            if game.sessions == 30000:
                print("Sessions Completed : {}".format(game.sessions))
            if game.sessions == 40000:
                print("Sessions Completed : {}".format(game.sessions))

        

# Example usage: creating a game with a larger window (scale=20)
game = Game()  # Increase scale to make the window bigger
game.play()
if not game.training_mode:
    game.window.mainloop()
else:
    try:
        print("Started")
        while game.sessions < 20000:
            game.play()
            
        print('Highscore Achieved : {}'.format(game.highscore))

    except KeyboardInterrupt:
        print("Training aborted by user.")
        print('Highscore Achieved : {}'.format(game.highscore))

