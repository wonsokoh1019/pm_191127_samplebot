#!/bin/env python
# -*- coding: utf-8 -*-
"""
Deal confirm check-in
"""

__all__ = ['deal_confirm_in' ,'confirm_in']

import tornado.gen
import asyncio
import time
import uuid
import logging
from datetime import datetime, timedelta
from tornado.web import HTTPError
from attendance_management_bot.common import global_data
from attendance_management_bot.common.local_timezone import local_date_time
from attendance_management_bot.model.data import make_text
from attendance_management_bot.externals.calendar_req import create_schedule
from attendance_management_bot.externals.send_message import push_message
from attendance_management_bot.actions.message import invalid_message, prompt_input
from attendance_management_bot.model.processStatusDBHandle import get_status_by_user, \
    insert_replace_status_by_user_date
from attendance_management_bot.model.calendarDBHandle import set_schedule_by_user, \
    get_schedule_by_user
from attendance_management_bot.common.contacts import get_user_info_by_account

LOGGER = logging.getLogger("attendance_management_bot")


@tornado.gen.coroutine
def deal_confirm_in(account_id, create_time, callback):
    """
    will be linked with the calendar internally, Check in time of registered user.
    Check also: attendance_management_bot/externals/calendar_req.py

    :param account_id: user account id.
    :param create_time: current date by local time.
    :param callback: The message content of the callback,
        include the user's check-in time
    :return: Prompt message of successful check in.
    """
    pos = callback.find("time=")
    str_time = callback[pos+5:]
    user_time = int(str_time)
    my_end_time = user_time + 60
    begin_time = local_date_time(user_time)
    current_date = datetime.strftime(begin_time, '%Y-%m-%d')

    info = get_schedule_by_user(account_id, current_date)
    if info is not None:
        raise HTTPError(500, "Internal data error")

    end_time = begin_time + timedelta(minutes=1)
    cur_time = local_date_time(create_time)
    title = "{account}'s clock-in time on {date}".\
        format(account=get_user_info_by_account(account_id),
               date=datetime.strftime(begin_time, '%A, %B %d'))
    schedule_uid = create_schedule(cur_time, end_time, begin_time,
                                   account_id, title)

    set_schedule_by_user(schedule_uid, account_id, current_date,
                         user_time, my_end_time)

    return make_text("Clock-in time has been registered.")


@tornado.gen.coroutine
def confirm_in(account_id, current_date, create_time, callback):
    """
    This function is triggered when the user clicks confirm check-in.
    Update user's input reminder status, progress.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param create_time: Time the request arrived at the server.
    :param callback: User triggered callback.
    :return: None
    """

    content = yield deal_confirm_in(account_id, create_time, callback)
    yield push_message(account_id, content)

    insert_replace_status_by_user_date(account_id, current_date,
                                       status="in_done",
                                       process="sign_in_done")
