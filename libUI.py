import pygame
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
            self.rect = rect
            self.parent = parent
            
            Sprite.__init__(self)
    
    class Layer():
        def __init__(self):
            self.toDraw = []
        
        def addElement(self,element):
            self.toDraw.append(element)
        
        def addElements(self,iterable):
            for i in iterable:
                self.addElement(i)
        
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
                i.parent.canvas.blit(i.canvas,i.position)
    
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