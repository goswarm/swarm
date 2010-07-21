# $Id: logger.py 1824 2008-09-27 05:24:40Z saunders $
# $URL: svn+ssh://akrill@dev.foodista.com/usr/local/repos/projects/common/src/logger.py $
from logging import handlers
import logging, signal, random, sys

logging.addLevelName(15, 'FACT')

def getLogger(options=None):
    logger = logging.getLogger()
    if type(options) != dict:
        options = { "LOGGING_LEVEL":getattr(options, 'loglevel', 10),
                    "LOGGING_FILE":getattr(options, 'logfile', '/tmp/somelog') }
    if not logger.handlers:
        logger.setLevel(options['LOGGING_LEVEL'])
        ch = handlers.TimedRotatingFileHandler(options['LOGGING_FILE'], 'midnight', 1, 60)
        ch.setLevel(options['LOGGING_LEVEL'])
        formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.addHandler(ch)
    return logger

def increaseLevel(sig, frame):
    logger = getLogger()
    levels = sorted([x for x in logging._levelNames.keys() if type(x) == int])
    current_level_index = levels.index(logger.level)
    if current_level_index+1 == len(levels): return
    new_level_index = current_level_index +1
    logger.setLevel(levels[new_level_index])
    logger.info("settings log level to %i" % logger.level)

def decreaseLevel(sig, frame):
    logger = getLogger()
    levels = sorted([x for x in logging._levelNames.keys() if type(x) == int])
    current_level_index = levels.index(logger.level)
    if current_level_index == 0: return
    new_level_index = current_level_index - 1
    logger.setLevel(levels[new_level_index])
    logger.info("settings log level to %i" % logger.level)

class UniqueLogger:
    def __init__(self, logger, req_id=None):
        self.req_id = req_id or ''.join([random.choice("BCDFGHJKLMNPQRSTVWXYZ2345678") for i in range(8)])
        self.logger = logger
    def log(self, lvl, msg):
        self.logger.log(lvl, "%s\t%s" % (self.req_id, msg))
    def fact(self, name, val):
        self.log(15, "%s\t%s" % (name, val))
    def debug(self, msg, *args, **kwargs):
        self.logger.debug("%s\t%s" % (self.req_id, msg), *args, **kwargs)
    def info(self, msg, *args, **kwargs):
        self.logger.info("%s\t%s" % (self.req_id, msg), *args, **kwargs)
    def warning(self, msg, *args, **kwargs):
        self.logger.warning("%s\t%s" % (self.req_id, msg), *args, **kwargs)
    def error(self, msg, *args, **kwargs):
        self.logger.error("%s\t%s" % (self.req_id, msg), *args, **kwargs)
    def critical(self, msg, *args, **kwargs):
        self.logger.critical("%s\t%s" % (self.req_id, msg), *args, **kwargs)
    def exception(self, msg, *args, **kwargs):
        self.logger.critical("%s\t%s" % (self.req_id, msg), *args, **kwargs)



class LoggerFile:
    def __init__(self, logfunc):
        self.func = logfunc
    def read(self, n=0):
        return ''
    def write(self, d):
        for x in d.split('\n'):
            self.func(x)

if __name__ == "__main__":
    logger = getLogger()
    increaseLevel(1,2)
    decreaseLevel(1,2)
    while 1: pass
