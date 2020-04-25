from datetime import datetime, timedelta
from core.world import world

SECONDS_IN_WEEK = 60*60*24*7

def time_since(timestamp:datetime) -> timedelta:
    return world.current_time - timestamp

def get_start_of_day():
    return world.current_time.replace(hour=0, minute=0, second=0,
                                                    microsecond=0)