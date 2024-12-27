import pygame

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5
        self.color = (0, 255, 0)

    def render(self, surface):    
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)
        

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.color = (255, 0, 0)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        