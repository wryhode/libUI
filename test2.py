import libUI
import unitConverter

app = libUI.Application([800,640])

canvas = app.Canvas(app.window.resolution,[0,0],app.window)

button = app.Button([10,10,200,100],canvas)
button2 = app.Button([10,120,200,100],canvas)

font = app.Font("./OpenSans.ttf",32)
text = app.Text(font,"Text",[255,255,255],[100,300],canvas)

mainLayer = app.Layer()
mainUpdateLayer = app.UpdateLayer()

mainLayer.addElements([button,button2,text])
mainUpdateLayer.addCloneFromLayer(mainLayer)

while app.update():
    mainUpdateLayer.update(app)
    canvas.clear()

    text.text = "Hello, world!"

    mainLayer.draw()
    canvas.draw()
    app.draw()