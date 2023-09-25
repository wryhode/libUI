import pygame
import libUI
import math

app = libUI.Application([800,480])

canvas = app.Canvas([250,250],[0,0],app.window)
c2 = app.Canvas([50,50],[200,200],canvas)

def printKey(dict):
    c2.clear()
    pygame.draw.line(c2.canvas,[255,0,0],(0,0),(50,50))

app.addEventCallback("KeyDown",printKey)
sprite = app.Sprite([200,200,150,150],canvas)

img = app.Image("./512x512.jpg")
sprite.canvas = img.image

layer = app.Layer()
layer.addElements([c2,sprite,canvas])

while app.update():
    for e in app.events:
        pass
        
    canvas.clear()
    
    layer.depthSort()
    
    c2.position = [math.sin(app.window.frame/50)*32,math.cos(app.window.frame/50)*32]
        
    pygame.draw.line(canvas.canvas,[255,0,0],(0,0),(50,50))
    canvas.canvas.blit(img.image,(0,0))
    layer.draw()
    app.draw()
    
app.quit()
exit()