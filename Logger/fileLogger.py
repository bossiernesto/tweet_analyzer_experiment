from Logger.abstractLogger import AbstractLogger
import logging

FORMAT = "[%(name)-s][%(levelname)-s]  %(message)s (%(filename)s:%(lineno)d) at %(asctime)-15s"


class DopplerLogger(AbstractLogger):
    def __init__(self, name, fileName=None):
        logging.Logger.__init__(self, name, logging.DEBUG)
        self.fileName = fileName if fileName else 'DopplerAPI.log'

        console = logging.FileHandler(self.fileName)
        console.setFormatter(logging.Formatter(FORMAT, "%Y-%m-%d %H:%M:%S"))

        self.addHandler(console)
        logging.setLoggerClass(DopplerLogger)
