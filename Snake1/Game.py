import tkinter as tk
import random
from Snake import Snake
from Ai import AI

class Game:
    def __init__(self, scale=50):
        self.snake = Snake(10)
        self.agent = AI()
        self.agent.load() #load in qtable

        self.delay = 100 #delay between updates, higher = slower game
        self.score = 0
        self.highscore = 0
        self.apple = [0,0,-1] #coordinates of apple and if apple has been spawned, -1 at init, swaps between 0 and 1 after first spawn
        self.gridsize = 10 #keeping gridsize small for now, changing this value will increase qspace and require further training
        self.scale = scale  #set the scale for grid size

        self.sessions = 0 #for training, to track number of sessions completed
        self.training_mode = False #set true for training, training mode turns off window
        
        if not self.training_mode: #if not in training mode, game will be displayed on window 
            self.window = tk.Tk()
            self.window.title('Snake')

            self.session_label = tk.Label(self.window, text='Sessions Completed: {}'.format(self.sessions), font=('Arial', 15))
            self.session_label.pack(anchor='w')

            #score and highscore
            self.score_label = tk.Label(self.window, text='Score: {}'.format(self.score), font=('Arial', 15))
            self.score_label.pack(anchor='w')

            self.highscore_label = tk.Label(self.window, text='Highscore: {}'.format(self.highscore), font=('Arial', 15))
            self.highscore_label.pack(anchor='w')

            #adjust the canvas size according to the scale
            self.canvas = tk.Canvas(self.window, height=10 * self.scale, width=10 * self.scale, bg='grey')
            self.canvas.pack()


    def addScore(self): #called when snake eats apple
        self.score += 1
        self.snake.grow = True #set snake to grow by 1 segment
        if self.score > self.highscore:
            self.highscore = self.score
            
        if not self.training_mode: #update score and highscore counters in window
            self.score_label.config(text='Score: {}'.format(self.score))
            self.highscore_label.config(text='Highscore: {}'.format(self.highscore))

    def drawSnake(self):
        self.canvas.delete("snake") #delete old snake

        for [x, y] in self.snake.body: #draw new snake
            self.canvas.create_rectangle(
                x * self.scale, y * self.scale,
                (x + 1) * self.scale, (y + 1) * self.scale,
                fill='green', tag='snake'
            )

    def spawnApple(self):
        x = random.randint(0, self.gridsize - 1) #select random location for apple spawn
        y = random.randint(0, self.gridsize - 1)
        while [x, y] in self.snake.body: #reroll until valid location
            x = random.randint(0, self.gridsize - 1)
            y = random.randint(0, self.gridsize - 1)

        self.apple = [x, y, 1] #set apple coordiantes and spawned to 1
        
        if not self.training_mode:
            self.drawApple() #draw apple in window

    def drawApple(self):
        self.canvas.delete("apple") #delete old apple
        self.canvas.create_rectangle( #draw apple
            self.apple[0] * self.scale, self.apple[1] * self.scale,
            (self.apple[0] + 1) * self.scale, (self.apple[1] + 1) * self.scale,
            fill='red', tag='apple'
        )
        

    def checkCollision(self):
        head = self.snake.body[0]

        if head == self.apple[:2] and self.apple[2] == 1: #head = apple and apple spawned 
            self.addScore()
            self.apple[2] = 0 #apple no longer spawned cuz eaten
            if not self.training_mode:
                self.canvas.delete("apple") #delete apple if eating
            return 'Apple' #return collision type

        if head[0] < 0 or head[0] >= self.gridsize: #collide with wall
            return 'Wall'
        if head[1] < 0 or head[1] >= self.gridsize:
            return 'Wall'
        if head in self.snake.body[1:]: #collide with body
            return 'Wall'

    def play(self):
        if self.apple[2] != 1: #spawns apple if not spawned
            self.spawnApple()

        currentState = self.agent.getState(self.snake.body, self.apple, self.snake.direction)
        actionIndex = self.agent.nextAction(currentState)
        self.snake.changeDirection(actionIndex)
        
        self.snake.move() #snake moves by 1 grid in direction

        collision = self.checkCollision() #check for collision after movement
        
        if collision == 'Wall': #game ends
            self.agent.learn(currentState, actionIndex, -10, currentState, True)
            self.agent.save()
            self.reset() #resets to begin next session

        elif collision == 'Apple': #eat apple
            self.agent.learn(currentState, actionIndex, 1, self.agent.getState(self.snake.body, self.apple, self.snake.direction))
        else:
            self.agent.learn(currentState, actionIndex, 0, self.agent.getState(self.snake.body, self.apple, self.snake.direction))

        if not self.training_mode: #draw new position of snake in window
            self.drawSnake()
            self.window.after(self.delay, self.play) #go to next update

    def reset(self): #resets game for new session
        self.score = 0
        self.apple = [0,0,-1]
        self.snake.reset()
        self.spawnApple()
        self.sessions +=1
        
        if not self.training_mode:
            self.session_label.config(text='Sessions Completed: {}'.format(self.sessions)) #update number of sessions currently completed in window

        
        if self.training_mode: #just to check progress on training sessions
            if game.sessions % 1000 == 0:
                print("Sessions Completed : {}".format(game.sessions))


        


game = Game()  
game.play()

if not game.training_mode:
    game.window.mainloop() #start window
else: #training mode
    try:
        print("Started")
        while game.sessions < 10000: #change number here to edit number of sessions to train on
            game.play()
            
        print('Highscore Achieved : {}'.format(game.highscore)) #highscore after training sessions completed

    except KeyboardInterrupt: #ctrl+c in console to interrupt
        print("Training aborted by user.")
        print('Highscore Achieved : {}'.format(game.highscore))

