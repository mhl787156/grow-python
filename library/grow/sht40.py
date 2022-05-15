import board
import adafruit_sht4x
import time
from copy import deepcopy
import schedule

class SHT40(object):

    def __init__(self):

        self.sht = adafruit_sht4x.SHT4x(board.I2C())
        self.sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
        
        self._reading = (0, 0) # (temperature, humidity)

        self._history = []
        self._history_length = 200

        self._time_start = time.time()

        schedule.every(10).seconds.do(lambda x: self.reading)

    @property
    def history(self):
        return self._history

    @property
    def _time_elapsed(self):
        return time.time() - self._time_last_reading

    @property
    def reading(self):
        self._reading = self.sht.measurements
        self.history.append(deepcopy(self._reading))
        self.history = self._history[:self._history_length]
        return self._reading