# --------
#   title:      phySim
#   version:    beta version 0
#   author:     wryhode       
# --------

import libUI
import unitConverter
from phys import PhysObject, PhysWorld, userforces
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

        self.physWorld = PhysWorld()
        self.physObjects = {}
        self.cmPerPixel = 25
        self.workspaceOriginOffset = libUI.pygame.math.Vector2(0,0)

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
        self.UIsizing.objectsMenuItemSize = self.app.utils.fracDomain([1,1/self.UIsizing.objectsMenuNumItems],[self.UIsizing.objectsMenuSize[0]-25,self.UIsizing.objectsMenuSize[1]])
        self.UIsizing.objectsMenuHeaderSize = self.app.utils.fracDomain([1,1/self.UIsizing.objectsMenuNumItems],self.UIsizing.objectsMenuSize)
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
        self.objectsMenu.header = self.app.Canvas(self.UIsizing.objectsMenuHeaderSize,[0,0],self.objectsMenu.canvas)
        self.objectsMenu.header.canvas.fill([25,25,25])
        self.objectsMenu.scrollCanvas = self.app.Canvas([self.UIsizing.objectsMenuSize[0],self.UIsizing.objectsMenuItemSize[1]*20],[25,self.UIsizing.objectsMenuItemSize[1]],self.objectsMenu.canvas)
        self.objectsMenu.slider = self.app.Slider([0,self.UIsizing.objectsMenuItemSize[1],25,self.objectsMenu.canvas.rect.height-self.UIsizing.objectsMenuItemSize[1]],True,self.sideBar.canvas)
        libUI.pygame.draw.rect(self.objectsMenu.header.canvas,[114,114,114],self.objectsMenu.header.rect,1)
        self.objectsMenu.header.canvas.blit(self.font.font.render("Objects",True,[255,255,255]),[0,0])
        self.redrawObjects()

        self.propertyMenu = self.app.ElementCollection()
        self.propertyMenu.canvas = self.app.Canvas(self.UIsizing.propertyMenuSize,self.UIsizing.propertyMenuPosition,self.canvas)
        self.propertyMenu.canvas.canvas.fill([25,25,25])

        self.workspace = self.app.ElementCollection()
        self.workspace.canvas = self.app.Canvas(self.UIsizing.workspaceSize,self.UIsizing.workspacePosition,self.canvas)
        self.workspace.canvas.canvas.fill([33,33,33])
        self.workspace.gridCanvas = self.app.Canvas(self.UIsizing.workspaceSize,[0,0],self.workspace.canvas)

        self.mainLayer.addElementCollection(self.commandLine)
        self.mainLayer.addElementCollection(self.objectsMenu)
        self.mainLayer.addElementCollection(self.sideBar)
        self.mainLayer.addElementCollection(self.propertyMenu)
        self.mainLayer.addElementCollection(self.workspace)
        self.mainUpdateLayer.addCloneFromLayer(self.mainLayer)

    def drawObjectsMenuItem(self,size):
        canvas = self.app.Canvas(size,[0,0],None)
        libUI.pygame.draw.rect(canvas.canvas,[114,114,114],[[0,0],size],1)
        return canvas

    def redrawObjects(self):
        self.objectsMenu.scrollCanvas.canvas.fill([0,0,0])
        self.objectsMenu.objectSelectors = self.app.ElementCollection()
        self.objectsMenu.objectSelectors.buttons = []
        baseCanvas = self.drawObjectsMenuItem(self.UIsizing.objectsMenuItemSize)
        for i,o in enumerate(self.physObjects):
            self.objectsMenu.objectSelectors.buttons.append(self.app.Button([[0,i*self.UIsizing.objectsMenuItemSize[1]-1],self.UIsizing.objectsMenuItemSize],self.objectsMenu.scrollCanvas))
            self.objectsMenu.scrollCanvas.canvas.blit(baseCanvas.canvas,[0,i*self.UIsizing.objectsMenuItemSize[1]-1])

    def redrawCommandHistory(self):
        self.commandLine.longHistory.canvas.fill([0,0,0])
        for i in range(self.commandLineHistoryLength):
            if self.commandLineHistory[i] == None:
                self.commandLine.longHistory.canvas.blit(self.font.font.render("...",True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))
            else:
                self.commandLine.longHistory.canvas.blit(self.font.font.render(str(self.commandLineHistory[i]),True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))

    def clearWorkspace(self):
        self.drawWorkspaceGrid()
        self.workspace.canvas.canvas.blit(self.workspace.gridCanvas.canvas,[0,0])

    def drawWorkspaceGrid(self):
        self.workspace.gridCanvas.canvas.fill([33,33,33])
        wsRect = self.workspace.gridCanvas.rect
        value = self.cmPerPixel
        for y in range(0,wsRect.height,value):
            coord = y - self.workspaceOriginOffset.y % self.cmPerPixel
            libUI.pygame.draw.line(self.workspace.gridCanvas.canvas,[66,66,66],[0,coord],[wsRect.width,coord])
        for x in range(0,wsRect.width,value):
            coord = x - self.workspaceOriginOffset.x % self.cmPerPixel
            libUI.pygame.draw.line(self.workspace.gridCanvas.canvas,[66,66,66],[coord,0],[coord,wsRect.height])

    def resizeOnKey(self,dict):
        self.reBuildInterface()

    def createPhysObject(self,name):
        if not name in self.physObjects:
            self.physObjects[name] = PhysObject(parentworld=self.physWorld)
            self.physObjects[name].name = name
            self.redrawObjects()
            return True
        else:
            return False,"Object already exists"

    def createForce(self,name,function):
        if not name in userforces:
            userforces[name] = function
            return True
        else:
            return False,"Function already exists"

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
            if command[1].lower() == "force":
                self.createForce(command[2],command[3])
            else:
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
        a.position = a.position * self.cmPerPixel
        a.size = a.size * self.cmPerPixel
        return a

    # This is incredibly stupid, but botches will be botchin'
    def backTranslate(self,po):
        a = po
        # 1 pixel / 1 cm
        a.position = a.position / self.cmPerPixel
        a.size = a.size / self.cmPerPixel

    def worldToScreen(self,coord):
        return libUI.pygame.math.Vector2(coord - self.workspaceOriginOffset)

    def run(self):
        while self.app.update():
            for e in self.app.events:
                if e.type == libUI.pygame.MOUSEWHEEL:
                    self.cmPerPixel += e.y
                    if self.cmPerPixel < 1: self.cmPerPixel = 1

            if self.app.mouse.buttons[1]:
                self.workspaceOriginOffset -= libUI.pygame.math.Vector2(self.app.mouse.speed)

            self.mainUpdateLayer.update(self.app)
            self.canvas.clear([33,33,33])

            # Scroll commandline history
            self.commandLine.longHistory.rect.y = -self.commandLine.slider.value * (self.commandLine.longHistory.rect.height-self.commandLine.history.rect.height)

            self.clearWorkspace()
            for o in self.physObjects:
                po = self.physObjects[o]
                for i in range(100):
                    po.step(self.app.dt / 100)

                to = self.translatePhysToScreen(po)

                objectPos = self.worldToScreen(to.position)
                libUI.pygame.draw.rect(self.workspace.canvas.canvas,[255,0,0],(objectPos,to.size))
                libUI.pygame.draw.line(self.workspace.canvas.canvas,[0,255,0],objectPos,objectPos+to.velocity*40)
                libUI.pygame.draw.line(self.workspace.canvas.canvas,[255,0,0],objectPos,objectPos+to.acceleration*40)
                libUI.pygame.draw.line(self.workspace.canvas.canvas,[255,255,255],objectPos,objectPos+to.f_sum*40)

                self.workspace.canvas.canvas.blit(self.smallFont.font.render(po.name,True,[255,255,255]),(objectPos))

                for i,t in enumerate(po.attribs_to_display):
                    self.workspace.canvas.canvas.blit(self.smallFont.font.render(str(po.__dict__[t]),True,[255,255,255]),(objectPos.x,objectPos.y+((i+1)*self.smallFont.sizeOf("L")[1])))

                self.backTranslate(po)

            self.mainLayer.draw()
            if self.app.mouse.buttons[1]:
                self.canvas.canvas.blit(self.font.font.render(str(self.workspaceOriginOffset),True,[255,255,255]),(0,0))
            self.canvas.draw()
            self.app.draw()

if __name__ == "__main__":
    app = Application([1777,1000])
    app.run()