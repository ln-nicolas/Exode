from .pin import *
from .model import obj

class HCSR04(obj):

    def __init__(self, echo, trig):

        self._trig = DigPin(trig, 'OUTPUT')
        self._echo = DigPin(echo, 'INPUT')
        self._period = -1

        self.board = None

        self._readThread = None
        self._readKey = -1

        self.duration = -1
        self.cm = -1

        obj.__init__(self, "HCSR04(trig="+str(self._trig)+", echo="+str(self._echo)+")")
        self.setupEvent(["update"])

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


    def update(self, duration):
        self.duration = duration
        self.cm = round(duration/58.2, 2)

        self.log(":update duration="+str(duration)+" cm="+str(cm))
        self.event("update").call()

    def read(self, period=0):
        self._period = period
        self._readThread.start(self._period)
        self.log(".read("+str(period)+")")

    def stopRead(self):
        self._readThread.stop()
        self.log(".stopRead()")
