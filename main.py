import pygame
import sys
from environments import elements
from game import Game
import random

random.seed(42) 

WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

#BLOCK_SIZE = 10
SPEED = 10

WIDTH = 800
HEIGHT = 600


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    
    game = Game(WIDTH, HEIGHT, WHITE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        reward, game_over = game.play_step(keys)
        game.update_ui()
        if game_over:
            game.reset()
        

        # Regolare il framerate
        pygame.time.Clock().tick(60)

    # Uscita da Pygame
    pygame.quit()
    sys.exit()