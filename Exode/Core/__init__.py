# Log init
import logging
import datetime
current_time = datetime.datetime.now().time()


logging.addLevelName(9, "core")
logging.addLevelName(8, "obj")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('Exode-'+current_time.isoformat()+'.log')
handler.setLevel(8)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def logObj(msg):
    logger.log(8, msg)

def logCore(msg):
    logger.log(9, msg)

logger.info("Here we go !")

from .callback import CallBack, Interrupt, Timer
from .boardManager import Board

