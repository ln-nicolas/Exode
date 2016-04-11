from Exode import *

uno= Board('/dev/cu.wchusbserial1420')

pin=DigPin(13,'OUTPUT')

print("led 13 : on then off")

pin.write('HIGH')
delay(500)
pin.switch()


print("led 13 : blink 100ms")

pin.periodicSwitch(100)
delay(1500)
pin.stopPeriodicSwitch()


print("read lvl pin 13:")

pin.mode('INPUT')
pin.read()
print(pin._lvl)

# Emulate a fake button over the pin
fake_button= DigPin(13,'OUTPUT')
fake_button.periodicSwitch(500)

print("listen led 13")

def printMsg(msg):
    print(msg)

pin.attachEvent("on",printMsg,"is on !")
pin.listen()

delay(5000)

fake_button.stopPeriodicSwitch()
pin.stopListen()