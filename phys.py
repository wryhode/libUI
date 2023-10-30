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
        self.friction = 0.5
        self.run = False

        if startparams != None:
            self.__dict__ == startparams

        self.attribs_to_display = []

    def force_friction(self):
        pass

    def step(self,deltaTime):
        self.velocity += (self.acceleration * deltaTime) * self.run
        self.position += (self.velocity * deltaTime) * self.run
        self.localtime += deltaTime * self.run

class PhysWorld():
    def __init__(self):
        self.gravity_accel = Vector2(0,9.81)