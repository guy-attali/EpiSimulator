from datetime import datetime, timedelta
from core.world import world

def time_since(timestamp:datetime) -> timedelta:
    return world.current_tf.start - timestamp

def get_start_of_day():
    start_of_today = world.current_tf.start.replace(hour=0, minute=0, second=0,
                                                    microsecond=0)