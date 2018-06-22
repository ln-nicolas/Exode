from Exode import *

board = Board(BOARD.search()[0])

board.pinMode(13, 1)

thread = board.newThread()
thread.add("digitalWrite", 1)
thread.add("sleep", 1000)
thread.add("digitalWrite", 1)
thread.add("sleep", 1000)
thread.add("digitalWrite", 1)
thread.add("sleep", 1000)
thread.add("digitalWrite", 1)
thread.add("sleep", 1000)

thread.start(1000)
