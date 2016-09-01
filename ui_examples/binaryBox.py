uno= Board('/dev/cu.wchusbserial1410')

led= Led(13)

switchBox= ExdSwitchBox(target=led, value="lvl")
radioBox = ExdRadioBox(target=led, title="Led13", value="lvl")

APP.STACK.add_widget(switchBox)
APP.STACK.add_widget(radioBox)
