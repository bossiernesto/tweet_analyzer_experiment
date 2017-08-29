from abc import ABCMeta
import logging
from utils.pythonUtils import get_current_method_mame


class AbstractLogger(logging.Logger):
    __metaclass__ = ABCMeta

    def __init__(self, name):
        raise NotImplementedError


class DefaultLogger(AbstractLogger):
    """Default logger to build Decorator structure"""

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)
        console = logging.StreamHandler()
        self.addHandler(console)


class HomeLogger(AbstractLogger):
    def __init__(self, name, loggers=[], loginstances=[]):
        self.loggers = []
        for log in loggers:
            self.add_logger(log(name))
        for log in loginstances:
            self.add_logger(log)
        logging.Logger.__init__(self, name, logging.DEBUG)

    def set_level(self, level):
        for logger in self.loggers:
            logger.setLevel(level)

    def add_logger(self, logger):
        self.loggers.append(logger)

    def execLogger(self, func, msg, *args, **kwargs):
        for logger in self.loggers:
            getattr(logger, func)(msg)

    def critical(self, msg, *args, **kwargs):
        self.execLogger(get_current_method_mame(), msg, args, kwargs)

    def error(self, msg, *args, **kwargs):
        self.execLogger(get_current_method_mame(), msg, args, kwargs)

    def warning(self, msg, *args, **kwargs):
        self.execLogger(get_current_method_mame(), msg, args, kwargs)

    def info(self, msg, *args, **kwargs):
        self.execLogger(get_current_method_mame(), msg, args, kwargs)

    def debug(self, msg, *args, **kwargs):
        self.execLogger(get_current_method_mame(), msg, args, kwargs)
