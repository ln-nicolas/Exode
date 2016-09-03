
uno= Board('/dev/cu.wchusbserial1420')

stepper = Stepper(pins=[8,10,9,11], steps=2100, speed=15)

stepperViewer= ExdViewerBox(target=stepper)
APP.STACK.add_widget(stepperViewer)

control = ExdSliderBox(minv=0, maxv=2100, target=stepper, value="pos")
APP.STACK.add_widget(control)
