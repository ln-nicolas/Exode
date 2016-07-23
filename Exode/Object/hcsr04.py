from .pin import *
from .model import obj, uix_updater

class HCSR04(obj):

    def __init__(self, echo, trig, name=None):

        self._trig = DigPin(trig, 'OUTPUT')
        self._echo = DigPin(echo, 'INPUT')
        self._period = -1

        self.board = None

        self._readThread = None
        self._readKey = -1

        self.duration = -1
        self.cm = -1
        self._time = 0

        if name==None: name= "HCSR04(trig={:d}, echo={:d})".format(trig, echo)

        obj.__init__(self, name, type="HCSR04", pins=[echo, trig])
        self.setupEvent(["update"])

        ##UIX Compatibility
        self.getValue= self.getDistance

    def setup(self, board):
        self.board = board
        self._trig.on(board)
        self._echo.on(board)

        self._readKey = self.board.getKey()
        self._readThread = self.board.newThread()
        self._readThread.add('pulse',self._trig._pin,10)
        self._readThread.add('pulseIn',self._echo._pin, self._readKey)
        self.board.addListener(key=self._readKey, updateFunction=self.update, isInfinite= True)
        self.log(".setup() key="+str(self._readKey))

    @uix_updater
    def update(self, duration):

        #error
        if duration > 26000:
            return

        self.duration = duration
        self.cm = round(duration/58.2, 2)

        self.log(":update duration="+str(duration)+" cm="+str(self.cm))
        self.event("update").call()

        if self._period != -1 and self._plot != None:
            self._time+= self._period
            self._plot.points.append((self._time, self.cm))

    def getDistance(self):
        return self.cm

    def read(self, period=0):
        self._period = period
        self._readThread.start(self._period)
        self.log(".read("+str(period)+")")

    def stopRead(self):
        self._readThread.stop()
        self.log(".stopRead()")

    def getUIXView(self):
        return "[b]{:f}cm[/b]".format(self.cm)
