class Snake:
    def __init__(self,board_size):
        self.spawn = [[board_size//2,board_size//2]]
        self.body = self.spawn
        self.direction = 0 #up
        self.grow = False
    
    def reset(self):
        self.body = self.spawn
        self.direction = 0
        self.grow = False

    def move(self):
        new_head = self.body[0].copy()

        x = 0
        y = 1

        if (self.direction == 0): #up
            new_head[y] -= 1

        elif (self.direction == 1): #down
            new_head[y] += 1

        elif (self.direction == 2): #left
            new_head[x] -= 1

        elif (self.direction == 3): #right
            new_head[x] += 1

        if (self.grow):
            self.body = [new_head] + self.body
            self.grow = False

        else:
            self.body = [new_head] + self.body[:-1]
    
    def changeDirection(self, new_direction):
        opposite_directions = {
            0: 1,
            1: 0,
            2: 3,
            3: 2
        }
        if (new_direction in opposite_directions and self.direction != opposite_directions[new_direction]):
            self.direction = new_direction

    
