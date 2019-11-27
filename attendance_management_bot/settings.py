# !/bin/bash python3
# -*- coding: UTF-8 -*-
"""
the global setting for attendance_management_bot
"""

from attendance_management_bot.constant import ABSDIR_OF_PARENT

LOG_PATH = ABSDIR_OF_PARENT + "/logs/"
CALENDAR_LOG_FILE = LOG_PATH + "attendance_management_bot.log"
CALENDAR_LOG_ROTATE = "midnight"
CALENDAR_LOG_FMT = '[%(asctime)-15s] [%(levelname)s] ' \
                   '%(filename)s %(funcName)s:%(lineno)d ' \
                   '%(process)d %(request_id).8s %(message)s'
CALENDAR_LOG_LEVEL = "DEBUG"

CALENDAR_PORT = 8080
CALENDAR_PID_FILE = LOG_PATH + "attendance_management_bot.pid"
