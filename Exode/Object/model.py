from ..Core import logObj
from ..Core.boardManager import *

class obj:

    def __init__(self, signature, autoLoad=True):
        self.signature= signature
        if autoLoad:
            BOARD.autoAddObj(self)

    def __repr__(self):
        return str(self.board)+"."+self.signature

    def log(self, msg):
        logObj(str(self)+msg)

    def on(self, board):
        if self.board == None:
            self.setup(board)