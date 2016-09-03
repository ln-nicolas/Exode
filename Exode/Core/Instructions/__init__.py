#   Created by Lenselle Nicolas, August, 2016.
#   lenselle.nicolas@gmail.com


#
#   Instructions holder
#

class InstructionSet():

    def __init__(self, name):
        self.name= name
        self.instructions= []

        self.id_dict = {}

    def setInstruction(self, id, name, types):
        self.instructions.append([id, name, types])
        self.id_dict[id] = name

    def getInstructionName(self, id):
        return self.id_dict[id]


#
#   Types
#

byte = ['byte']
long = ['long']
float = ['float']
signedLong = ['signedLong']
