from pygame.math import *
from math import sqrt, sin, cos, tan, radians

forces_unit_conversions = {
    "m":"mass",
    "g":"gravity_accel",
    "ro":"mass_density",
    "f":"friction",
    "V":"volume",
    "v":"velocity",
    "k":"airresistance",
    "e_x":"e_x",
    "e_y":"e_y"
}

forces_standard = {
    "G":"m*g",
    "B":"ro*V*g",
    "N":"-G",
    "R":"f*N",
    "F":"k*v**2",
    "-G":"-m*g",
    "-B":"-ro*V*g",
    "-N":"G",
    "-R":"-f*N",
    "-F":"-(k*v**2)"
}

userforces = {

}

class PhysObject():
    def __init__(self,startparams=None,parentworld = None):
        self.name = None                    # friendly name that is user defineable
        self.shape = None                   # to be used later
        self.localtime = 0                  # keeps time since simulation start for the object
        self.position = Vector2(0,0)        # m 
        self.velocity = Vector2(0,0)        # m/s
        self.acceleration = Vector2(0,0)    # m/s^2
        self.size = Vector2(1,1)            # m - visual size
        self.depth = 1                      # Z "depth" - sets volume
        self.volume = self.size.x * self.size.y * self.depth    # initial value is decided by visual size
        self.mass = 10                     # kg
        self.friction = 0.5                 # 
        self.airresistance = 1.02           # 
        self.run = False                    # simulate?
        self.parentworld = parentworld      # to get gravity etc.
        self.e_x = Vector2(1,0)
        self.e_y = Vector2(0,1)
        self.f_sum = Vector2(0,0)
        if startparams != None:
            self.__dict__ == startparams

        self.attribs_to_display = []

        self.forces = {
            "G":"G",
            "N":"N",
            "A":"e_x*10",
            "-R":"-R"
        }

        self.toLog = []

        self.logs = {}

    @property
    def gravity(self):
        return self.parentworld.gravity_accel
    
    @property
    def massdensity(self):
        return self.parentworld.mass_density

    def parse_force(self,force,direction):
        if direction:
            index = 0   # X
        else:
            index = 1   # Y

        for k in forces_unit_conversions:
            v = forces_unit_conversions[k]
            try:
                value = self.__dict__[v]
            except KeyError:
                value = self.parentworld.__dict__[v]
            
            if not isinstance(value,Vector2):
                value = Vector2(float(value),float(value))

            force = force.replace(k,str(value[index]))

        cleared = True

        return eval(force)

    def force_sum(self):
        forcesX = []
        forcesY = []
        for k in self.forces:
            if k in forces_standard:    # is premade formula
                while k in forces_standard:
                    force = forces_standard[k]
                    k = forces_standard[k]
            elif k in userforces:
                force = userforces[k]
            else:
                force = self.forces[k]
            
            forcesX.append(self.parse_force(force,True))
            forcesY.append(self.parse_force(force,False))

        return Vector2(sum(forcesX),sum(forcesY))

    def forces_to_acceleration(self):
        self.f_sum = self.force_sum()
        return self.f_sum / self.mass

    def step(self,deltaTime):
        if self.run:
            self.acceleration = self.forces_to_acceleration()
            self.velocity += (self.acceleration * deltaTime)
            self.position += (self.velocity * deltaTime) 
            self.localtime += deltaTime

            for v in self.toLog:
                if not v in self.logs:
                    self.logs[v] = []
                self.logs[v].append(self.__dict__[v])

class PhysWorld():
    def __init__(self):
        self.gravity_accel = Vector2(0,9.81)
        self.mass_density = 1.225

if __name__ == "__main__":
    w = PhysWorld()
    a = PhysObject(parentworld=w)
    a.run = True
    a.step(0.1)