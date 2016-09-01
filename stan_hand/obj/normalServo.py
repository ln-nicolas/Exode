from Exode.Object.servo import adaServo
from Exode.Object.obj   import uix_view_update

class normalServo(adaServo):

    def __init__(self, n, minTick, maxTick, min=0, max=1):

        self._minTick = minTick
        self._maxTick = maxTick

        self.min = min
        self.max = max

        self._pos   = .5

        adaServo.__init__(self, n);

    def posToTick(self):
        # TODO : recalculate ! 
        return int(self._minTick + ((self._maxTick-self._minTick)/(self.max-self.min))*self._pos)

    @uix_view_update
    def set(self, pos):
        if pos >= self.min and pos <= self.max:
            self._pos = round(pos, 3)
            self.writeTicks(self.posToTick())

    def move(self, delta):
        self.set(self._pos + delta)

    def pos(self):
        return self._pos

    ### UIX compatibility

    def getUIXView(self):
        return '''[size=15][b]{:.3f}[/b][/size]\n{:d}'''.format(self._pos, ticks)

    def setValue(self, value, name):
        if name == "pos":
            self.set(value)
        adaServo.setValue(self, value, name)

    def getValue(self, name):
        if name == "pos":
            return self._pos
        return adaServo.getValue(self, name)
