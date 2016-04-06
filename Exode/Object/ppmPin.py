from .model import obj

_VARIABLES = {
    0:0,
    1:1,
    'OUTPUT':1,
    'INPUT':0,
    'HIGHT':1,
    'LOW': 0,
    'ON':1,
    'OFF':0,
}

class ppmPin(obj):

    def __init__(self, pin, us=1500):

        self._ppmThread= -1
        self._ppmUs= us

        self._pin= pin

        self.board= None

        obj.__init__(self, "ppmPin("+str(self._pin)+")")

    def setup(self, board):
        self.board = board
        board.add(self)
        board.addObject("ppmPin",self)
        self.init()

    def setPPMThread(self, thread):
        self._ppmThread = thread
        self.log(":init ppmThread="+str(thread))
        # When we receive the thread id we can write the pulsation
        self.write(self._ppmUs)

    def init(self):
        if self._ppmThread == -1:
            key = self.board.getKey()
            self.board.addPPM(self._pin, self._ppmUs, key)
            self.board.addListener(key=key, updateFunction=self.setPPMThread)

    def write(self, us):
        self._ppmUs = us
        if self._ppmThread != -1 and self._ppmUs != -1:
            self.board.writePPM(self._ppmThread,self._ppmUs)
            self.log(".write("+str(self._ppmUs)+")")

    def stop(self):
        self.board.removePPM(self._ppmThread)
        self.log(".stop()")
        self._ppmThread = -1


class Servo(ppmPin, obj):

    def __init__(self, pin, angle= 90, minAngle= 0, maxAngle= 180, zeroUs= 1000, angleToUs=5.555):

        self._minAngle = minAngle
        self._maxAngle = maxAngle

        self._angleToUs = angleToUs
        self._zeroUs = zeroUs

        self._angle = angle

        ppmPin.__init__(self, pin, self.angleToUs())
        obj.__init__("servo("+str(pin)+")", autoLoad=False)

    def angleToUs(self):
        return int(self._zeroUs + self._angle * self._angleToUs )

    def secure(self, minAngle= 0, maxAngle= 180):
        self._minAngle = minAngle
        self._maxAngle = maxAngle
        self.log(".secure(min={0}, max={1})".format(minAngle, maxAngle))

    def calibrate(self, zeroUs= 1000, angleToUs=5.555):
        self._zeroUs = zeroUs
        self._angleToUs = angleToUs
        self.log(".calibrate(zero={0}, angleToUs={1}".format(zeroUs, angleToUs))

    def detach(self):
        self.stop()
        self.log(".stop()")

    def write(self, angle):
        if angle >= self._minAngle and angle <= self._maxAngle:
            self._angle = angle
            ppmPin.write(self, self.angleToUs())
            self.log(".write("+str(angle)+")")

    def writeUs(self, us):
        ppmPin.write(self, us)
        self.log(".writeUs("+str(us)+")")