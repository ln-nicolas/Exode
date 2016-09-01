uno= Board('/dev/cu.wchusbserial1420')

servo= Servo(13)
servoController= ExdSliderBox(minv=0, maxv=180,
                              target= servo, value="angle")

APP.STACK.add_widget(servoController)
