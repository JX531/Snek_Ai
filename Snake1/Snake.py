class Snake:
    def __init__(self,board_size):
        self.spawn = [[board_size//2,board_size//2]] #Spawn location with 1 segment in middle of board
        self.body = self.spawn 
        self.direction = 0 #starts with up // 0 = up, 1 = down, 2 = left, 3 = right
        self.grow = False #grow ticks to True whenever it eats apple to add new segment, then back to false
    
    def reset(self): #reset snake
        self.body = self.spawn
        self.direction = 0
        self.grow = False

    def move(self):
        new_head = self.body[0].copy()

        x = 0 #using x y coordinates to improve readibility
        y = 1

        if (self.direction == 0): #up
            new_head[y] -= 1

        elif (self.direction == 1): #down
            new_head[y] += 1

        elif (self.direction == 2): #left
            new_head[x] -= 1

        elif (self.direction == 3): #right
            new_head[x] += 1

        if (self.grow): #if set to grow
            self.body = [new_head] + self.body #appends entire old body to new head
            self.grow = False #turn off grow after growing

        else:
            self.body = [new_head] + self.body[:-1] #appends everything except very last node to new head
    
    def changeDirection(self, new_direction): # to stop snake from reversing into itself
        opposite_directions = {
            0: 1,
            1: 0,
            2: 3,
            3: 2
        }
        if (new_direction in opposite_directions and self.direction != opposite_directions[new_direction]): #not reversing
            self.direction = new_direction #change direction

    
