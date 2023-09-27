# Tiny self-installer if the user doesn't have pygame installed
try:
    import pygame

except ImportError:
    print("This program requires the module 'PyGame' to run")
    answer = str(input("Do you want me to install it for you? (Y/N) [This will run 'pip install pygame'] >")).upper()

    if answer == "Y":
        import os
        print("Installing...")
        os.system("pip install pygame")
        print()
        print("Trying to start now...")
        import pygame
    
    else:
        print("Ok. Type 'pip install pygame' to install it later.")
        exit()

# Assume all went well
from pygame.locals import *
pygame.init()

class Application():
    class Window():
        def __init__(self,resolution,flags=0):
            self.resolution = resolution
            self.flags = flags
            self.position = [0,0]
            self.framerate = 60
            self.frame = 0
            self.canvas = pygame.display.set_mode(self.resolution,flags)

    class Image():
        def __init__(self,path):
            try:
                self.sourceImage = pygame.image.load(path)
            except FileExistsError:
                self.sourceImage = pygame.Surface([64,64])
                self.sourceImage.fill([255,0,255])

        @property
        def image(self):
            return self.sourceImage
        
        @property
        def size(self):
            return self.sourceImage.get_size()
            
    class Canvas():
        def __init__(self,resolution,position,parent):
            self.rect = pygame.Rect(position,resolution)
            self.parent = parent
            self.canvas = pygame.Surface(self.resolution)
            
        def draw(self):
            bp = self.position
            self.parent.canvas.blit(self.canvas,bp)
        
        def clear(self,color=[0,0,0]):
            self.canvas.fill(color)
        
        @property
        def c(self):
            return self.canvas
            
        @property
        def resolution(self):
            return self.rect.size
         
        @property
        def position(self):
            return self.rect.topleft
            
        @position.setter
        def position(self,position):
            self.rect.topleft = position
                    
        @resolution.setter
        def resolution(self,resolution):
            self.rect.size = resolution
            self.canvas = pygame.Surface(resolution)
            
        def update(self):
            pass

    class Sprite(pygame.sprite.Sprite):
        def __init__(self, rect, parent):
            self.rect = pygame.Rect(rect)
            self.image = pygame.Surface(self.rect.size)
            self.parent = parent
            
            pygame.sprite.Sprite.__init__(self)
            
        def draw(self):
            self.parent.canvas.blit(self.image,self.position)
        
        @property
        def canvas(self):
            return self.image
            
        @canvas.setter
        def canvas(self,img):
            self.image = img
        
        @property
        def position(self):
            return self.rect.topleft
        
        @property
        def resolution(self):
            return self.rect.size
    
    class Button(Sprite):
        def __init__(self,rect,parent):
            Application.Sprite.__init__(self,rect,parent)

            # Draw button image
            self.drawUnPressed()

            self.held = False
            self.touchPosition = [0,0]
            self.reDrew = False

        def drawPressed(self):
            self.canvas.fill([92,51,76])
            pygame.draw.rect(self.canvas,[168,43,121],[5,0,self.rect.width-5,self.rect.height-5])
            pygame.draw.rect(self.canvas,[219,57,157],[5,5,self.rect.width-10,self.rect.height-10])
            self.reDrew = True

        def drawUnPressed(self):
            self.canvas.fill([92,51,76])
            pygame.draw.rect(self.canvas,[168,43,121],[5,0,self.rect.width-5,self.rect.height-5])
            pygame.draw.rect(self.canvas,[92,24,66],[5,5,self.rect.width-10,self.rect.height-10])
            self.reDrew = True

        def clampTouchPos(self,v):
            if v < 0: return 0
            if v > 1: return 1
            return v

        def update(self,mouse):
            if self.rect.collidepoint(mouse.position):
                if mouse.downState[0]:
                    self.held = True
                    self.drawPressed()

            if self.held:
                self.touchPosition[0] = self.clampTouchPos((self.rect.x - mouse.position[0]) / -self.rect.width)
                self.touchPosition[1] = self.clampTouchPos((self.rect.y - mouse.position[1]) / -self.rect.height)

            if not mouse.buttons[0]:
                self.drawUnPressed()
                self.held = False

        def draw(self):
            self.parent.canvas.blit(self.canvas,self.rect.topleft)
    
    class Font():
        def __init__(self,path,size):
            self.font = pygame.font.Font(path,size)

        def sizeOf(self,input):
            return self.font.size(str(input))

    class Text():
        def __init__(self,font,text,color,position,parent):
            self.font = font
            self.text = text
            self.prevText = self.text
            self.color = color
            self.rect = pygame.Rect(position,[0,0])
            self.parent = parent

            self.reDraw()

        def reDraw(self):
            self.canvas = self.font.font.render(str(self.text),True,self.color)
            self.rect = pygame.Rect(self.rect.topleft,self.canvas.get_size())

        def softUpdate(self):
            # Detects if the text has changed and automatically updates it
            if self.text != self.prevText:
                self.reDraw()
                self.prevText = self.text

        def update(self):
            self.softUpdate()

        def draw(self):
            self.softUpdate()
            self.parent.canvas.blit(self.canvas,self.rect)
            
        @property
        def position(self):
            return self.rect.topleft

    class TextInput(Button):
        def __init__(self,rect,parent,font,color):
            Application.Button.__init__(self,rect,parent)
            
            self.input = ""
            self.focused = False
            self.font = font
            self.color = color
            self.textCanvas = self.font.font.render("TextInput element",True,self.color)
        
        def update(self, mouse):
            super().update(mouse)

            if self.held:
                self.focused = True
            
            if mouse.downState[0] and not self.rect.collidepoint(mouse.position) and not self.held:
                self.focused = False

            if self.focused:
                self.canvas.fill([255,0,0])

        def draw(self):
            if self.reDrew:
                self.canvas.blit(self.textCanvas,(0,0))
                self.reDrew = False

            self.parent.canvas.blit(self.canvas,self.rect.topleft)

    class Slider(Button):
        def __init__(self,rect,direction,parent):
            Application.Button.__init__(self,rect,parent)

            self.direction = direction # True -> Vertical, False -> Horizontal

            if self.direction:
                self.sliderHead = Application.Sprite([(0,0),(self.rect.width,self.rect.width)],self)
            else:
                self.sliderHead = Application.Sprite([(0,0),(self.rect.height,self.rect.height)],self)

            self.sliderHead.canvas.fill([255,0,0])

        def update(self, mouse):
            super().update(mouse)

            if self.held:
                self.drawPressed()
                if self.direction:
                    self.sliderHead.rect.topleft = 0,self.touchPosition[1] * self.rect.height
                else:
                    self.sliderHead.rect.topleft = self.touchPosition[0] * self.rect.width,0

            self.sliderHead.draw()

    class Layer():
        def __init__(self):
            self.toDraw = []
        
        def addElement(self,element):
            self.toDraw.append(element)
        
        def addElements(self,iterable):
            for i in iterable:
                self.addElement(i)

        def removeElement(self,element):
            if self.hasElement(element):
                self.toDraw.remove(element)

        def removeElements(self,iterable):
            for i in iterable:
                self.removeElement(i)
        
        def hasElement(self,element):
            return element in self.toDraw
        
        def _depthSortKey(self,e):
            return -e.position[1]
            
        def _depthSortKeyRev(self,e):
            return -e.position[1]
        
        def depthSort(self,reverse=False):
            """Sorts all the layers by Y position"""
            if reverse:
                self.toDraw.sort(key=self._depthSortKeyRev)
            else:
                self.toDraw.sort(key=self._depthSortKey)
        
        def draw(self):
            for i in self.toDraw:
                i.draw()
                #i.parent.canvas.blit(i.canvas,i.position)

        def addCloneFromUpdateLayer(self,updateLayer):
            for i in updateLayer.toUpdate:
                self.toDraw.append(i)
    
    class UpdateLayer():
        def __init__(self):
            self.toUpdate = []

        def addElement(self,element):
            self.toUpdate.append(element)
        
        def addElements(self,iterable):
            for i in iterable:
                self.addElement(i)

        def removeElement(self,element):
            if self.hasElement(element):
                self.toUpdate.remove(element)

        def removeElements(self,iterable):
            for i in iterable:
                self.removeElement(i)

        def hasElement(self,element):
            return element in self.toUpdate

        def addCloneFromLayer(self,layer):
            for i in layer.toDraw:
                self.toUpdate.append(i)

        def update(self,app):
            for e in self.toUpdate:
                if isinstance(e,Application.Button):
                    e.update(app.mouse)
                else:
                        e.update()

    class Utils():
        def __init__(self):
            pass
            
        def clamp(self,v,mi,ma):
            if v > ma: return ma
            if v < mi: return mi
            return v
            
        def fracDomain(self,fracPos,sizePixels):
            # Automatically get size if a Canvas is passed
            if isinstance(sizePixels,Application.Canvas) or isinstance(sizePixels,Application.Window):
                sizePixels = sizePixels.resolution
            return sizePixels[0]*self.clamp(fracPos[0],0,1),sizePixels[1]*self.clamp(fracPos[1],0,1)
            
        def isIterable(self,variable):
            try:
                iter(variable)
            except TypeError:
                return False
            else:
                return True
                
    class Mouse():
        def __init__(self):
            self.position = [0,0]
            self.speed = [0,0]
            self.buttons = [False,False,False]
            self.upState = [False,False,False]
            self.downState = [False,False,False]

        def update(self):
            self.position = pygame.mouse.get_pos()
            self.speed = pygame.mouse.get_rel()
            
            pressed = pygame.mouse.get_pressed()

            for i,b in enumerate(pressed):
                if pressed[i] and self.buttons[i] == False:
                    self.downState[i] = True

                elif pressed[i] and self.buttons[i]:
                    self.downState[i] = False

                else:
                    self.downState[i] = False

                if self.buttons[i] and pressed[i] == False:
                    self.upState[i] = True

                else:
                    self.upState[i] = False

            self.buttons = pressed
    
    def __init__(self,windowResolution,flags=0):
        self.window = self.Window(windowResolution,flags)
        self.mouse = self.Mouse()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.utils = self.Utils()
        self.evCallbacks = {}
      
    def update(self):
        run = True
        self.events = pygame.event.get()
        for e in self.events:
            en = pygame.event.event_name(e.type)
            # Handle user defined event callbacks
            if en in self.evCallbacks:
                # Nothing to compare
                if self.evCallbacks[en]["dict"] == None:
                    self.evCallbacks[en]["func"](e.__dict__)
                else:
                    for ek in self.evCallbacks[en]["dict"]:
                        try:
                            if e.__dict__[ek] == self.evCallbacks[en]["dict"][ek]:
                                self.evCallbacks[en]["func"](e.__dict__)
                        # Key does not exist
                        except KeyError:
                            pass
                
            if e.type == pygame.QUIT:
                run = False
        
        self.dt = self.clock.tick(self.window.framerate) / 1000
        self.mouse.update()
        
        # Clear window, expect constant updates to canvas.draw()
        self.window.canvas.fill([0,0,0])
        return run
        
    def draw(self):
        self.window.frame += 1
        pygame.display.update()
    
    def quit(self):
        pygame.quit()
        
    def resize(self,newResolution):
        self.window.__init__(newResolution,self.window.flags)
    
    def addEventCallback(self,eventName,function,dictToTest = None):
        self.evCallbacks[eventName] = {"func":function,"dict":dictToTest}

if __name__ == "__main__":
    print("This script is not to be ran, please run another one in this folder (or subfolder)")