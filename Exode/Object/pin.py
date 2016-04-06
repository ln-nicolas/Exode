from ..Core.boardManager import *
from ..Core.callback import *
from ..Core import logObj

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

class DigPin:

    def __init__(self, pin, mode):

        self.board = None

        self._pin = pin
        self._mode = _VARIABLES[mode]

        self._lvl = 0

        self._listenThread = None
        self._writeThread = None

        self._event = {
        "switch" : CallBack(),
        "on" : CallBack(),
        "off" : CallBack()
        }

        BOARD_MANAGER.autoAddObj(self)

    def __repr__(self):
        return str(self.board)+"."+"digPin("+self._pin+")"

    def log(self, msg):
        logObj(str(self)+msg)

    def on(self, board):
        self.board = board
        board.add(self)

        board.addObject("digPin",self)
        board.pinMode(self._pin, self._mode)
        self.log(".mode("+self._mode+")")

    def mode(self, mode):
        self._mode = mode
        self.board.pinMode(pin, 'OUTPUT')
        self.log(".mode("+self._mode+")")


    def write(self, lvl):
        if self._mode == 1:
            self._lvl = _VARIABLES[lvl]
            self.board.digitalWrite(self._pin, self._lvl)
            self.log(".write("+self._lvl+")")

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
            self._event["switch"].call()
            self.log(":switched")
        self._lvl = lvl

        if self._lvl == 1:
            self._event["on"].call()
            self._event["on"].off()
            self._event["off"].on()
            self.log(":on")

        if self._lvl == 0:
            self._event["off"].call()
            self._event["off"].off()
            self._event["on"].on()
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

        self.log(".listen("+period+")")

    def stopListen(self):
        self._listenThread.stop()
        self.log(".stopListen()")

    def periodicWrite(self, period):
        if self._writeThread == None:
            self._writeThread = self.board.newThread()
            self._writeThread.add('digitalSwitch', self._pin)
            self._writeThread.start(period)
        else:
            self._writeThread.stop()
            self._writeThread.start(period)
        self.log(".periodicWrite("+period+")")

    def stopPeriodicWrite(self):
        self._writeThread.stop()
        self.log(".stopPeriodic()")

    def attachEvent(self, event, callback, *args):
        self._event[event].setCallback(callback, *args)
        self.log(".attachEvent("+event+", "+str(callback)+", "+str(*args))

    def detachEvent(self, event):
        self._event[event].reset()
        self.log(".detachEvent("+event+")")


class AnaPin:

    def __init__(self, pin, mode):

        self.board = None

        self._pin = pin
        self._mode = _VARIABLES[mode]

        self.value = 0

        self._listenThread = None
        self._updateEvent = CallBack()

    def on(self, board):
        self.board = board
        board.add(self)

        board.addObject("anaPin",self)
        board.pinMode(self._pin, self._mode)

    def update(self, value):
        self.value = value
        self._updateEvent.call()

    def write(self, value):
        self.value = value
        self.board.analogWrite(self._pin, self.value)

    def read(self):
        key = self.board.getKey()
        self.board.analogRead(self._pin, self.key)
        self.board.addListener(key= key, updateFunction=self.update)

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

    def attachEvent(self, event, callback, *args):
        self._updateEvent.setCallback(callback, *args)

    def detachEvent(self):
        self._updateEvent.reset()
        self.stopListen()


class Button(DigPin):

    def __init__(self,pin):
        DigPin.__init__(self, pin, 'INPUT')


class Led(DigPin):

    def __init__(self, pin):
        DigPin.__init__(self, pin, 'OUTPUT')
    def blink(self, period):
        self.periodicWrite(period)
    def stopBlink(self):
        self.stopPeriodicWrite()
