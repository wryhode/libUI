# --------
#   title:      phySim
#   version:    beta version 0
#   author:     wryhode       
# --------

import libUI
import unitConverter
from phys import PhysObject, PhysWorld
from commandLine import parseCommand

class Application():
    def __init__(self,resolution):
        self.app = libUI.Application(resolution,libUI.pygame.RESIZABLE)
        self.app.attachResizeBehaviour(self.reBuildInterface)

        self.mainLayer = self.app.Layer()
        self.mainUpdateLayer = self.app.UpdateLayer()

        self.UIsizing = self.app.ElementCollection()
        self.UIsizing.vertSplit = 0.75
        self.UIsizing.commandLineHeight = 0.2
        self.UIsizing.commandLineHistoryLength = 5
        self.UIsizing.objectsMenuHeight = 0.5
        self.UIsizing.objectsMenuNumItems = 10
        self.UIsizing.propertyMenuHeight = 0.25

        self.commandLineHistoryLength = 25
        self.commandLineHistory = [None] * self.commandLineHistoryLength

        self.physObjects = {}

        self.reBuildInterface()

    def reBuildInterface(self):
        self.canvas = self.app.Canvas(self.app.window.resolution,[0,0],self.app.window)
        self.font = self.app.Font("./Rubik-Regular.ttf",int(self.app.window.resolution[1]/31.25))
        self.smallFont = self.app.Font("./Rubik-Regular.ttf",int(self.app.window.resolution[1]/62.5))
        self.LargeFont = self.app.Font("./Rubik-Regular.ttf",int(self.app.window.resolution[1]/16.125))

        self.UIsizing.commandLineSize = self.app.utils.fracDomain([self.UIsizing.vertSplit,self.UIsizing.commandLineHeight],self.app.window.resolution)
        self.UIsizing.sideBarSize = self.app.utils.fracDomain([1-self.UIsizing.vertSplit,1],self.app.window.resolution)
        self.UIsizing.sideBarPosition = self.app.utils.fracDomain([self.UIsizing.vertSplit,0],self.app.window.resolution)
        self.UIsizing.objectsMenuSize = self.app.utils.fracDomain([1,self.UIsizing.objectsMenuHeight],self.UIsizing.sideBarSize)
        self.UIsizing.objectsMenuItemSize = self.app.utils.fracDomain([1,1/self.UIsizing.objectsMenuNumItems],self.UIsizing.objectsMenuSize)
        self.UIsizing.propertyMenuPosition = self.app.utils.fracDomain([0,1-self.UIsizing.propertyMenuHeight],self.app.window.resolution)
        self.UIsizing.propertyMenuSize = self.app.utils.fracDomain([self.UIsizing.vertSplit,self.UIsizing.propertyMenuHeight],self.app.window.resolution)
        self.UIsizing.workspaceSize = self.app.utils.fracDomain([self.UIsizing.vertSplit,1-(self.UIsizing.commandLineHeight+self.UIsizing.propertyMenuHeight)],self.app.window.resolution)
        self.UIsizing.workspacePosition = self.app.utils.fracDomain([0,self.UIsizing.commandLineHeight],self.app.window.resolution)

        # Dont duplicate elements
        self.mainLayer.removeAll()
        self.mainUpdateLayer.removeAll()

        self.commandLine = self.app.ElementCollection()
        self.commandLine.canvas = self.app.Canvas(self.UIsizing.commandLineSize,[0,0],self.canvas)
        self.commandLine.history = self.app.Canvas([self.commandLine.canvas.rect.width,(self.commandLine.canvas.rect.height / self.UIsizing.commandLineHistoryLength) * (self.UIsizing.commandLineHistoryLength-1)],[0,0],self.canvas)
        self.commandLine.longHistory = self.app.Canvas([self.commandLine.canvas.rect.width,self.font.sizeOf("L")[1]*25],[0,0],self.commandLine.history)
        for i in range(self.commandLineHistoryLength):
            self.commandLine.longHistory.canvas.blit(self.font.font.render(str(self.commandLineHistory[i]),True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))

        self.commandLine.slider = self.app.Slider([self.commandLine.canvas.rect.width-25,0,25,self.commandLine.history.rect.height+1],True,self.canvas)
        self.commandLine.input = self.app.TextInput([0,self.commandLine.history.rect.height,self.commandLine.canvas.rect.width,(self.commandLine.canvas.rect.height / self.UIsizing.commandLineHistoryLength)],self.commandLine.canvas,self.font,[255,255,255])
        self.commandLine.input.callback = self.parseCommandline

        self.sideBar = self.app.ElementCollection()
        self.sideBar.canvas = self.app.Canvas(self.UIsizing.sideBarSize,self.UIsizing.sideBarPosition,self.canvas)
        self.sideBar.canvas.canvas.fill([25,25,25])

        self.objectsMenu = self.app.ElementCollection()
        self.objectsMenu.canvas = self.app.Canvas(self.UIsizing.objectsMenuSize,[0,0],self.sideBar.canvas)
        self.objectsMenu.header = self.app.Canvas(self.UIsizing.objectsMenuItemSize,[0,0],self.objectsMenu.canvas)
        self.objectsMenu.header.canvas.fill([25,25,25])
        self.objectsMenu.scrollCanvas = self.app.Canvas([self.UIsizing.objectsMenuSize[0],self.UIsizing.objectsMenuItemSize[1]*20],[0,self.UIsizing.objectsMenuItemSize[1]],self.objectsMenu.canvas)
        self.objectsMenu.slider = self.app.Slider([0,self.UIsizing.objectsMenuItemSize[1],25,self.objectsMenu.canvas.rect.height-self.UIsizing.objectsMenuItemSize[1]],True,self.sideBar.canvas)
        libUI.pygame.draw.rect(self.objectsMenu.header.canvas,[114,114,114],self.objectsMenu.header.rect,1)

        self.propertyMenu = self.app.ElementCollection()
        self.propertyMenu.canvas = self.app.Canvas(self.UIsizing.propertyMenuSize,self.UIsizing.propertyMenuPosition,self.canvas)
        self.propertyMenu.canvas.canvas.fill([25,25,25])

        self.workspace = self.app.ElementCollection()
        self.workspace.canvas = self.app.Canvas(self.UIsizing.workspaceSize,self.UIsizing.workspacePosition,self.canvas)
        self.workspace.canvas.canvas.fill([33,33,33])

        self.mainLayer.addElementCollection(self.commandLine)
        self.mainLayer.addElementCollection(self.objectsMenu)
        self.mainLayer.addElementCollection(self.sideBar)
        self.mainLayer.addElementCollection(self.propertyMenu)
        self.mainLayer.addElementCollection(self.workspace)
        self.mainUpdateLayer.addCloneFromLayer(self.mainLayer)

    def redrawCommandHistory(self):
        self.commandLine.longHistory.canvas.fill([0,0,0])
        for i in range(self.commandLineHistoryLength):
            if self.commandLineHistory[i] == None:
                self.commandLine.longHistory.canvas.blit(self.font.font.render("...",True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))
            else:
                self.commandLine.longHistory.canvas.blit(self.font.font.render(str(self.commandLineHistory[i]),True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))

    def resizeOnKey(self,dict):
        self.reBuildInterface()

    def createPhysObject(self,name):
        if not name in self.physObjects:
            self.physObjects[name] = PhysObject()
            self.physObjects[name].name = name
            return True
        else:
            return False,"Object already exists"

    def deletePhysObject(self,name):
        del self.physObjects[name]

    def parseCommandline(self,cinput):
        """
        command = cinput.split(" ")
        target = command[0].lower()

        if target == "new":
            name = command[1]
            self.createPhysObject(name)
            
        elif target == "set":
            name = command[1]
            attrib = command[2]
            value = command[3].split(",")
            print(value)
            self.physObjects[name].__dict__[attrib] = libUI.pygame.math.Vector2(float(value[0]),float(value[1]))
        """

        command = parseCommand(cinput)
        output = ""

        if command[0] == "new":
            self.createPhysObject(command[1])
        
        elif command[0] == "set":
            try:
                self.physObjects[command[1]]
            except KeyError:
                output += f" >> name {command[1]} is not defined"
                return
            try:
                self.physObjects[command[1]].__dict__[command[2]]
            except KeyError:
                output += f" >> parameter {command[2]} is not defined"
                return
            try:
                self.physObjects[command[1]].__dict__[command[2]] = command[3]
            except :
                output += f" >> parameter {command[3]} is of wrong data type"
                return

        elif command[0] == "delete":
            self.deletePhysObject(command[1])

        elif command[0] == "display":
            if command[1] == "off":
                self.physObjects[command[2]].attribs_to_display.remove(command[3])
            else:
                self.physObjects[command[1]].attribs_to_display.append(command[2])

        elif command[0] == "function":
            pass

        self.commandLineHistory.insert(0,cinput + output)
        self.commandLineHistory.pop(self.commandLineHistoryLength)
        self.redrawCommandHistory()

    def translatePhysToScreen(self,po):
        a = po
        # 1 pixel / 1 cm
        a.position = a.position * 100
        a.size = a.size * 100
        return a

    # This is incredibly stupid, but botches will be botchin'
    def backTranslate(self,po):
        a = po
        # 1 pixel / 1 cm
        a.position = a.position / 100
        a.size = a.size / 100

    def run(self):
        while self.app.update():
            self.mainUpdateLayer.update(self.app)
            self.canvas.clear([33,33,33])

            # Scroll commandline history
            self.commandLine.longHistory.rect.y = -self.commandLine.slider.value * (self.commandLine.longHistory.rect.height-self.commandLine.history.rect.height)

            self.workspace.canvas.canvas.fill([33,33,33])
            for o in self.physObjects:
                po = self.physObjects[o]
                po.step(self.app.dt)

                to = self.translatePhysToScreen(po)

                libUI.pygame.draw.rect(self.workspace.canvas.canvas,[255,0,0],(to.position,to.size))
                self.workspace.canvas.canvas.blit(self.smallFont.font.render(po.name,True,[255,255,255]),(to.position))

                for i,t in enumerate(po.attribs_to_display):
                    self.workspace.canvas.canvas.blit(self.smallFont.font.render(str(po.__dict__[t]),True,[255,255,255]),(to.position[0],to.position[1]+((i+1)*self.smallFont.sizeOf("L")[1])))

                self.backTranslate(po)

            self.mainLayer.draw()
            self.canvas.draw()
            self.app.draw()

if __name__ == "__main__":
    app = Application([1777,1000])
    app.run()