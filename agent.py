import torch
import random
import numpy as np
from collections import deque
from game import Game
from model import Model, Trainer
from utils import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = .84
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Model( 14, 256, 4)
        self.train = Trainer(self.model, LEARNING_RATE, self.gamma)
    
    def get_state(Self, game):
        pass
    
    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.train_step(states, actions, rewards, next_states, game_overs)
    
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.train_step(state, action, reward, next_state, game_over)
    
    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            action = random.randint(0, 2)
            move[action] = 1
        else:
            state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state)
            action = torch.argmax(prediction).item()
            move[action] = 1
        return move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    scores = []
    mean = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = Game()
    keep_training = True
    
    while keep_training:
        state = game.get_state()
        move = agent.get_action(state)
        reward, game_over, score = game.play_step_AI(move)
        new_state = agent.get_state(game)
        
        agent.train_short_memory(state, move, reward, new_state, game_over)
        agent.remember(state, move, reward, new_state, game_over)
        
        if game_over:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
            
            print(f"Game {agent.n_games} Score: {score} Record: {record}")
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
        
        

if __name__ == "__main__":
    train()