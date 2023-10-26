from pygame.math import Vector2, Vector3

class CommandParameters():
    def __init__(self):
        self._parameters = {}

def parseCommand(command):
    cmd = CommandParameters()

    inp = command.split(" ")
    
    """
    if len(inp) > 0:
        cmd.command = inp[0]

        if len(inp) > 1:
            cmd.name = inp[1]

            if len(inp) > 2:
                cmd.attribute = inp[2]
    """

    params = []
    while len(inp) > 0:
        parameter = inp[0]
        if "," in parameter:
            vect = parameter.strip().split(",")
            parameter = Vector2(float(vect[0]),float(vect[1]))
        elif parameter.isnumeric():
            parameter = float(parameter)
        else:
            pass # Let it stay as a string
        params.append(parameter)
        inp.pop(0)
    
    return params