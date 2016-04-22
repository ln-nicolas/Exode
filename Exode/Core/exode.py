#   exode.py
#
#   Exode is an object to facilitate the communication
#   between your python script and an Arduino Board.
#
#   A program compiled on the Arduino board is able
#   to decode the instructions sending by Exode
#   throught byte array.
#
#   Exode listen the Serial port and update the
#   incoming values
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

import serial
import time
import _thread

from .variable import _VARIABLES, _FUNCTIONS, _INV_FUNCTIONS, fct
from .listener import valueListener
from . import logCore

class ExodeSpeaker :

    def __init__(self, serialPort, name=""):
        self.port = serialPort

        self.connected = False
        self.mute = False

        if not hasattr(self, 'name'):
            self.name= name


    def speak(self, byteArray):
        # 1st byte : lenght of the instruction
        protocolArray = bytearray([len(byteArray)]) + byteArray
        logCore("speaker-"+self.name+" send "+_INV_FUNCTIONS[int(byteArray[0])]+" : "+str(list(protocolArray)))

        if not self.mute:
            self.port.write(protocolArray)

        return protocolArray

    def pinMode(self, pin, mode, analogic=False):
        mode = _VARIABLES[mode]

        ana=0
        if analogic:
            ana=1

        return self.speak(bytearray([fct('pinMode'), pin, mode, ana]))

    def digitalWrite(self, pin, lvl):
        lvl = _VARIABLES[lvl]
        return self.speak(bytearray([fct('digitalWrite'), pin, lvl]))

    def digitalRead(self, pin, key):
        return self.speak(bytearray([fct('digitalRead'), pin, key]))

    def digitalSwitch(self, pin):
        return self.speak(bytearray([fct('digitalSwitch'), pin]))

    def analogWrite(self, pin, value):
        return self.speak(bytearray([fct('analogWrite'), pin, value]))

    def analogRead(self, pin, key):
        return self.speak(bytearray([fct('analogRead'), pin, key]))

    def addPPM(self, pin, us, key):
        microUs = bytearray(us.to_bytes(4, 'little'))
        return self.speak(bytearray([fct('addPPM'), pin, key])+microUs)

    def removePPM(self, id):
        return self.speak(bytearray([fct('removePPM'), id]))

    def writePPM(self, id, us):
        microUs = bytearray(us.to_bytes(4, 'little'))
        return self.speak(bytearray([fct('writePPM'), id])+microUs)

    def pulse(self, pin, us):
        byteUs = bytearray(us.to_bytes(4,'little'))
        return self.speak(bytearray([fct('pulse'), pin])+byteUs)

    def pulseIn(self, pin, key):
        return self.speak(bytearray([fct('pulseIn'), pin, key]))

    def reset(self):
        return self.speak(bytearray([fct("reset")]))

class ExodeListener:

    def __init__(self, serialPort, name=""):
        self.port = serialPort
        self.listener = {}

        if not hasattr(self, 'name'):
            self.name= name

        self.isRun = True
        _thread.start_new_thread(self.run,())

    def getKey(self, excpt=[]):
        '''
        Values sending by arduino are identified by a key
        then, when the value is listening, the listener
        can call the associate updateFunction
        '''
        id_list = sorted(self.listener.keys())
        for i in range(255):
            if i not in id_list and not i in excpt:
                self.listener[i] = None
                return i

    def addListener(self, updateFunction, requestFunction=None, key=-1, isInfinite=False):
        if key==-1:
            key = self.getKey()
        self.listener[key] = valueListener(key, updateFunction, requestFunction, isInfinite)


    def updateValues(self):

        while self.port.inWaiting() > 0:

            key = int.from_bytes(self.port.read(), byteorder='little')
            value = int.from_bytes(self.port.read(4), byteorder='little', signed=False)
            logCore("listener-"+self.name+" got ["+str(key)+"]:"+str(value))

            if key in self.listener.keys():
                self.listener[key].updateValue(value)
                if not self.listener[key].isInfinite:
                    self.listener.pop(key)

    def run(self):
        while 1:
            if self.isRun:
                self.updateValues()

    def start(self):
        self.isRun = True

    def stop(self):
        self.isRun = False


class Exode(ExodeSpeaker, ExodeListener):

    def __init__(self, port, name=""):
        self.port = serial.Serial(port, 9600)
        ExodeSpeaker.__init__(self, self.port, name)
        ExodeListener.__init__(self, self.port, name)

        #Otherwise, the arduino automatically resets..
        time.sleep(2)

    def newThread(self):
        from .boardThread import boardThread
        return boardThread(self)

    def wait(self,period=False):
        t1= time.time()
        t2= t1
        while (t2-t1)*1000 < period or not period:
            t2= time.time()
