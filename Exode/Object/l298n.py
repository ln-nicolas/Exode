#   l298n.py
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

from .pin   import *
from .obj   import BoardObj, uix_view_update

class L298N_MOTOR(BoardObj):

    def __init__(self, DC, IN1, IN2, speed=50, **kwargs):

        self._dc =  DigPin(DC,'OUTPUT')
        self._IN1 = DigPin(IN1,'OUTPUT')
        self._IN2 = DigPin(IN2,'OUTPUT')

        self.board = None

        self._speed = speed
        self._direction = 1
        self.isRunning = False

        name= kwargs.get('name',"L298N_MOTOR(DC={self._dc}, IN1={self._IN1}, IN2={self._IN2} )".format(self=self))
        BoardObj.__init__(self, name, pins=[DC, IN1, IN2])

        self.type= "L298N"

    def setup(self, board):

        board.add(self)
        board.add(self._dc)
        board.add(self._IN1)
        board.add(self._IN2)

        self._dc.write(self._speed)
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

    ### UIX compatibility
    def getUIXView(self):
        di= "forward"
        if self._direction == -1: di= "backward"
        if not self.isRunning: di= "stop"
        return '''{:s}
                  [b]{:f} %[/b]'''.format(di, self._speed)

    def setValue(self, value, name):
        if name == "isRunning":
            if value: self.run()
            else: self.stop()

        if name == "speed":
            self.setSpeed(value)

        if name == "direction":
            self.setDirection(value)

    def getValue(self, name):
        if name == "isRunning":
            return self.isRunning

        if name == "speed":
            return self._speed

        if name == "direction":
            return self._direction
