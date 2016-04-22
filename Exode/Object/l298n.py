from .pin import *
from .model import obj

class L298N_MOTOR(obj):

    def __init__(self, DC, IN1, IN2, speed=50):

        self._dc =  DigPin(DC,'OUTPUT')
        self._IN1 = DigPin(IN1,'OUTPUT')
        self._IN2 = DigPin(IN2,'OUTPUT')

        self.board = None

        self._speed = speed
        self._direction = 1
        self.isRunning = False

        obj.__init__(self, "L298N_MOTOR(DC={self._dc}, IN1={self._IN1}, IN2={self._IN2} )".format(self=self))

    def setup(self, board):

        self._dc.on(board)
        self._IN1.on(board)
        self._IN2.on(board)

        self._dc.write(self._speed)
        self.board = board
        self.log(".setup()")

    def setSpeed(self, value):
        self._speed = value
        self._speed = min(self._speed,100)
        self._speed = max(self._speed,0)
        self._dc.write((self._speed*255)/100)
        self.log(".speed("+str(value)+")")

    def setDirection(self, value):
        if value == 'forward' or value == 1:
            self._direction = 1
        if value == 'backward' or value == -1:
            self._direction = -1

        self.log(".setDirection("+str(value)+")")
        if self.isRunning:
            self.run()

    def switch(self):
        self.setDirection(-self._direction)
        self.log(".switchDirection()")

    def runForward(self):
        self._IN1.write('HIGH')
        self._IN2.write('LOW')
        self.log(".runForward()")

    def runBackward(self):
        self._IN1.write('LOW')
        self._IN2.write('HIGH')
        self.log(".runBackward()")

    def run(self):
        if self._direction == 1:
            self.runForward()
        else:
            self.runBackward()

        self.isRunning = True

    def stop(self):
        self._IN1.write('LOW')
        self._IN2.write('LOW')

        self.isRunning = False
        self.log(".stop()")
