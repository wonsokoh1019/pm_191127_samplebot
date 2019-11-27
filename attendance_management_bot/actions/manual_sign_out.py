#!/bin/env python
# -*- coding: utf-8 -*-
"""
Handle the user's manual check-out
"""

__all__ = ['manual_sign_out_message', 'manual_sign_out_content', 'manual_sign_out']

import tornado.web
import asyncio
import logging
from attendance_management_bot.model.data import make_text
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.actions.message import invalid_message, prompt_input
from attendance_management_bot.model.processStatusDBHandle \
    import get_status_by_user, set_status_by_user_date

LOGGER = logging.getLogger("attendance_management_bot")


def manual_sign_out_message():
    """
    generate manual check-out message

    :return: message content list
    """
    text1 = make_text("Please manually enter the clock-out time.")

    text2 = prompt_input()

    return [text1, text2]


@tornado.gen.coroutine
def manual_sign_out_content(account_id, current_date):
    """
    Update user status and generate manual check-out message.

    :param account_id: user account id
    :param current_date: current date by local time.
    :return: message content list
    """
    yield asyncio.sleep(1)
    content = get_status_by_user(account_id, current_date)

    if content is None or content[1] is None or content[1] != "sign_in_done":
        return [invalid_message()]

    set_status_by_user_date(account_id, current_date, "wait_out")

    return manual_sign_out_message()


@tornado.gen.coroutine
def manual_sign_out(account_id, current_date, _, __):
    """
    Handle the user's manual check-out.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param _: no use
    :param __: no use
    """
    contents = yield manual_sign_out_content(account_id, current_date)

    yield push_messages(account_id, contents)
