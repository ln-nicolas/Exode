from .pin import *

class L298N_MOTOR:

    def __init__(self, DC, IN1, IN2, speed=100):

        self._dc = AnaPin(DC,'OUTPUT')
        self._IN1 = DigPin(IN1,'OUTPUT')
        self._IN2 = DigPin(IN2,'OUTPUT')

        self.board = None

        self._speed = speed
        self._direction = 1
        self.isRunning = False

    def on(self, board):

        self._dc.on(board)
        self._IN1.on(board)
        self._IN2.on(board)

        self._dc.write(self._speed)
        self.board = board

    def setSpeed(self, value):
        self._speed = value
        self._dc.write(value)

    def setDirection(self, value):
        if value == 'forward' or value == 1:
            self._direction = 1
        if value == 'backward' or value == -1:
            self._direction = -1

        if self.isRunning:
            self.run()

    def switch(self):
        self.setDirection(-self._direction)

    def runForward(self):
        self._IN1.write('HIGH')
        self._IN2.write('LOW')

    def runBackward(self):
        self._IN1.write('LOW')
        self._IN2.write('HIGH')

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
