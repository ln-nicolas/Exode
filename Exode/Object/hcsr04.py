#   hcsr04.py
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

from .pin import *
from .obj import BoardObj, uix_view_update

class HCSR04(BoardObj, DataObj):

    def __init__(self, echo, trig, **kwargs):

        self._trig = DigPin(trig, 'OUTPUT')
        self._echo = DigPin(echo, 'INPUT')
        self._period = -1

        self._readThread = None
        self._readKey = -1

        self.__duration = -1
        self._cm = -1

        name= kwargs.get('name', "HCSR04(trig={:d}, echo={:d})".format(trig, echo))
        BoardObj.__init__(self, name, pins=[echo, trig])
        DataObj.__init__(self)
        self.type= 'HCSR04'

        self.setupEvent(["update"])

    def setup(self, board):
        board.add(self)

        board.add(self._trig)
        board.add(self._echo)

        self._readKey = self.board.getKey()
        self._readThread = self.board.newThread()
        self._readThread.add('pulse',self._trig._pin,10)
        self._readThread.add('pulseIn',self._echo._pin, self._readKey)
        self.board.addListener(key=self._readKey, updateFunction=self.update, isInfinite= True)
        self.log(".setup() key="+str(self._readKey))

    def cm(self):
        return self._cm

    def duration(self):
        return self._duration

    @uix_view_update
    def update(self, duration):

        #error
        if duration > 26000:
            return

        self._duration = duration
        self._cm = round(duration/58.2, 2)

        self.log(":update duration="+str(duration)+" cm="+str(self._cm))
        self.event("update").call()

        self.appendData(self._cm)

    @uix_view_update
    def read(self, period=0):
        self._period = period
        self._readThread.start(self._period)
        self.log(".read("+str(period)+")")

    def stopRead(self):
        self._readThread.stop()
        self.log(".stopRead()")

    ### UIX compatibility
    def getUIXView(self):
        return '''[b]{:f}cm[/b]
                  {:d} ms'''.format(self._cm, self._period)

    def setValue(self, value, name):
        if name == "period":
            self.read(period)

    def getValue(self, name):
        if name == "cm":
            return self._cm
        if name == "period":
            return self._period
