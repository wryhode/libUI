import pygame
import libUI
import unitConverter

app = libUI.Application([800,640])

canvas = app.Canvas(app.window.resolution,[0,0],app.window)

button = app.Button([10,10,200,100],canvas)
button.canvas.fill([255,0,0])

font = app.Font("./OpenSans.ttf",32)
text = app.Text(font,"Hello, world!",[255,255,255],[10,10],canvas)

mainLayer = app.Layer()
mainLayer.addElements([button,text])

while app.update():
    button.update(app.mouse)
    canvas.clear()

    mainLayer.draw()
    canvas.draw()
    app.draw()