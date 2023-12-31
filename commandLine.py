from pygame.math import Vector2, Vector3
from math import sqrt,sin,cos,tan,radians

class CommandParameters():
    def __init__(self):
        self._parameters = {}

def parseCommand(command):
    cmd = CommandParameters()

    inp = command.split(" ")

    params = []
    while len(inp) > 0:
        parameter = inp[0]
        if "{" in parameter:
            parameter = eval(parameter)
        elif "[" in parameter:
            parameter = eval(parameter)            
        elif "," in parameter:
            vect = parameter.strip().split(",")
            parameter = Vector2(float(vect[0]),float(vect[1]))
        elif parameter.replace(".", "").isnumeric():
            parameter = float(parameter)

        else:
            pass # Let it stay as a string
        params.append(parameter)
        inp.pop(0)
    
    return params