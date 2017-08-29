import logging

from Logger.coloredFormater import *
from Logger.abstractLogger import AbstractLogger

FORMAT = "[$BOLD%(name)-s$RESET][%(levelname)-s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d) at %(asctime)-15s"


# Custom logger class with multiple destinations
class ColoredLogger(AbstractLogger):
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)
        logging.setLoggerClass(ColoredLogger)
