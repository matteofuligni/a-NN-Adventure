# This file contains the class Ball, which is used to create a ball object in the environment.
from math import sin, cos
import numpy as np
import pygame
from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Ball:
    def __init__(self, x, y, dvx, dvy, radius, color):
        self.x = x
        self.y = y
        self.dvx = dvx
        self.dvy = dvy
        self.radius = radius
        self.color = color
        self.age = .0
        self.alive = True
        self.hp = 100
        self.neural_network = None
        self.vision = []
        self.vision_range = 50
        self.map = None
    
    def move_x(self):
        self.x += self.dvx
        
    def move_y(self):
        self.y += self.dvy
        
    def turn_right(self):
        self.dvx, self.dvy = -self.dvy, self.dvx
        
    def turn_left(self):
        self.dvx, self.dvy = self.dvy, -self.dvx
        
    def invert_direction(self):
        self.dvx, self.dvy = -self.dvx, -self.dvy
        
    def set_map(self, map):
        self.map = map
        
    def set_neural_network(self, neural_network):
        self.neural_network = neural_network
        
    #def turn_right(self, angle):
    #    self.dvx, self.dvy = self.dvx * cos(angle) - self.dvy * sin(angle), self.dvx * sin(angle) + self.dvy * cos(angle)
        
    #def turn_left(self, angle):
    #    self.dvx, self.dvy = self.dvx * cos(angle) + self.dvy * sin(angle), -self.dvx * sin(angle) + self.dvy * cos(angle)
    
    def gain_energy(self):
        self.hp += 10
        
    def lose_energy(self):
        self.hp -= 10
        
    def get_position(self):
        return self.x, self.y
            
    def get_hp(self):    
        return self.hp
    
    def get_age(self):
        return self.age
    
    def get_status(self):
        return self.alive
    
    def get_vision(self):
        return self.vision
    
    def get_radius(self):
        return self.radius
    
    def get_color(self):
        return self.color
    
    def is_outside_map(self, width, height):
        if self.x < 0 or self.x > width:
            self.alive = False
        if self.y < 0 or self.y > height:
            self.alive = False
        
    def render(self, surface):
        pygame.draw.circle(surface, self.color, self.get_position(), self.radius)
        
    def ai_decision(self, ambience):
        if self.neural_network is not None:
            self.vision = ambience
            decision = np.argmax(self.neural_network.make_decision(self.vision))
            if decision == 0:
                self.turn_left()
            elif decision == 1:
                self.turn_right()
            elif decision == 2:
                self.invert_direction()
            else:
                pass
                
    def update(self, ambience):
        self.ai_decision(ambience)
        self.move_x()
        self.move_y()
        self.age += 0.1
        
        # Sistemare il fattp che se il ball è fuori dallo schermo muore
        