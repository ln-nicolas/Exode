from ..Core.callback import *
from .model import obj

_VARIABLES = {
    0:0,
    1:1,
    'OUTPUT':1,
    'INPUT':0,
    'HIGH':1,
    'LOW': 0,
    'ON':1,
    'OFF':0,
}

class DigPin(obj):

    def __init__(self, pin, mode, analogic=False):

        self.board = None

        self._pin = pin
        self._mode = _VARIABLES[mode]
        self._analog=analogic

        self._lvl = 0

        self._listenThread = None
        self._writeThread = None

        obj.__init__(self, "digPin("+str(self._pin)+")")
        self.setupEvent(["switch","on","off"])

    def setup(self, board):
        self.board = board
        board.add(self)

        board.addObject("digPin",self)
        board.pinMode(self._pin, self._mode, analogic=self._analog)
        self.log(".mode("+str(self._mode)+")")

    def mode(self, mode):
        self._mode = mode
        self.board.pinMode(self._pin, mode, analogic=self._analog)
        self.log(".mode("+str(self._mode)+")")


    def write(self, lvl):
        if self._mode == 1:
            self._lvl = _VARIABLES[lvl]
            self.board.digitalWrite(self._pin, self._lvl)
            self.log(".write("+str(self._lvl)+")")

    def analogWrite(self, value):
        self.value = value
        self.board.analogWrite(self._pin, self.value)
        self.log(".analogWrite("+str(value)+")")

    def switch(self):
        self.board.digitalSwitch(self._pin)
        self.log(".swith()")

    def read(self):
        key = self.board.getKey()
        self.board.digitalRead(self._pin, key)
        self.board.addListener(key= key, updateFunction=self.update)
        self.log(".read()")

    def update(self, lvl):
        if self._lvl != lvl:
            self.event("switch").call()
            self.log(":switched")
        self._lvl = lvl

        if self._lvl == 1:
            self.event("on").call()
            self.event("on").off()
            self.event("off").on()
            self.log(":on")

        if self._lvl == 0:
            self.event("off").call()
            self.event("off").off()
            self.event("on").on()
            self.log(":off")

    def listen(self, period = 100):
        if self._listenThread == None:
            key = self.board.getKey()
            self._listenThread = self.board.newThread()
            self._listenThread.add('digitalRead', self._pin, key)
            self.board.addListener(key=key, updateFunction=self.update, isInfinite=True)
            self._listenThread.start(period)
        else:
            self._listenThread.stop()
            self._listenThread.start(period)

        self.log(".listen("+str(period)+")")

    def stopListen(self):
        self._listenThread.stop()
        self.log(".stopListen()")

    def periodicSwitch(self, period):
        if self._writeThread == None:
            self._writeThread = self.board.newThread()
            self._writeThread.add('digitalSwitch', self._pin)
            self._writeThread.start(period)
        else:
            self._writeThread.stop()
            self._writeThread.start(period)
        self.log(".periodicSwitch("+str(period)+")")

    def stopPeriodicSwitch(self):
        self._writeThread.stop()
        self.log(".stopPeriodic()")

class AnaPin(obj):

    def __init__(self, pin, mode):

        self.board = None

        self._pin = pin
        self._mode = _VARIABLES[mode]

        self.value = 0

        self._listenThread = None

        obj.__init__(self, "anaPin("+str(self._pin)+")")
        self.setupEvent(["update"])

    def setup(self, board):
        self.board = board
        board.add(self)

        board.addObject("anaPin",self)
        board.pinMode(self._pin, self._mode, analogic=True)
        self.log(".AnaPinMode("+str(self._mode)+")")

    def update(self, value):
        self.value = value
        self.log(":read "+str(value))
        self.event("update").call()

    def mode(self, mode):
        self._mode = _VARIABLES[mode]
        self.board.pinMode(self._pin, mode, analogic=True)
        self.log(".mode("+str(mode)+")")

    def read(self):
        key = self.board.getKey()
        self.board.analogRead(self._pin, key)
        self.board.addListener(key= key, updateFunction=self.update)
        self.log(".read()")

    def listen(self, period= 100):
        if self._listenThread == None:
            key = self.board.getKey()
            self._listenThread = self.board.newThread()
            self._listenThread.add('analogRead', self._pin, key)
            self.board.addListener(key= key, updateFunction=self.update, isInfinite=True)
            self._listenThread.start(period)
        else:
            self._listenThread.stop()
            self._listenThread.start(period)
        self.log(".listen("+str(period)+")")

    def stopListen(self):
        self._listenThread.stop()
        self.log(".stopListen()")


class Button(DigPin):

    def __init__(self,pin):
        DigPin.__init__(self, pin, 'INPUT')


class Led(DigPin):

    def __init__(self, pin):
        DigPin.__init__(self, pin, 'OUTPUT')
    def blink(self, period):
        self.periodicSwitch(period)
    def stopBlink(self):
        self.stopPeriodicSwitch()
