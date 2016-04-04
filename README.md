# Exode
*version : beta 0.3*

Python's library for communication between Arduino microcontroller boards and a connected computer. Write Python script and take control on your board using a serial IO.


## Well, What is it ?
> Here, a code to blink a led

```python
from Exode import *

uno = Board('/dev/tty.wchusbserial1420')
led = Led(13)

led.blink(500)
```

Exode is a Python's library for communication between
Arduino microcontroller boards and a connected computer.
Write Python script and take control on your board using a serial IO.

##  Fast and Intuitive

Exode was designed to simplify the development of Arduino projects. The library
take advantages from the clear and light Python's syntax.

Once your Arduino connected to your device (computer, Rasberry Pi, smartphone ..)
using a serial IO (usb/bluetooth), you'r now allowed to have remote interactions
with your board.

You microcontroller become a simple slave, let your computer process the more
complexe tasks. You may add artificial intelligence algorithm in your projects...

## Powerfull tools

> Blink two led asynchronously

```python

from Exode import *
uno = Board('/dev/tty.HC-06-DevB')

led13 = Led(13)
led14 = Led(14)

led13.blink(250)
led14.blink(500)

```

Many of Arduino components are implemented in Exode, that's way you can directly
manipulate them with Python.

Exode use event-driven programming to manage the interactions between the differents
components plugged on your board, or your computer it-self.

Furthermore, the Exode's kernel is based on a asynchronous processes,
greatly simplifying your project !!
