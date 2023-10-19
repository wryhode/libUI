from pygame.math import *

class PhysObject():
    def __init__(self):
        self.name = None
        self.shape = None
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.acceleration = Vector2(0,1)
        self.size = Vector2(50,50)
        self.mass = 1

    def force_friction(self):
        

    def step(self,deltaTime):
        self.velocity += self.acceleration * deltaTime
        self.position += self.velocity * deltaTime