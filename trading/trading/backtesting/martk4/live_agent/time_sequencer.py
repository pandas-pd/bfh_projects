import numpy as np

hour= 60*60
day = 24*hour
year = (365.2425)*day

class Sequencer():
    """
    Turns hourly,daily and yearly periods into sin functions.
    In this way a neural network can detect periodicle events.
    """
    @staticmethod
    def transform_hour(timestamp_s):
        return timestamp_s * (2 * np.pi / hour)
    @staticmethod
    def transform_day(timestamp_s):
        return np.sin(timestamp_s * (2 * np.pi / day))
    @staticmethod
    def transform_year(timestamp_s):
        return np.sin(timestamp_s * (2 * np.pi / year))
    