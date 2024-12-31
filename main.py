import pygame
import sys
from environment.map import Map
from environment.ball import Ball
from environment.object import Food, Obstacle
from models.neural_network import NeuralNetwork
import numpy as np

np.random.seed(42) 

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLUE2 = (0, 100, 255)

BLOCK_SIZE = 7
SPEED = 80

# Ball settings
ball_radius = 7

map = Map(width, height)

nn = NeuralNetwork(3, 10)
ball = Ball(width // 2, height // 2, 1, 0, BLOCK_SIZE, BLUE)
ball.set_neural_network(nn)
#food = [Food(x, y) for x in range(0, width-50, 20) for y in range(0, height-50, 20)]
food = [Food(x, y) for x, y in np.random.randint(20, height-20, size=(10,2))]
obstacles = [Obstacle(x, y) for x, y in np.random.randint(20, height-20, size=(10,2))]
#food = [Food(x, y) for x, y in zip(np.random.randint(20, width-20, size=10), np.random.randint(20, height-20, size=10))]

ball.set_map(map)
map.add_ball(ball)
map.add_food_list(food)
map.add_obstacle_list(obstacles)
#map.render()

i = 0
# Main loop
running = True
while running:
    
        
       
    map.update()
    
    
    if i == 500:
       pygame.quit()
    
    if map.get_balls() == []:
        running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
    
    i += 1

pygame.quit()
#sys.exit()

#print('Simulation ended! i = ', i)