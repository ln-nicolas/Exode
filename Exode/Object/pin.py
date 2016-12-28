#   pin.py
#
#   Created by Lenselle Nicolas, Januar, 2016.
#   lenselle.nicolas@gmail.com

from .obj import BoardObj, DataObj, uix_view_update

_VARIABLES = {
    0:0, 1:1,
    'OUTPUT':1, 'INPUT':0,
    'HIGH':1, 'LOW': 0,
    'ON':1, 'OFF':0,
}

class DigPin(BoardObj, DataObj):

    def __init__(self, pin, mode, analogic=False, **kwargs):

        self._pin = pin
        self._mode = _VARIABLES[mode]
        self._analog = analogic

        self._lvl = 0
        self._period = -1
        self._value = -1

        self._listenThread = None
        self._writeThread  = None

        name= kwargs.get('name', "digPin({})".format(pin))
        BoardObj.__init__(self, name, pins=[pin])
        DataObj.__init__(self)

        self.type= "DigPin"

        self.setupEvent(["switch", "on", "off"])

    def setup(self, board):
        board.add(self)
        board.addObject("digPin", self)
        board.pinMode(self._pin, self._mode, self._analog)
        self.log(".mode("+str(self._mode)+")")

    @uix_view_update
    def mode(self, mode):
        self._mode = _VARIABLES[mode]

        self.board.pinMode(self._pin, mode, analogic=self._analog)

        self.log(".mode("+str(self._mode)+")")

    @uix_view_update
    def write(self, lvl):
        if self._mode == 1:
            self._lvl = _VARIABLES[lvl]
            self.board.digitalWrite(self._pin, self._lvl)
            self.log(".write("+str(self._lvl)+")")

    @uix_view_update
    def analogWrite(self, value):
        self._value = value
        self.board.analogWrite(self._pin, value)
        self.log(".analogWrite("+str(value)+")")

    @uix_view_update
    def switch(self):
        self.board.digitalSwitch(self._pin)
        self._lvl = (self._lvl + 1)%2
        self.log(".swith()")

    def read(self):
        key = self.board.getKey()
        self.board.digitalRead(self._pin, key)
        self.board.addListener(key= key, updateFunction=self.update)
        self.log(".read()")

    @uix_view_update
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

        self.appendData(lvl)

    def listen(self, period = 100):
        self._period= period

        if period==0:
            self.stopListen()
            return

        if self._listenThread is None:
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
        self._period= -1
        if self._listenThread is None:
            return
        self._listenThread.stop()
        self.log(".stopListen()")

    @uix_view_update
    def periodicSwitch(self, period):
        self._period= period

        if period == 0:
            self.stopPeriodicSwitch()
            return

        if self._writeThread == None:
            self._writeThread = self.board.newThread()
            self._writeThread.add('digitalSwitch', self._pin)
            self._writeThread.start(period)
        else:
            self._writeThread.stop()
            self._writeThread.start(period)
        self.log(".periodicSwitch("+str(period)+")")

    @uix_view_update
    def stopPeriodicSwitch(self):
        self._period= -1
        if self._writeThread is None:
            return
        self._writeThread.stop()
        self._period= -1
        self.log(".stopPeriodic()")

    ### UIX compatibility

    def getUIXView(self):
        if self._period != -1:
            if self._mode == 1:
                return "[b] periodic switch [/b]\n {:d} ms".format(int(self._period))
            else:
                return "[b][size=20]{:d}[/size] \n periodic listen [/b]\n {:d}ms".format(self._lvl, self._period)
        else:
            if self._lvl == 1: return "[size=25][b]HIGH[/b][/size]"
            else: return "[size=25][b]LOW[/b][/size]"

    def setValue(self, value, name):
        if name == "period":
            self.periodicSwitch(value)
        if name == "lvl":
            if self._analog:
                self.analogWrite(value)
            else:
                self.write(value)

    def getValue(self, name):
        if name=="period": return self._period
        else:
            if self._analog:
                return self._value
            else:
                return self._lvl

class AnaPin(BoardObj, DataObj):

    def __init__(self, pin, mode, name=None, **kwargs):

        self._pin = pin
        self._mode = _VARIABLES[mode]

        self.value = 0
        self._plot = None

        self._listenThread = None
        self._period= -1

        self._time= 0

        name= kwargs.get('name', "anaPin({})".format(pin))
        BoardObj.__init__(self, name, pins=[pin])
        DataObj.__init__(self)

        self.setupEvent(["update"])

    def setup(self, board):
        self.board = board
        board.add(self)

        board.addObject("anaPin",self)
        board.pinMode(self._pin, self._mode, analogic=True)
        self.log(".AnaPinMode("+str(self._mode)+")")

    @uix_view_update
    def update(self, value):
        self.value = value

        self.appendData(value)

        #self.log(":read "+str(value))
        self.event("update").call()

    def mode(self, mode):
        self._mode = _VARIABLES[mode]
        self.board.pinMode(self._pin, self._mode, analogic=True)
        self.log(".mode("+str(mode)+")")

    def read(self):
        key = self.board.getKey()
        self.board.analogRead(self._pin, key)
        self.board.addListener(key= key, updateFunction=self.update)
        self.log(".read()")

    @uix_view_update
    def listen(self, period= 100):
        self._period = period

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

    @uix_view_update
    def stopListen(self):
        self._listenThread.stop()
        self.log(".stopListen()")
        self._period = -1

    ### UIX compatibility

    def setValue(self, value, name):
        if name == "period":
            self.listen(value)

        ## to complete

    def getValue(self, name):
        return self.value

    def getUIXView(self):
        if self._period == -1:
            return "value \n[b]{:d}[/b]".format(self.value)
        else:
            return "value \n[b]{:d}[/b]\n listen {:d} ms".format(self.value, self._period)

class Button(DigPin):

    def __init__(self, pin, **kwargs):
        DigPin.__init__(self, pin, 'INPUT', **kwargs)


class Led(DigPin):

    def __init__(self, pin, **kwargs):
        DigPin.__init__(self, pin, 'OUTPUT', **kwargs)
        self.type= "Led"

    def blink(self, period):
        self.periodicSwitch(period)
    def stopBlink(self):
        self.stopPeriodicSwitch()
