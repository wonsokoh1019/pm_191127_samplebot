#!/bin/env python
# -*- coding: utf-8 -*-
"""
Deal confirm check-out
"""

__all__ = ['confirm_out']

import tornado.gen
import asyncio
import time
import logging
from datetime import datetime
from tornado.web import HTTPError
from attendance_management_bot.common import global_data
from attendance_management_bot.common.local_timezone import local_date_time
from attendance_management_bot.model.data import make_text
from attendance_management_bot.externals.calendar_req import modify_schedule
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.actions.message import invalid_message, prompt_input, \
    TimeStruct, number_message
from attendance_management_bot.model.processStatusDBHandle import get_status_by_user, \
    set_status_by_user_date
from attendance_management_bot.model.calendarDBHandle import get_schedule_by_user, \
    modify_schedule_by_user
from attendance_management_bot.common.contacts import get_user_info_by_account

LOGGER = logging.getLogger("attendance_management_bot")


def confirm_out_message(user_time, hours, min):
    user_time = TimeStruct(user_time)

    return make_text("Clock-out time has been registered."
                     "The total working hours for {date} "
                     "is {hours} hours and {minutes} minutes."
                     .format(date=user_time.date_time.strftime('%A, %B %d'),
                             hours=hours, minutes=min))


@tornado.gen.coroutine
def deal_confirm_out(account_id, create_time, callback):
    """
    will be linked with the calendar internally, Check out time of registered user.
    Check also: attendance_management_bot/externals/calendar_req.py

    :param account_id: user account id.
    :param create_time: current date by local time.
    :param callback: The message content of the callback,
        include the user's check-out time
    :return: Prompt message of successful check out.
    """
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    user_time = int(str_time)

    end_time = local_date_time(user_time)
    current_date = datetime.strftime(end_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is None:
        raise HTTPError(500, "Internal data error")
    schedule_id = info[0]
    begin_time_st = info[1]

    cur_time = local_date_time(create_time)
    begin_time = local_date_time(begin_time_st)

    title = "{account}'s working hours on {date}".\
        format(account=get_user_info_by_account(account_id),
               date=datetime.strftime(end_time, '%A, %B %d'))
    modify_schedule(schedule_id, cur_time, end_time, begin_time,
                    account_id, title)

    modify_schedule_by_user(schedule_id, user_time)

    if user_time < begin_time_st:
        yield asyncio.sleep(1)
        set_status_by_user_date(account_id, current_date, status="wait_out")
        return number_message(), False

    hours = int((user_time - begin_time_st)/3600)
    min = int(((user_time - begin_time_st) % 3600)/60)

    return [confirm_out_message(user_time, hours, min)], True


@tornado.gen.coroutine
def confirm_out(account_id, current_date, create_time, callback):
    """
    This function is triggered when the user clicks confirm check-out.
    will be linked with the calendar internally.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time the request arrived at the server.
    :param callback: User triggered callback.
    :return: None
    """
    contents, success = yield deal_confirm_out(account_id, create_time, callback)

    yield push_messages(account_id, contents)

    if success:
        set_status_by_user_date(account_id, current_date,
                                status="out_done", process="sign_out_done")
