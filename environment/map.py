
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLUE2 = (0, 100, 255)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('A NN Adventure')
        self.clock = pygame.time.Clock()
        #self.reset()
        self.balls = []
        self.food = []
        self.obstacles = []
        
    def add_ball(self, ball):
        self.balls.append(ball)
        
    def add_signle_food(self, food):
        self.food.append(food)
        
    def add_food_list(self, food_list):
        self.food = food_list
        
    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
    
    def add_obstacle_list(self, obstacle_list):
        self.obstacles = obstacle_list
        
    def remove_ball(self, ball):
        self.balls.remove(ball)
    
    def remove_food(self, food):
        self.food.remove(food)
    
    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)
        
    def get_balls(self):
        return self.balls
        
    def render(self, wall):
        for ball in self.balls:
            ball.render(wall)
        for item in self.food:
            item.render(wall)
        for obstacle in self.obstacles:
            obstacle.render(wall)
            
    def update(self):
        self.display.fill(BLACK)  
        for ball in self.balls:
            pygame.draw.circle(self.display, ball.color, ball.get_position(), ball.radius)
            ambience = self.get_ambience(ball)
            for food in self.food:
                food.render(self.display)
                if ball.x == food.x and ball.y == food.y:
                    ball.gain_energy()
                    self.remove_food(food)
            for obstacle in self.obstacles:
                obstacle.render(self.display)
                if ball.x == obstacle.x and ball.y == obstacle.y:
                    ball.lose_energy()
                    if self.get_hp() == 0:
                        ball.alive = False
            ball.is_outside_map(self.width, self.height)
            if ball.get_status() == False:
                self.remove_ball(ball)
            ball.update(ambience)
            
        text = pygame.font.SysFont('arial', 25).render("hp: " + str(ball.hp), True, WHITE)
        self.display.blit(text, [0, 0])
            
    def get_ambience(self, ball):
        vision_range = ball.vision_range
        ambience = []
        for x in range(ball.x - vision_range, ball.x + vision_range + 1):
            for y in range(ball.y - vision_range, ball.y + vision_range + 1):
                if x < 0 or x > self.width or y < 0 or y > self.height:
                    ambience.append((x, y, -1))  # Wall or obstacle
                else:
                    found = False
                    for food in self.food:
                        if food.x == x and food.y == y:
                            ambience.append((x, y, 1))  # Food
                            found = True
                            break
                    if not found:
                        for obstacle in self.obstacles:
                            if obstacle.x == x and obstacle.y == y:
                                ambience.append((x, y, -1))  # Obstacle
                                found = True
                                break
                    if not found:
                        ambience.append((x, y, 0))  # Empty space
        return ambience