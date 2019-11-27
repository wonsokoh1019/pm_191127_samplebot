#!/bin/env python
# -*- coding: utf-8 -*-
"""
deal time zone
"""

__all__ = ['local_date_time']

from datetime import datetime, timedelta, timezone
from conf.config import TZone
import pytz

def local_date_time(time=None):
    """
    Time to switch UTC time to a specific time zone.

        reference
        - https://docs.python.org/3/library/datetime.html

    :param time: Time to switch time zones
    :return: local time.
    """

    if time is not None:
        date_time = datetime.utcfromtimestamp(time)
        utc_dt = date_time.replace(tzinfo=timezone.utc)
        return utc_dt.astimezone(pytz.timezone(TZone))

    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(pytz.timezone(TZone))

