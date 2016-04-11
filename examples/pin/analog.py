from Exode import *

uno= Board('/dev/cu.wchusbserial1420')

analog= AnaPin(2, 'INPUT')

analog.read()
print(analog.value)

def printValue(pin):
  print(str(pin._pin)+": "+str(pin.value))

analog.attachEvent("update",printValue,analog)
analog.listen()

uno.wait(1000)
analog.stopListen()