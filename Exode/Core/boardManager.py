#   boardManager.py
#
#   boardManager manage the boards..
#
#   Created by Lenselle Nicolas, March, 2016.
#   lenselle.nicolas@gmail.com

from .exode import *

class BoardManager():

    def __init__(self):
        self.boardList= []

    def portUsed(self):
        return [board.portPath for board in self.boardList]

    def getBoardByPort(self, port):
        for board in self.boardList:
            if board.portPath == port:
                return board
        return None

    def add(self, board):
        board.id= len(self.boardList)
        self.boardList.append(board)

    def searchBoard(self):
        print("not defined yet")

    def autoAddObj(self, obj):
        # If there is only one board
        # edd the obj (pin e.g) on the board
        if len(self.boardList) == 1:
            self.boardList[0].add(obj)

BOARD_MANAGER= BoardManager()


class Board(Exode):

    def __init__(self, port, name=""):

        if not port in BOARD_MANAGER.portUsed():
            Exode.__init__(self, port)
            self.portPath= port
            self.objLst= {}
            self.id = -1

            if name == "":
                self.name= "Board-"+str(id)
            else:
                self.name= name
            BOARD_MANAGER.add(self)
        else:
            self= BOARD_MANAGER.getBoardByPort(port)

    def add(self, obj):
        if(obj.board == None):
            obj.on(self)

    def addObject(self, name, values):
        if not name in self.objLst.keys():
            self.objLst[name]= []
        self.objLst[name].append(values)

