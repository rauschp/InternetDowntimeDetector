from datetime import datetime
import pytz

def create_now_timestamp(timezone_string):
    stamp = datetime.now()
    timezone = pytz.timezone(timezone_string)
    return timezone.localize(stamp)

