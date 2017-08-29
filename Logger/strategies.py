from Logger.abstractLogger import HomeLogger
from Logger.teepyLogger import TweepyLogger


class NormalLogStrategy(HomeLogger):
    def __init__(self, name):
        from Logger.coloredLogger import ColoredLogger

        HomeLogger.__init__(self, name, loggers=[ColoredLogger, TweepyLogger])
        self.set_level('INFO')


class DebugLogStartegy(NormalLogStrategy):
    def __init__(self, name):
        NormalLogStrategy.__init__(self, name)
        self.set_level('DEBUG')
