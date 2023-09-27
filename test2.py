import libUI
import unitConverter

app = libUI.Application([1768,1000])

canvas = app.Canvas(app.window.resolution,[0,0],app.window)
font = app.Font("./Rubik-Regular.ttf",32)
mainLayer = app.Layer()
mainUpdateLayer = app.UpdateLayer()

commandLineWidth = 0.8
commandLineSize = app.utils.fracDomain([commandLineWidth,0.25],app.window.resolution)

commandLineHistoryLength = 32
commandLineHistory = app.Canvas(
    [
        commandLineSize[0],
        font.sizeOf("e")[1]*commandLineHistoryLength
    ],
    [0,0],
    canvas
)
commandLineInput = app.TextInput(
    [
        (0,0),
        (commandLineSize[0],font.sizeOf("e")[1])
    ],
    canvas,
    font,
    [255,255,255]
)

objectPanel = app.Canvas(
    app.utils.fracDomain([1-commandLineWidth,1],app.window.resolution),
    [commandLineSize[0],0],
    canvas
)
objectPanel.canvas.fill([255,0,0])

slider = app.Slider([100,120,15,500],True,canvas)
slider2 = app.Slider([100,80,500,15],False,canvas)

mainLayer.addElements([commandLineHistory,commandLineInput,objectPanel,slider,slider2])
mainUpdateLayer.addCloneFromLayer(mainLayer)

while app.update():
    mainUpdateLayer.update(app)
    canvas.clear()

    

    mainLayer.draw()
    canvas.draw()
    app.draw()