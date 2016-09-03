#   stepper.py
#
#   Created by Lenselle Nicolas, July, 2016.
#   lenselle.nicolas@gmail.com

from .obj import BoardObj, uix_view_update
from .pin   import DigPin

DRIVER = 1
FULL2WIRE = 2
FULL3WIRE = 3
FULL4WIRE = 4
HALF3WIRE = 6
HALF4WIRE = 8

class Stepper(BoardObj):

    def __init__(self, interface, pins, steps, **kwargs):

        # stepper's pins
        self._pins   = pins

        # stepper param
        self._nbPins= len(pins)
        self._steps = steps        # nb of steps
        self._pos   = 0            # current position
        self._interface = interface
        self._speed = 100       # steps.s^-1
        self._acc   = 50        # steps.s^-2

        name= kwargs.get('name', "stepper({})".format(str(pins)))
        BoardObj.__init__(self, name, pins=pins)

        self.type= "Stepper"

    def setup(self, board):

        board.add(self)

        def setId(value):
            self._id = value

        key = self.board.getKey()
        self.board.addListener(key=key, updateFunction=setId)

        board.addStepper(key, self._interface, *self._pins)
        self.log(".setup()")

    @uix_view_update
    def setRpm(self, rpm):
        self._rpm= rpm
        self._speed = rpm * (self._steps/60)

        self.board.setStepperSpeed(self._id, self._speed)
        self.log(".setRpm({:f})".format(rpm))

    @uix_view_update
    def setSpeed(self, speed):
        self._speed= speed
        self._rpm = self._speed / (self._steps/60)

        self.board.setStepperSpeed(self._id, self._speed)
        self.log(".setSpeed({:f})".format(speed))

    @uix_view_update
    def setAcceleration(self, acc):
        self._acc = acc

        self.board.setStepperAcceleration(self._id, self._acc)
        self.log(".setAcceleration({:f})".format(acc))

    @uix_view_update
    def move(self, step):
        self.board.moveStepper(self._id, step)
        self.log(".move({:d})".format(step))

    def setPos(self, pos):
        step= self._pos - pos
        self.move(step)

    ### UIX compatibility

    def getUIXView(self):
        return "{:d}\n[b]steps \n {:.2f}% [/b][size=15]\n{:d}rpm[/size]".format(self._pos, self._pos/self._steps, self._rpm)

    def setValue(self, value, name):
        if name == "speed":
            self.setSpeed(value)
        if name == "pos":
            self.setPos(value)
        if name == "acc":
            self.setAcceleration(value)
        if name == "rpm":
            self.setRpm(value)

    def getValue(self, name):
        if name == "speed":
            return self._speed
        if name == "pos":
            return self._pos
        if name == "acc":
            return self._acc
        if name == "rpm":
            return self._rpm
