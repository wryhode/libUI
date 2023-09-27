import libUI
import unitConverter

app = libUI.Application([800,640])

def removeText(dict):
    if mainLayer.hasElement(text):
        mainLayer.removeElement(text)
        mainUpdateLayer.removeElement(text)
    else:
        mainLayer.addElement(text)
        mainUpdateLayer.addElement(text)

app.addEventCallback("KeyDown",removeText)

canvas = app.Canvas(app.window.resolution,[0,0],app.window)

button = app.Button([10,10,200,100],canvas)
button2 = app.Button([10,120,200,100],canvas)

font = app.Font("./OpenSans.ttf",32)
text = app.Text(font,"Text",[255,255,255],[100,300],canvas)

tinput = app.TextInput([100,400,400,50],canvas,font,[255,255,255])

mainLayer = app.Layer()
mainUpdateLayer = app.UpdateLayer()

mainLayer.addElements([button,button2,text,tinput])
mainUpdateLayer.addCloneFromLayer(mainLayer)

while app.update():
    mainUpdateLayer.update(app)
    canvas.clear()

    text.text = "Hello, world!"

    mainLayer.draw()
    canvas.draw()
    app.draw()