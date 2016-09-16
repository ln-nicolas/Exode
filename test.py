from Exode import *
uno = Board('/dev/tty.HC-06-DevB')

#Init the HCSR04 (ER ultrasound) and a Led
hcsr = HCSR04(echo=9, trig=8)
led  = Led(13)

#Define a control function
def control():
    if hcsr.cm() < 10:
      led.write(1)
    else:
      led.write(0)

#Bind the event to the function
hcsr.attachEvent('update', control)

#Setup the read every 100ms
hcsr.read(100)
