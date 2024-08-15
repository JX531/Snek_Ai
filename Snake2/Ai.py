import numpy as np
import random
import pickle
import os

class AI:
    def __init__(self, gridsize = 10, alpha =0.2, gamma = 0.9, epsilon = 0.0):
        self.q_table = {}
        self.actions = [0,1,2,3]
        self.gridsize = gridsize

        self.alpha = alpha #learning rate
        self.gamma = gamma #discount 
        self.epsilon = epsilon #exploration 

    def getState(self,snake_body,apple,direction):
        head = snake_body[0]
        
        state = (head[0], head[1], direction, #head position, direction
                 (apple[0] - head[0] > 0), (apple[0] - head[0] < 0), #apple left? or right?
                 (apple[1] - head[1] > 0), (apple[1] - head[1] < 0), #apple up? or down?
                 self.isUnsafe(snake_body,head[0]+1,head[1]), #unsafe around head adjacent
                 self.isUnsafe(snake_body,head[0]-1,head[1]),
                 self.isUnsafe(snake_body,head[0],head[1]+1),
                 self.isUnsafe(snake_body,head[0],head[1]-1),

                 self.isUnsafe(snake_body,head[0]+1,head[1]+1), #unsafe around head diagonal
                 self.isUnsafe(snake_body,head[0]-1,head[1]+1),
                 self.isUnsafe(snake_body,head[0]+1,head[1]-1),
                 self.isUnsafe(snake_body,head[0]-1,head[1]-1)) 

        
        return state
    
    def isUnsafe(self,body,a,b):
        if ([a,b] in body): #[a,b] is body segment
            return 1
        if (a < 0 or a >= self.gridsize): #[a,b] is outside boundary
            return 1
        if (b< 0 or b >= self.gridsize):
            return 1
        
        return 0

    def getQvalue(self,state,action):
        if (state not in self.q_table): #first time entering state
            self.q_table[state] = [0]* len(self.actions) #init to all 0s
        return self.q_table[state][action] #return value of the action taken in given state
    
    def nextAction(self,state):
        if (random.uniform(0,1) < self.epsilon): #pick random action
            return random.choice(range(len(self.actions)))
        else:
            q_values = [self.getQvalue(state,a) for a in range(len(self.actions))] #get q values for current state
            return np.argmax(q_values) #take highest value action
    
    def learn(self, state, action, reward, next_state, terminal=False):
        q_predict = self.getQvalue(state, action)
        if terminal:
            q_actual = reward  # No future rewards after a terminal state
        else:
            q_actual = reward + self.gamma * max(self.getQvalue(next_state, a) for a in range(len(self.actions)))
        self.q_table[state][action] += self.alpha * (q_actual - q_predict)

    
    def save(self):
        temp_filename = 'Snake_Qtable_temp.pkl'
        final_filename = 'Snake_Qtable.pkl'
        
        # Write to the temporary file first
        with open(temp_filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        
        # Replace the old file with the new one
        if os.path.exists(final_filename):
            os.remove(final_filename)  # Remove the old file
        
        os.replace(temp_filename, final_filename)  # Replace the old file with the new file
    
    def load(self):
        with open('Snake_Qtable.pkl','rb') as f:
            self.q_table = pickle.load(f)

    def load_partial(self):
        try:
            with open('Snake_Qtable.pkl', 'rb') as f:
                data = pickle.load(f)
            return data
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error loading file: {e}")
            return None
        
#agent = AI()

#Attempt to load the partially corrupted file

# data = agent.load_partial()

# if data is None:
#     print("File is corrupted and cannot be fully recovered.")
#     # Handle the case where the file is not recoverable
#     data = {}  # Start fresh

# agent.save()





