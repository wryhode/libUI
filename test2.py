import pygame
import libUI

app = libUI.Application([800,640])

canvas = app.Canvas(app.window.resolution,[0,0],app.window)

button = app.Button([10,10,200,100],canvas)
button.canvas.fill([255,0,0])

mainLayer = app.Layer()
mainLayer.addElements([button])

while app.update():
    canvas.clear()

    

    mainLayer.draw()
    canvas.draw()
    app.draw()