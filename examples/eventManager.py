from Exode import *

uno= Board('/dev/cu.wchusbserial1420')

pin=DigPin(13,'OUTPUT')
led=Led(13)

def switchedEvent():
    print("hey hey !")

pin.attachEvent("switch", switchedEvent)
pin.listen()

led.blink(3000)

uno.wait()