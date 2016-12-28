#   Object.obj.py
#
#   Abstract mother class of all Exode's obj
#
#   Created by Lenselle Nicolas, July, 2016.
#   lenselle.nicolas@gmail.com

from ..Core import BOARD, logCore, logObj, EXD_TIME
from ..Core.callback import CallBack

import time

import io

#
#   Decorator, to update viewers
#
def uix_view_update(func):
    def wrapper(self, *args):
        val = func(self, *args)
        for view in self.views:
            view.update()
        return val
    return wrapper

#
#   AbstractObj, any kind of Exd's obj
#
class AbstractObj:

    def __init__(self, name="noname"):
        self.type  = "obj"
        self.name  = name
        self.views = []
        self.events = {}

        self.color = [0.06, 0.25, 0.49, 1]

    def __repr__(self):
        return self.name

    # log system

    def log(self, msg):
        logObj(str(self)+msg)

    # UIX

    def getUIXView(self):
        # Return a string representation of itself,
        # could be styled with markdown
        return "[b]{}[/b]".format(self.name)

    def getValue(self, name):
        # getter
        return -1

    def setValue(self, value, name):
        # setter
        pass

    @uix_view_update
    def attachView(self, view):
        # Attach a viewer widget to
        # this
        self.views.append(view)

    def setColor(self, color):
        self.color= color

    # Event management

    def setupEvent(self, eventList):
        self.events= {event:CallBack() for event in eventList}

    def attachEvent(self, event, callback):
        self.log(".attachEvent("+event+", "+str(callback))
        if not event in self.events:
            logCore(event+" is not defined on "+str(self))
            self.events[event]= CallBack(function=callback)
        self.events[event].setCallback(callback)

    def event(self, event):
        return self.events[event]

    def detachEvent(self, event):
        if not event in self.events:
            logCore(event+" is not defined on "+str(self))
        self.events[event].reset()
        self.log(".detachEvent("+event+")")

#
# BoardObj, obj on a board
#
class BoardObj(AbstractObj):

    def __init__(self, name, pins=[], autoLoad=True):
        AbstractObj.__init__(self, name)

        self.type = "boardObj"
        self.pins = pins

        if autoLoad:
            BOARD.autoAddObj(self)

    def setup(self, board):
        pass

    def __repr__(self):
        return str(self.board)+"."+self.name

    def on(self, board):
        # Init this obj on board
        if not hasattr(self, 'board'):
            self.board= board
            self.setup(board)
        return self


#
# DataObj, obj generating data
#
class DataObj:

    def __init__(self):
        self.plot= None
        self.output= None

    def setPlot(self, plot):
        self.plot= plot

        if hasattr(self, 'color'):
            self.plot.color= self.color

    def appendData(self, data):
        t= EXD_TIME()
        if not self.plot is None:
            self.plot.points.append((t, data))

        if not self.output is None:
            self.output.write("{:.3f}".format(t))
            if type(data) is tuple or type(data) is list:
                self.output.write("".join([';'+str(value) for value in data])+'\n')
            else:
                self.output.write(';'+str(data)+'\n')

            self.output.flush()

    def clearPlot(self):
        if not self.plot is None:
            self.plot.points = []

    def openStream(self, path):
        self.output= open(path,"w+",encoding="utf-8")

    def closeStream(self):
        self.output.close()
        self.output=None

    def waitData(self):
        l = len(self.plot)
        while l == len(self.plot):
            time.sleep(0.005)
