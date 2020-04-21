from datetime import datetime, timedelta
from typing import Union


class TimeFrame:
    def __init__(self, start, i: Union[datetime, timedelta]):
        self.start = start
        if isinstance(i, datetime):
            self.end = i
            self.duration = self.end - self.start
        elif isinstance(i, timedelta):
            self.duration = i
            self.end = self.start + self.duration

    def within(self, timestamp: datetime):
        return self.start <= timestamp <= self.end
