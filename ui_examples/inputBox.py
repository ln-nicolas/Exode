uno= Board('/dev/cu.wchusbserial1420')

led= Led(13)
led.setColor([0.84, 0.34, 0.67])

ledController= ExdTextInputBox(target= led, value="period", size="sm")
APP.STACK.add_widget(ledController)
