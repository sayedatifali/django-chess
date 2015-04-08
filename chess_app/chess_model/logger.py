import logging

logger = logging.getLogger('root')
FORMAT = "%(levelname)s: [%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)
