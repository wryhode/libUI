from pygame.math import *

class PhysObject():
    def __init__(self,startparams=None):
        self.name = None
        self.shape = None
        self.localtime = 0
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.acceleration = Vector2(0,0)
        self.size = Vector2(1,1)
        self.mass = 1

        if startparams != None:
            self.__dict__ == startparams

    def force_friction(self):
        pass

    def step(self,deltaTime):
        self.velocity += self.acceleration * deltaTime
        self.position += self.velocity * deltaTime
        self.localtime += deltaTime