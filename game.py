import pygame
import random
from environments.elements import Ball, Food, Obstacle, Wall

WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SPEED = 20
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)


class Game:
    def __init__(self, width, height, screen_color):
        self.width = width
        self.height = height
        self.balls = []
        self.food = []
        self.obstacles = []
        self.walls = []
        self.scree_color = screen_color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My First Game")
        self.screen.fill(self.scree_color)
        self.clock = pygame.time.Clock()
        self.reset()
        self.font = pygame.font.Font(None, 36)
        
    def reset(self):
        self.score = 0
        self.foods = []
        self._generate_food()
        self.balls = []
        self._generate_ball()
        self.obstacles = []
        self._generate_obstacles()
        self.walls = []
        self._generate_walls()
        self.frame_iteration = 0
        
    def update_ui(self, key):
        # Aggiornare la finestra
        self.screen.fill(WHITE)
        self.check_collision()
        self.check_out_of_bounds()
        for food in self.foods:
            food.render(self.screen)
        for obstacle in self.obstacles:
            obstacle.render(self.screen)
        for wall in self.walls:
            wall.render(self.screen)
        for ball in self.balls:
            ball.change_direction(key)
            ball.move()
            ball.render(self.screen)
            health = ball.health
            if health <= 0:
                self.reset()
        text = self.font.render("Health: " + str(health), True, BLACK)
        self.screen.blit(text, [BLOCK_SIZE*1.1, BLOCK_SIZE*1.1])
        pygame.display.flip()
        
    def _generate_ball(self):
        self.balls.append(Ball(WIDTH // 2 + BLOCK_SIZE//2, HEIGHT // 2 + BLOCK_SIZE//2, SPEED, 0, BLOCK_SIZE//2))
        
    def _generate_food(self, number_of_foods=10):
        def generate_food():
            x = random.randint(1, (WIDTH//BLOCK_SIZE - 2)) * BLOCK_SIZE
            y = random.randint(1, (HEIGHT//BLOCK_SIZE - 2)) * BLOCK_SIZE
            self.foods.append(Food(x+BLOCK_SIZE//2, y+BLOCK_SIZE//2))
        [generate_food() for _ in range(number_of_foods)]
    
    def _generate_obstacles(self, number_of_obstacles=15):
        def generate_obstacle():
            x = random.randint(1, (WIDTH//BLOCK_SIZE - 1)) * BLOCK_SIZE
            y = random.randint(1, (HEIGHT//BLOCK_SIZE - 1)) * BLOCK_SIZE
            self.obstacles.append(Obstacle(x, y))
        [generate_obstacle() for _ in range(number_of_obstacles)]
        
    def check_collision(self):
        def distance(x1, y1, x2, y2):
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

        for ball in self.balls:
            for food in self.foods:
                if distance(ball.x, ball.y, food.x, food.y) < ball.size + food.size:
                    ball.health += 10
                    self.foods.remove(food)
                    self._generate_food(1)
            for obstacle in self.obstacles:
                if distance(ball.x, ball.y, (obstacle.x + obstacle.size // 2), (obstacle.y + obstacle.size // 2)) < ball.size + obstacle.size//2:
                    ball.health -= 10
                    self.obstacles.remove(obstacle)
                    self._generate_obstacles(1)
            if ball.x - ball.size == BLOCK_SIZE or ball.x + ball.size == WIDTH - BLOCK_SIZE or ball.y - ball.size == BLOCK_SIZE or ball.y + ball.size == HEIGHT - BLOCK_SIZE:
                ball.health -= 10
                self.reset()
                
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
                self.reset()