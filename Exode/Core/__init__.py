# Log init
import logging
import datetime
import time

current_time = datetime.datetime.now().time()


logging.addLevelName(9, "core")
logging.addLevelName(8, "obj")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('Exode-'+current_time.isoformat()+'.log')
#handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def logObj(msg):
    logger.debug("OBJC - "+msg)
def logCore(msg):
    logger.debug("CORE - "+msg)

logger.info("Here we go !")

from .callback import CallBack, Interrupt, Timer
from .boardManager import *

def delay(ms):
    time.sleep(ms/1000)