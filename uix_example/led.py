
uno= Board('/dev/cu.wchusbserial1420')

led= Led(13)

#
#   LedViewer
#
ledViewer= ExdViewer(led)
APP.STACK.add_widget(ledViewer)

#
#   Led On/Off
#
ledViewer= ExdRadio(target=led, name="Led ON/OFF")
APP.STACK.add_widget(ledViewer)

#
#   Led blink period
#
ledController= ExdSlider(minv=0, maxv=1000,
                         target= led, valueName="period",
                         name= "Led period")
APP.STACK.add_widget(ledController)

#
#   Dig RealTime graph
#
dig = DigPin(2, 'INPUT')
dig.setColor(color=[0.8, 0.08, 0.36, 1])

ledplot  = MeshLinePlot()
dig.setPlot(ledplot)
ledGraph = ExdRealTimeGraph("Led Graph")
ledGraph.add_plot(ledplot)
APP.STACK.add_widget(ledGraph)

dig.listen(100)

#
# DigViewer
#
digViewer= ExdViewer(dig)
APP.STACK.add_widget(digViewer)
