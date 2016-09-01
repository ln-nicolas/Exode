
uno= Board('/dev/cu.wchusbserial1420')

led= Led(13)

#
#   LedViewer
#
ledViewer= ExdViewerBox(target=led)
APP.STACK.add_widget(ledViewer)

#
#   Led On/Off
#
ledViewer= ExdSwitchBox(target=led, value="lvl")
APP.STACK.add_widget(ledViewer)

#
#   Led blink period
#
ledController= ExdSliderBox(minv=0, maxv=1000,
                            target= led, value="period")
APP.STACK.add_widget(ledController)


#
#   Dig RealTime graph
#
ana = AnaPin(2, 'INPUT')
ana.setColor(color=[0.8, 0.08, 0.36, 1])

ana2 = AnaPin(3, 'INPUT')
ana2.setColor(color=[0.68, 0.84, 0.15, 1])

ana.setPlot(MeshLinePlot())
ledGraph = ExdTimeGraph(size="md", ymin=0, ymax=500)
ledGraph.add_plot(ana.plot)
APP.STACK.add_widget(ledGraph)

ana2.setPlot(MeshLinePlot())
ledGraph.add_plot(ana2.plot)

anaViewer= ExdViewerBox(target=ana)
APP.STACK.add_widget(anaViewer)

ana2Viewer= ExdViewerBox(target=ana2)
APP.STACK.add_widget(ana2Viewer)

ana.listen(100)
