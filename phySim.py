import libUI
import unitConverter
from phys import PhysObject

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
            self.commandLine.longHistory.canvas.blit(self.font.font.render(str(self.commandLineHistory[i]),True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))

    def resizeOnKey(self,dict):
        self.reBuildInterface()

    def createPhysObject(self,name):
        if not name in self.physObjects:
            self.physObjects[name] = PhysObject()
            return True
        else:
            return False,"Object already exists"

    def parseCommandline(self,cinput):
        self.commandLineHistory.insert(0,cinput)
        self.commandLineHistory.pop(self.commandLineHistoryLength)

        command = cinput.split(" ")
        target = command[0].lower()

        if target == "new":
            name = command[1]
            self.createPhysObject(name)

        self.redrawCommandHistory()

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

                libUI.pygame.draw.rect(self.workspace.canvas.canvas,[255,0,0],(po.position,po.size))

            self.mainLayer.draw()
            self.canvas.draw()
            self.app.draw()

if __name__ == "__main__":
    app = Application([1777,1000])
    app.run()