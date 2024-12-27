import pygame
import sys
from environment.map import Map
from environment.ball import Ball
from environment.object import Food, Obstacle
import numpy as np

np.random.seed(42) 

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ball on Map')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Ball settings
ball_radius = 7

ball = Ball(width // 2, height // 2, 1, 1, ball_radius, BLUE)
#food = [Food(x, y) for x in range(0, width-50, 20) for y in range(0, height-50, 20)]
food = [Food(x, y) for x, y in np.random.randint(20, height-20, size=(10,2))]
obstacles = [Obstacle(x, y) for x, y in np.random.randint(20, height-20, size=(10,2))]
#food = [Food(x, y) for x, y in zip(np.random.randint(20, width-20, size=10), np.random.randint(20, height-20, size=10))]
map = Map(width, height)
map.add_ball(ball)
map.add_food_list(food)
map.add_obstacle_list(obstacles)
map.render(window)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    window.fill(BLACK)     
    map.update(window)
    
    if map.get_balls() == []:
        running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()