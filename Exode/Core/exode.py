#   exode.py
#
#   Exode is an interface between python scripts
#   and an Arduino Board.
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
import struct
import _thread

from .variable import _VARIABLES, _FUNCTIONS, _INV_FUNCTIONS, ID
from .listener import valueListener
from . import logCore

from .Instructions.exodeSet import exodeInstructionSet

class ExodeSpeaker :

    def __init__(self, serialPort, name=""):
        self.port = serialPort

        self.connected = False
        self.mute = False

        if not hasattr(self, 'name'):
            self.name= name

        self.addInstructionSet(exodeInstructionSet, 0)


    def sendByteArray(self, byteArray):
        # 1st byte : lenght of the instruction
        protocolArray = bytearray([len(byteArray)]) + byteArray
        #logCore("speaker-"+self.name+" send "+_INV_FUNCTIONS[int(byteArray[0])]+" : "+str(list(protocolArray)))
        logCore("speaker-"+self.name+" send "+" : "+str(list(protocolArray)))

        if not self.mute:
            self.port.write(protocolArray)

        return protocolArray

    # Send a list of typed args on the board
    def send(self, *args):

        byteArray = bytearray([])
        for arg in args:

            type = arg[0]
            value = arg[1]

            if type == 'byte':
                byteArray += bytearray([value])
            elif type == 'long' :
                byteArray += bytearray(value.to_bytes(4, 'little'))
            elif type == 'signedLong' :
                byteArray += bytearray(struct.pack("<i", value))
            elif type == 'float' :
                byteArray += bytearray(struct.pack("<f", value))

        return self.sendByteArray(byteArray)

    # Return a method calling an instruction on the board
    def makeInstructionMethod(self, set_id, instruction_id, instruction_types):
        def method(self, *args, **kwargs):

            typed_arg = [('byte', set_id), ('byte', instruction_id)]

            # args loop
            for i in range(0, len(args)):
                typed_arg.append((instruction_types[i], args[i]))

            # kwargs loop
            inst_id = len(args) - 1
            for key, value in kwargs.items():
                typed_arg.append((instruction_types[inst_id], args[inst_id]))
                inst_id+= 1

            return self.send(*typed_arg)

        return method

    def addInstructionSet(self, set, set_id):

        for inst in set.instructions:
            inst_id    = inst[0]
            name  = inst[1]
            types = inst[2]
            setattr(ExodeSpeaker, name, self.makeInstructionMethod(set_id, inst_id, types))


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


from .boardThread import *
class Exode(ExodeSpeaker, ExodeListener):

    def __init__(self, port, name=""):
        self.port = serial.Serial(port, 9600)

        ExodeSpeaker.__init__(self, self.port, name)
        ExodeListener.__init__(self, self.port, name)

        #Otherwise, the arduino automatically resets..
        time.sleep(2)


    def newThread(self):
        return boardThread(self)

    def wait(self,period=False):
        t1= time.time()
        t2= t1
        while (t2-t1)*1000 < period or not period:
            t2= time.time()
