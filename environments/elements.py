import pygame
import numpy as np

RED = (200,0,0)

BLOCK_SIZE = 20
#SPEED = 10

class Ball:
    def __init__(self, x, y, dx, dy, size):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.color = (255, 0, 0)
        self.speed = 20
        self.health = 100
        
    def change_direction(self, key):
        if key[pygame.K_LEFT]:
            self.dx = -self.speed
            self.dy = 0
        if key[pygame.K_RIGHT]:
            self.dx = self.speed
            self.dy = 0
        if key[pygame.K_UP]:
            self.dx = 0
            self.dy = -self.speed
        if key[pygame.K_DOWN]:
            self.dx = 0
            self.dy = self.speed
            
    def change_direction_AI(self, action):
        if np.array_equal(action, [1, 0, 0, 0]):
            self.dx = -self.speed
            self.dy = 0
        if np.array_equal(action, [0, 1, 0, 0]):
            self.dx = self.speed
            self.dy = 0
        if np.array_equal(action, [0, 0, 1, 0]):
            self.dx = 0
            self.dy = -self.speed
        if  np.array_equal(action, [0, 0, 0, 1]):
            self.dx = 0
            self.dy = self.speed
            
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        
    def bounce(self):
        self.dx = -self.dx
        self.dy = -self.dy
        
    def get_direction(self):
        if self.dx == self.speed:
            return [1, 0, 0, 0]
        elif self.dx == -self.speed:
            return [0, 1, 0, 0]
        elif self.dy == self.speed:
            return [0, 0, 1, 0]
        else:
            return [0, 0, 0, 1]
           
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.color = (0, 255, 0)
        
    def render(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        
    def get_positoion(self):
        return [self.x, self.y]
        
class Obstacle:
    def __init__(self, x, y, shape="square"):
        self.x = x
        self.y = y
        self.size = 20
        self.color = (0, 0, 0)
        self.shape = shape
        
    def render(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        elif self.shape == "triangle":
            pygame.draw.polygon(screen, self.color, [(self.x, self.y), (self.x + self.size, self.y), (self.x + self.size // 2, self.y - self.size)])
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def get_position(self):
        return [self.x, self.y]
            
class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color_1 = (0, 0, 0)
        self.color_2 = (200, 0, 0)
        
    def render(self, screen):
        pygame.draw.rect(screen, self.color_1, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, self.color_2, (self.x + self.size/5, self.y + self.size/5, 3*self.size/5, 3*self.size/5))
        
    def get_position(self):
        return [self.x, self.y]
