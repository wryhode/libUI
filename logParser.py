logFile = open("./log copy.txt","r")

import libUI

class Simulator():
    def __init__(self):
        self.events = []
        self.eventPointer = 0

    def run(self):
        self.app = libUI.Application([200,200],self.flags)

    def executeEvent(self,ev):
        command = ev["command"]
        if command == "setWindowSize":
            self.app.resize(ev["param1"])

    def step(self):
        self.executeEvent(self.events[self.eventPointer])
        self.eventPointer += 1

sim = Simulator()
sim.flags = 0

for l in logFile.readlines():
    logLine = l.split(" ")
    print(logLine)
    if logLine[0].strip(":") == "WINDOW":
        if logLine[1] == "New":
            sim.events.append({"command"})
        elif logLine[1] == "Set" and logLine[3] == "title":

            print("Set window title")

print("Simulating...")
sim.run()