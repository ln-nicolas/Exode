#   stepper.py
#
#   Created by Lenselle Nicolas, July, 2016.
#   lenselle.nicolas@gmail.com

from .obj import BoardObj, uix_view_update
from .pin   import DigPin

class Stepper(BoardObj):

    def __init__(self, pins, steps, speed, **kwargs):

        # stepper's pins
        self._pins   = pins
        self._pinsObj= []
        for p in self._pins:
            digPin= DigPin(p, 'OUTPUT',
                               name="stepperPin({})".format(p),
                               autoLoad=False)
            self._pinsObj.append(digPin)

        # stepper param
        self._nbPins= len(pins)
        self._steps = steps        # nb of steps
        self._pos   = 0            # current position

        name= kwargs.get('name', "stepper({})".format(str(pins)))
        BoardObj.__init__(self, name, pins=pins)

        self.type= "Stepper"
        self.setSpeed(speed) # rpm

    def setup(self, board):

        board.add(self)
        for p in self._pinsObj:
            board.add(p)

        # stepCounter is an integer in the board's
        # memory to count the number of iteration
        self.stepCounter = self.board.getShareInt()

        self.log(".setup()")

    @uix_view_update
    def setSpeed(self, speed):
        self._speed= speed
        self.delay = int((60000000/self._steps)/self._speed)

        self.log(".setSpeed({:d})".format(speed))
        self.log(".delay = {:d}us".format(self.delay))

    @uix_view_update
    def step(self, step):

        if isinstance(step, float):
        ## if is float convert % to step
            step= int(step*self._steps)

        self._pos = (self._pos+step) % self._steps

        if self.delay < 5000:
            thread= self.board.newTimer1Thread()
            delay = self.delay
        else:
            thread= self.board.newThread()
            delay = int(self.delay/1000)

        if self._nbPins == 5:
            thread.add("stepper_5", self._pins[0], self._pins[1],
                                    self._pins[2], self._pins[3],
                                    self._pins[4], step,
                                    self.stepCounter.id)
        if self._nbPins == 4:
            thread.add("stepper_4", self._pins[0], self._pins[1],
                                    self._pins[2], self._pins[3],
                                    step, self.stepCounter.id)
        if self._nbPins == 2:
            thread.add("stepper_2", self._pins[0], self._pins[1],
                                    step, self.stepCounter.id)

        self.stepCounter.write(0)
        thread.start(delay)

        self.log(".step({:d})".format(step))

    def setPos(self, pos):
        step= self._pos - pos
        self.step(step)


    ### UIX compatibility

    def getUIXView(self):
        return "{:d}\n[b]steps \n {:.2f}% [/b][size=15]\n{:d}rpm[/size]".format(self._pos, self._pos/self._steps, self._speed)

    def setValue(self, value, name):
        if name == "speed":
            self.setSpeed(value)
        if name == "pos":
            self.setPos(value)

    def getValue(self, name):
        if name == "speed":
            return self._speed
        if name == "pos":
            return self._pos
