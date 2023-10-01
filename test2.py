import libUI
import unitConverter

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

        # Dont duplicate elements
        self.mainLayer.removeAll()
        self.mainUpdateLayer.removeAll()

        self.commandLine = self.app.ElementCollection()
        self.commandLine.canvas = self.app.Canvas(self.UIsizing.commandLineSize,[0,0],self.canvas)
        self.commandLine.history = self.app.Canvas([self.commandLine.canvas.rect.width,(self.commandLine.canvas.rect.height / self.UIsizing.commandLineHistoryLength) * (self.UIsizing.commandLineHistoryLength-1)],[0,0],self.canvas)
        self.commandLine.longHistory = self.app.Canvas([self.commandLine.canvas.rect.width,self.font.sizeOf("L")[1]*25],[0,0],self.commandLine.history)
        for i in range(25):
            self.commandLine.longHistory.canvas.blit(self.font.font.render("Element: "+str(i),True,[255,255,255]),(0,i*self.font.sizeOf("L")[1]))

        self.commandLine.slider = self.app.Slider([self.commandLine.canvas.rect.width-25,0,25,self.commandLine.history.rect.height+1],True,self.canvas)
        self.commandLine.input = self.app.TextInput([0,self.commandLine.history.rect.height,self.commandLine.canvas.rect.width,(self.commandLine.canvas.rect.height / self.UIsizing.commandLineHistoryLength)],self.commandLine.canvas,self.font,[255,255,255])
        self.commandLine.input.callback = self.printInput

        self.sideBar = self.app.ElementCollection()
        self.sideBar.canvas = self.app.Canvas(self.UIsizing.sideBarSize,self.UIsizing.sideBarPosition,self.canvas)
        self.sideBar.canvas.canvas.fill([25,25,25])

        self.objectsMenu = self.app.ElementCollection()
        self.objectsMenu.canvas = self.app.Canvas(self.UIsizing.objectsMenuSize,[0,0],self.sideBar.canvas)
        self.objectsMenu.header = self.app.Canvas(self.UIsizing.objectsMenuItemSize,[0,0],self.objectsMenu.canvas)
        self.objectsMenu.header.canvas.fill([25,25,25])

        self.mainLayer.addElementCollection(self.commandLine)
        self.mainLayer.addElementCollection(self.objectsMenu)
        self.mainLayer.addElementCollection(self.sideBar)
        self.mainUpdateLayer.addCloneFromLayer(self.mainLayer)

    def resizeOnKey(self,dict):
        self.reBuildInterface()

    def printInput(self,input):
        print(input)

    def run(self):
        while self.app.update():
            self.mainUpdateLayer.update(self.app)
            self.canvas.clear([33,33,33])

            # Scroll commandline history
            self.commandLine.longHistory.rect.y = -self.commandLine.slider.value * (self.commandLine.longHistory.rect.height-self.commandLine.history.rect.height)

            self.mainLayer.draw()
            self.canvas.draw()
            self.app.draw()

if __name__ == "__main__":
    app = Application([1777,1000])
    app.run()