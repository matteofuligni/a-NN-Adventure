import pygame
import random
import numpy as np
from elements import Ball, Food, Obstacle, Wall

WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SPEED = 20
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

pygame.init()
font = pygame.font.Font("arial.ttf", 36)

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT, screen_color=WHITE):
        self.width = width
        self.height = height
        self.balls = []
        self.foods = []
        self.obstacles = []
        self.walls = []
        self.reward = 0
        self.score = 0
        self.game_over = False
        self.scree_color = screen_color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My First Game")
        self.screen.fill(self.scree_color)
        self.clock = pygame.time.Clock()
        self.reset()
        self.font = pygame.font.Font("arial.ttf", 36)
        
    def reset(self):
        self.reward = 0
        self.score = 0
        self.game_over = False
        self.foods = []
        self._generate_food()
        self.balls = []
        self._generate_ball()
        self.obstacles = []
        self._generate_obstacles()
        self.walls = []
        self._generate_walls()
        self.frame_iteration = 0
        
    def update_ui(self):
        self.screen.fill(WHITE)
        for food in self.foods:
            food.render(self.screen)
        for obstacle in self.obstacles:
            obstacle.render(self.screen)
        for wall in self.walls:
            wall.render(self.screen)
        for ball in self.balls:
            ball.render(self.screen)
        text = self.font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(text, [BLOCK_SIZE*1.1, BLOCK_SIZE*1.1])
        pygame.display.flip()
        self.clock.tick(60)
        
    def play_step(self, key): 
        self.frame_iteration += 1
        for ball in self.balls:
            ball.change_direction(key)
            ball.move()
            self.check_collision()
            self.check_out_of_bounds()
            health = ball.health
            if health <= 0:
                self.reward = 10
                self.game_over = True
            if self.frame_iteration > 1000:
                self.reward = -10
                self.game_over = True
        return self.reward, self.game_over
    
    def play_step_AI(self, action): 
        self.frame_iteration += 1
        for ball in self.balls:
            ball.change_direction_AI(action)
            ball.move()
            self.game_over = self.check_collision(ball)
            self.game_over = self.check_out_of_bounds()
            #health = ball.health
            #if health < 0:
            #    self.reward = -10
            #    self.game_over = True
            if self.frame_iteration > 10000:
                #self.reward = -10
                self.game_over = True
        return self.reward, self.game_over, self.score
        
    def get_state(self):
        def flatten_state(state):
            flat_state = []
            for item in state:
                if isinstance(item, list):  # If the item is a list, extend the flat_state
                    flat_state.extend(item)
                else:  # If the item is an integer, append it directly
                    flat_state.append(item)
            return flat_state
        
        for ball in self.balls:
            state = []
            state.append(ball.get_direction())
            if self.check_obstacle(ball.x+BLOCK_SIZE, ball.y, ball.size) or self.check_wall(ball.x+BLOCK_SIZE, ball.y, ball.size):
                state.append(1) 
            else:
                state.append(0)
            if self.check_obstacle(ball.x-BLOCK_SIZE, ball.y, ball.size) or self.check_wall(ball.x-BLOCK_SIZE, ball.y, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_obstacle(ball.x, ball.y+BLOCK_SIZE, ball.size) or self.check_wall(ball.x, ball.y+BLOCK_SIZE, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_obstacle(ball.x, ball.y-BLOCK_SIZE, ball.size) or self.check_wall(ball.x, ball.y-BLOCK_SIZE, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_food(ball.x+BLOCK_SIZE, ball.y, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_food(ball.x-BLOCK_SIZE, ball.y, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_food(ball.x, ball.y+BLOCK_SIZE, ball.size):
                state.append(1)
            else:
                state.append(0)
            if self.check_food(ball.x, ball.y-BLOCK_SIZE, ball.size):    
                state.append(1)
            else:
                state.append(0)
            state.append(self.get_nearest_food(ball.x, ball.y))
            state = flatten_state(state)
        return np.array(state, dtype=int)

    def _generate_ball(self):
        self.balls.append(Ball(WIDTH // 2 + BLOCK_SIZE//2, HEIGHT // 2 + BLOCK_SIZE//2, SPEED, 0, BLOCK_SIZE//2))
        
    def _generate_food(self, number_of_foods=10):
        def generate_food():
            x = random.randint(1, (WIDTH//BLOCK_SIZE - 2)) * BLOCK_SIZE
            y = random.randint(1, (HEIGHT//BLOCK_SIZE - 2)) * BLOCK_SIZE
            self.foods.append(Food(x+BLOCK_SIZE//2, y+BLOCK_SIZE//2))
        [generate_food() for _ in range(number_of_foods)]
    
    def _generate_obstacles(self, number_of_obstacles=0):
        def generate_obstacle():
            x = random.randint(1, (WIDTH//BLOCK_SIZE - 1)) * BLOCK_SIZE
            y = random.randint(1, (HEIGHT//BLOCK_SIZE - 1)) * BLOCK_SIZE
            self.obstacles.append(Obstacle(x, y))
        [generate_obstacle() for _ in range(number_of_obstacles)]
        
    def check_collision(self, ball):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        ball_x, ball_y, ball_size = ball.x, ball.y, ball.size
        for food in self.foods:
            if distance(ball_x, ball_y, food.x, food.y) < ball_size + food.size:
                self.score += 1
                self.reward = 10
                self.foods.remove(food)
                self._generate_food(1)
                #ball.health += 10
        for obstacle in self.obstacles:
            if distance(ball_x, ball_y, (obstacle.x + obstacle.size // 2), (obstacle.y + obstacle.size // 2)) < ball_size + obstacle.size//2:
                self.score -= 1
                self.reward = -10
                self.obstacles.remove(obstacle)
                self._generate_obstacles(1)
                #ball.health -= 10
                return True
        if ball_x - ball_size == BLOCK_SIZE or ball_x + ball_size == WIDTH - BLOCK_SIZE or ball_y - ball_size == BLOCK_SIZE or ball_y + ball_size == HEIGHT - BLOCK_SIZE:
            self.reward = -10
            #self.game_over = True
            #ball.health -= 100
            return True
        return False
                
    def check_food(self, ball_x, ball_y, ball_size):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        for food in self.foods:
            if distance(ball_x, ball_y, food.x, food.y) < ball_size + food.size:
                # Removed object removal and new generation
                return True
        return False
    
    def check_obstacle(self, ball_x, ball_y, ball_size):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        for obstacle in self.obstacles:
            if distance(ball_x, ball_y, (obstacle.x + obstacle.size // 2), (obstacle.y + obstacle.size // 2)) < ball_size + obstacle.size//2:
                # Removed object removal and new generation
                return True
        return False
    
    def check_wall(self, ball_x, ball_y, ball_size):
        if ball_x - ball_size == BLOCK_SIZE or ball_x + ball_size == WIDTH - BLOCK_SIZE or ball_y - ball_size == BLOCK_SIZE or ball_y + ball_size == HEIGHT - BLOCK_SIZE:
            #self.score -= 10
            self.game_over = True
            return True
        return False
        
    def get_nearest_food(self, ball_x, ball_y):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        min_distance = 10000
        state = []
        for food in self.foods:
            if distance(ball_x, ball_y, food.x, food.y) < min_distance:
                min_distance = distance(ball_x, ball_y, food.x, food.y)
                min_x, min_y = food.x, food.y
        if min_x > ball_x:
            state.append(1)
        else:
            state.append(0)
        if min_y > ball_y:
            state.append(1)
        else:
            state.append(0)
        return state

    def _generate_walls(self):
        def generate_wall(x=0, y=0):
            self.walls.append(Wall(x, y))
        [generate_wall(x=x) for x in range(0, WIDTH, BLOCK_SIZE)]
        [generate_wall(y=y) for y in range(0, HEIGHT, BLOCK_SIZE)]
        [generate_wall(x=x, y=HEIGHT-BLOCK_SIZE) for x in range(0, WIDTH, BLOCK_SIZE)]
        [generate_wall(x=WIDTH-BLOCK_SIZE, y=y) for y in range(0, HEIGHT, BLOCK_SIZE)]

    def check_out_of_bounds(self):
        for ball in self.balls:
            if ball.x < BLOCK_SIZE or ball.x > WIDTH - BLOCK_SIZE or ball.y < BLOCK_SIZE or ball.y > HEIGHT - BLOCK_SIZE:
                return True
        return False