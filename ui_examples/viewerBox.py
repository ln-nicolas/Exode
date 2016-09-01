uno= Board('/dev/cu.wchusbserial1420')

servo= Servo(13, name="servo13")
servo.setColor([0.05, 0.75, 0.85])

servoViewer= ExdViewerBox(target= servo, size="xl")
APP.STACK.add_widget(servoViewer)
