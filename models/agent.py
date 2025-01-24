import torch
import random
import numpy as np
from collections import deque
from game import Game

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.n_gamse = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
    
    def get_state(Self, game):
        pass
    
    def remember(self, state, action, reward, next_state, game_over):
        pass
    
    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, game_over):
        pass
    
    def get_action(self, state):
        pass
    
def train():
    scores = []
    mean = []
    total_score = 0
    best_score = 0
    agent = Agent()
    game = Game()
    keep_training = True
    
    while keep_training:
        state = agent.get_state(game)
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
        
        

if __name__ == "__main__":
    train()