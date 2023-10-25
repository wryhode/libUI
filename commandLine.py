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
        params.append(inp[0])
        inp.pop(0)
    
    return params