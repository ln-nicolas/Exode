#   event.py
#
#   CallBack is an object holding
#   a function and its arguments.
#   This object make easier the use of
#   callback functions.
#
#   Created by Lenselle Nicolas, January, 2016.
#   lenselle.nicolas@gmail.com

import threading
import time

class CallBack:

    def __init__(self, function=None, activate=True):
        self._fc = function
        self._on = activate

    def isOn(self):
        return self._on

    def isEmpty(self):
        return self._fc == None

    def on(self):
        self._on = True

    def off(self):
        self._on = False

    def setCallback(self, function):
        self._fc = function
        self._on = True

    def reset(self):
        self._fc = None
        self.on = False

    def call(self, *args):
        if self._fc != None and self.isOn():
            if args != None:
                return self._fc(*args)
            else:
                return self._fc()

class Interrupt:

    def __init__(self, interrupt, callback, activate=True):


        if type(interrupt) is CallBack:
            self.interrupt = interrupt # interrupt should return a boolean
        else:
            self.interrupt = CallBack(interrupt)

        if type(callback) is CallBack:
            self.callback = callback
        else:
            self.callback = CallBack(callback)

        self.toKill = False

        self.isRun = activate
        self.thread = threading.Thread(target=self.watch)
        self.thread.start()


    def on(self):
        self.isRun = True

    def off(self):
        self.isRun = False

    def kill(self):
        self.toKill = True

    def watch(self):
        while 1:
            if self.toKill:
                return 0
            if self.isRun:
                time.sleep(0.0001)
                if self.interrupt.call():
                    self.kill()
                    self.callback.call()
                    return 0

class Timer():

    def __init__(self, callBack, period, loop=False):

        self.period = period
        self.callBack = callBack
        self.loop = loop

        self.timer = threading.Timer(period, self.call)
        self.timer.start()

    def call(self):
        self.callBack.call()
        if self.loop:
            self.timer = threading.Timer(self.period, self.call)
            self.timer.start()

    def cancel(self):
        self.timer.cancel()
        self.loop = False
