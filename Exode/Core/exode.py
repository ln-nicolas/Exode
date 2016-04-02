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

from .variable import _VARIABLES, _FUNCTIONS, _INV_FUNCTIONS, DEBUG, fct
from .listener import valueListener

class ExodeSpeaker :

    def __init__(self, serialPort):
        self.port = serialPort

        self.connected = False
        self.mute = False

        #if self.port != None:
        #    self.waitBoard()


    def waitBoard(self):
        while self.port.inWaiting() <= 0:
            self.connected = False
        answer=""
        while self.port.inWaiting()>0:
            answer += self.port.read().decode("utf-8")
        if answer == "run": # The board send the key word 'run' during the initialisation
            self.connected = True
        if (DEBUG):
            print(answer)

    def debugSpeak(self, byteArray, instruction):
        if (DEBUG):
            print("(log) "+instruction+" : ",end="")
            print(list(byteArray))

    def speak(self, byteArray):
        # 1st byte : lenght of the instruction
        protocolArray = bytearray([len(byteArray)]) + byteArray
        self.debugSpeak(protocolArray, _INV_FUNCTIONS[int(byteArray[0])])

        if not self.mute:
            self.port.write(protocolArray)

        return protocolArray

    def pinMode(self, pin, mode):
        mode = _VARIABLES[mode]
        return self.speak(bytearray([fct('pinMode'), pin, mode]))

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

class ExodeListener:

    def __init__(self, serialPort):
        self.port = serialPort
        self.listener = {}

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

    def debug(self, key, value):
        if DEBUG:
            print("["+str(key)+"] : "+str(value))

    def updateValues(self):

        while self.port.inWaiting() > 0:

            key = int.from_bytes(self.port.read(), byteorder='little')
            value = int.from_bytes(self.port.read(4), byteorder='little', signed=False)
            self.debug(key, value)

            if key in self.listener.keys():
                self.listener[key].updateValue(value)
                if not self.listener[key].isInfinite:
                    self.listener.pop(key)

    def run(self):
        while 1:
            if self.isRun:
                time.sleep(0.00001)
                self.updateValues()

    def start(self):
        self.isRun = True

    def stop(self):
        self.isRun = False


class Exode(ExodeSpeaker, ExodeListener):

    def __init__(self, port):
        self.port = serial.Serial(port, 9600)
        ExodeSpeaker.__init__(self, self.port)
        ExodeListener.__init__(self, self.port)

    def newThread(self):
        from .boardThread import boardThread
        return boardThread(self)
