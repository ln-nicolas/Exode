#   valueListener.py
#
#   Some values (e.g coming from sensors) must be updated
#   These values are associated to a key. when the board
#   send the value, we launch the updateFunction
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

import _thread

class valueListener:

    def __init__(self, key, updateFunction, requestFunction=None, isInfinite=False):

        self.requestFunction = requestFunction
        self.updateFunction = updateFunction

        # If the value will be updating indefinitely
        self.isInfinite = isInfinite

        self.key = key

    def updateValue(self, value):
        #value :the new value coming from the board
        self.updateFunction(value)

    def requestValue(self, token):
        if( self.requestFunction != None):
            self.requestFunction(token)
