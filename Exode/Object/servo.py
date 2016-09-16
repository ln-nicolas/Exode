#   servoPwm.py
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

from .obj   import BoardObj, uix_view_update

_VARIABLES = {
    0:0, 1:1,
    'OUTPUT':1, 'INPUT':0,
    'HIGH':1, 'LOW': 0,
    'ON':1, 'OFF':0,
}

class servoPwm(BoardObj):

    def __init__(self, pin, us=1500, **kwargs):

        self._pwmID= -1
        self._pwmUs= us

        self._pin= pin

        name= kwargs.get('name', "servoPwm({})".format(pin))
        BoardObj.__init__(self, name, pins=[pin])

    def setup(self, board):

        board.add(self)
        board.addObject("servoPwm",self)
        self.init()

    @uix_view_update
    def setID(self, ID):
        self._pwmID = ID
        self.log(":init pwmThread="+str(ID))
        self.write(self._pwmUs)

    def getpwmUS(self):
        #deprecate ?
        return self._pwmUs

    def init(self):
        if self._pwmID == -1:
            key = self.board.getKey()
            self.board.addServo(self._pin, key, self._pwmUs)
            self.board.addListener(key=key, updateFunction=self.setID)

    @uix_view_update
    def write(self, us):
        self._pwmUs = int(us)
        self.log("test")
        if self._pwmID != -1 and self._pwmUs != -1:
            self.board.writeServo(self._pwmID,self._pwmUs)
            self.log(".write("+str(self._pwmUs)+")")

    @uix_view_update
    def stop(self):
        self.board.removeServo(self._pwmID)
        self.log(".stop()")
        self._pwmID = -1

    ### UIX compatibility
    def getUIXView(self):
        if self._pwmID == -1:
            return "[b] Sleep [/b]"
        else:
            return ''' [b]{:d} us[/b]
                       ID : {:d}'''.format(self._pwmUs,
                                           self._pwmID)

    def setValue(self, value, name):
        if name == "us":
            self.write(value)

    def getValue(self, name):
        if name == "us":
            return self._pwmUs


class Servo(servoPwm):

    def __init__(self, pin, angle= 90,
                            minAngle= 0, maxAngle= 180,
                            zeroUs= 1000, angleToUs=5.555,
                            **kwargs):

        self._minAngle = minAngle
        self._maxAngle = maxAngle

        self._angleToUs = angleToUs
        self._zeroUs = zeroUs

        self._angle = angle

        name= kwargs.get('name', "Servo({})".format(pin))
        servoPwm.__init__(self, pin, self.angleToUs(), name=name)
        self.type= "Servo"

    def angleToUs(self):
        return int(self._zeroUs + self._angle * self._angleToUs )

    @uix_view_update
    def secure(self, minAngle= 0, maxAngle= 180):
        self._minAngle = minAngle
        self._maxAngle = maxAngle
        self.log(".secure(min={0}, max={1})".format(minAngle, maxAngle))

    @uix_view_update
    def calibrate(self, zeroUs= None, angleToUs=None):
        if zeroUs != None:
            self._zeroUs = zeroUs
        if angleToUs != None:
            self._angleToUs = angleToUs
        self.log(".calibrate(zero={0}, angleToUs={1}".format(self._zeroUs, self._angleToUs))

    def detach(self):
        self.stop()
        self.log(".stop()")

    def angle(self):
        return self._angle

    @uix_view_update
    def write(self, angle):
        if angle >= self._minAngle and angle <= self._maxAngle:
            self._angle = angle
            servoPwm.write(self, self.angleToUs())
            self.log(".write("+str(angle)+")")


    def writeUs(self, us):
        servoPwm.write(self, us)
        self._angle = int((us-self._zeroUs)/self._angleToUs)
        self.log(".writeUs("+str(us)+")")

    ### UIX compatibility
    def getUIXView(self):
        if self._pwmID == -1:
            return "[b] Sleep [/b]"
        else:
            return ''' [b]{:d}°[/b]\n[size=12]pwm : {:d} us\n {:.2f} us.deg-1[/size]
                       '''.format(self._angle,
                                  self._pwmUs,
                                  self._angleToUs)

    def setValue(self, value, name):
        if name == "us":
            self.writeUs(value)
        if name == "angle":
            self.write(value)
        if name == "zeroUs":
            self.calibrate(zeroUs= value)
        if name == "angleToUs":
            self.calibrate(angleToUs= value)

    def getValue(self, name):
        if name == "us":
            return self._pwmUs
        if name == "angle":
            return self._angle
        if name == "zeroUs":
            return self._zeroUs
        if name == "angleToUs":
            return self._angleToUs



class adaServo(Servo):

    def __init__(self, n, angle=90,
                           minAngle=0, maxAngle=180,
                           zeroTick=100, angleToTick=1,
                           **kwargs):

        self._minAngle = minAngle
        self._maxAngle = maxAngle

        self._angleToTick = angleToTick
        self._zeroTick    = zeroTick

        self._angle       = angle
        self._n           = n
        self._ticks       = self.angleToTick()


        name = kwargs.get('name', "adaServo({})".format(n))
        BoardObj.__init__(self, name, pins=['a4', 'a5'])
        self.type = "adaServo"

    def setup(self, board):
        pass

    def angleToTick(self):
        return int(self._zeroTick + self._angle * self._angleToTick )

    @uix_view_update
    def calibrate(self, zeroTick= None, angleToTick= None):
        if zeroTick != None:
            self._zeroTick = zeroTick
        if angleToTick != None:
            self._angleToTick = angleToTick
        self.log(".calibrate(zero={0}, angleToTick={1}".format(self._zeroTick, self._angleToTick))

    @uix_view_update
    def writeTicks(self, ticks):
        self._angle = int((ticks-self._zeroTick)/self._angleToTick)
        self._ticks = ticks
        self.board.setAdaPWM(self._n, self._ticks)
        self.log(".setAdaPWM({:d}, {:d})".format(self._n, self._ticks))

    @uix_view_update
    def write(self, angle):
        if angle >= self._minAngle and angle <= self._maxAngle:
            self._angle = angle
            self.writeTicks(self.angleToTick())
            self.log(".write({:d})".format(angle))

    ### UIX compatibility

    def getUIXView(self):
        return ''' [b]{:d}°[/b]\n[size=12]ticks: {:d} \n[/size]
                   '''.format(self._angle,
                              self._pwmUs)

    def setValue(self, value, name):
        if name == "ticks":
            self.writeTicks(value)
        if name == "angle":
            self.write(value)
        if name == "zeroTick":
            self.calibrate(zeroTick= value)
        if name == "angleToTick":
            self.calibrate(angleToTick= value)

    def getValue(self, name):
        if name == "ticks":
            return self._ticks
        if name == "angle":
            return self._angle
        if name == "zeroTick":
            return self._zeroTick
        if name == "angleToTick":
            return self._angleToTick
