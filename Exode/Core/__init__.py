# Log init
import logging
import datetime
import time

from io import StringIO

current_time = datetime.datetime.now().time()

logging.addLevelName(9, "core")
logging.addLevelName(8, "obj")

logger = logging.getLogger(__name__)
logger.setLevel(10)

LOG_PATH = 'ExodeLog.log'

formatter = logging.Formatter('%(asctime)s|%(name)s|%(message)s')
handler = logging.FileHandler(LOG_PATH)
handler.setFormatter(formatter)
logger.addHandler(handler)

def logObj(msg):
    logger.debug("OBJC|"+msg)

def logCore(msg):
    logger.debug("CORE|"+msg)

def logPy(msg):
    logger.debug("PYTH|"+msg)

logger.info("INFO|Here we go!")

from .callback import CallBack, Interrupt, Timer
from .boardManager import *

START_TIME = time.time()
def EXD_TIME():
    return round(time.time() - START_TIME, 3)
