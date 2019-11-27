# !/bin/env python
# -*- coding: utf-8 -*-
"""
Handle the user's direct check-out
"""

__all__ = ['deal_sign_out_message', 'deal_sign_out']

import tornado.web
import logging
from attendance_management_bot.model.data import make_text, make_quick_reply
from attendance_management_bot.externals.send_message import push_message
from attendance_management_bot.actions.message import invalid_message, \
    TimeStruct, create_quick_replay_items
from attendance_management_bot.model.processStatusDBHandle \
    import get_status_by_user

LOGGER = logging.getLogger("attendance_management_bot")


def deal_sign_out_message(sign_time, manual_flag=False):
    """
    Generate a message returned to the user when checking out.

    :param sign_time: The user's check-in time is a timestamp.
    :param manual_flag: Boolean value. True is manually enters time.
    :return: message content is a json.
    """
    call_back = "sign_out"
    if manual_flag:
        call_back = "manual_sign_out"

    user_time = TimeStruct(sign_time)

    text = make_text("Register the current time {date} at {hours}:{min} "
                     "{interval} as clock-out time?"
                     .format(date=user_time.date_time.strftime('%m, %d %A'),
                             hours=user_time.hours, min=user_time.min,
                             interval=user_time.interval_en))

    if manual_flag:
        text = make_text("Register the entered {date} at {hours}:{min} "
                         "{interval} as clock-out time?"
                         .format(date=user_time.date_time.strftime('%m, %d %A'),
                                 hours=user_time.hours, min=user_time.min,
                                 interval=user_time.interval_en))

    reply_items = create_quick_replay_items(
        "confirm_out&time=" + user_time.str_current_time_tick, call_back)

    text["quickReply"] = make_quick_reply(reply_items)
    return text


@tornado.gen.coroutine
def deal_sign_out(account_id, current_date, sign_time, manual_flag=False):
    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "out_done":
            return invalid_message()

    if process is None or process != "sign_in_done":
        return invalid_message()

    return deal_sign_out_message(sign_time, manual_flag)


@tornado.gen.coroutine
def direct_sign_out(account_id, current_date, sign_time, _):
    """
    Handle the user's direct check-out.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param sign_time: Time when the user clicks to check-out.
    :param _: no use
    """
    content = yield deal_sign_out(account_id, current_date, sign_time)

    yield push_message(account_id, content)
