#   ArduinoUno.py
#
#   Abstraction of the real board,
#   This object manages the pins, threads,
#   objects .. and detect eventuel errors
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

from ..Core.exode import *

class ArduinoUno(Exode):

    def __init__(self, port):
        Exode.__init__(self,port)
        self.objLst = {}

    def add(self, obj):
        if (obj.board == None):
            obj.on(self)

    def addObject(self, name, values):
        if not name in self.objLst.keys():
            self.objLst[name] = []

        self.objLst[name].append(values)
