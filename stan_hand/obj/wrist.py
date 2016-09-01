
from Exode.Object.obj import *
from .normalServo import normalServo

import numpy as np

servoG_min = 380
servoG_max = 250
servoD_min = 190
servoD_max = 340

class wrist(AbstractObj):

    def __init__(self, servoG, servoD):

        self._sg = normalServo(servoG, servoG_min, servoG_max)
        self._sd = normalServo(servoD, servoD_min, servoD_max)

        self._servoPos = np.matrix([0, 0])
        self._wirstPos = np.matrix([0, 0])

        self._servoToWirst = np.matrix([[.5,.5],[.5,-.5]])
        self._wirstToservo = np.linalg.inv(self._servoToWirst)

        self.updatePos()

        AbstractObj.__init__(self, "wrist")

    # update pos from servo current position
    def updatePos(self):
        self._servoPos.itemset((0,0), self._sg.pos())
        self._servoPos.itemset((0,1), self._sd.pos())
        self._wirstPos = self._servoPos * self._servoToWirst

    def writeServo(self):
        self._sg.set(self._servoPos.item(0,0))
        self._sd.set(self._servoPos.item(0,1))

    @uix_view_update
    def setWristPos(self, pos):
        x= pos[0]; y= pos[1]

        self._wirstPos = np.matrix([x, y])
        self._servoPos = self._wirstPos * self._wirstToservo
        self.writeServo()

    @uix_view_update
    def setServoPos(self, pos):
        x= pos[0]; y= pos[1]

        self._servoPos = np.matrix([x, y])
        self._wirstPos = self._servoPos * self._wirstToservo
        self.updateServo()

    def getWirstPos(self):
        return (self._wirstPos.item(0,0), self._wirstPos.item(0,1))

    def getServoPos(self):
        return (self._servoPos.item(0,0), self._servoPos.item(0,1))

    ### UIX compatibility

    def getUIXView(self):
        pos = self.getWirstPos()
        return '''[size=15][b]({:.3f},{:.3f})[/b][/size]\n'''.format(pos[0], pos[1])

    def setValue(self, value, name):
        if name == "wirstPos":
            self.setWirstPos(value)

    def getValue(self, name):
        if name == "wirstPos":
            return self.getWirstPos()
