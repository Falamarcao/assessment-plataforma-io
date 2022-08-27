from django.utils.timezone import make_aware
from datetime import datetime, timedelta


def str_to_datetime(date_time_str, is_end=False):
    if date_time_str:
        if is_end:
            return make_aware(
                datetime.strptime(date_time_str, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
            )
        return make_aware(
            datetime.strptime(date_time_str, '%Y-%m-%d')
        )
