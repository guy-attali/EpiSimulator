from datetime import datetime, timedelta
from typing import Union


class TimeFrame:
    def __init__(self, start: datetime, i: Union[datetime, timedelta]):
        self.start = start
        if isinstance(i, datetime):
            self.end = i
        elif isinstance(i, timedelta):
            self.end = self.start + i

    @property
    def duration(self):
        return self.end - self.start

    def within(self, timestamp: datetime):
        return self.start <= timestamp < self.end

    def __add__(self, delta: timedelta):
        return TimeFrame(self.start+delta, self.end+delta)

    def __sub__(self, delta: timedelta):
        return TimeFrame(self.start-delta, self.end-delta)

    def __iadd__(self, delta: timedelta):
        self.start += delta
        self.end += delta

    def __isub__(self, delta: timedelta):
        self.start -= delta
        self.end -= delta

    def overlap(self, other_timeframe):
        if other_timeframe.start >= self.end:
            return 0.0
        if other_timeframe.end <= self.start:
            return 0.0
        return (min(self.end, other_timeframe.end) - max(self.start, other_timeframe.start))/self.duration
