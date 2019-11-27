# !/bin/env python
# -*- coding: utf-8 -*-
"""
Handle the user's check-out
"""

__all__ = ['sign_out_message', 'sign_out_content', 'sign_out']

import tornado.web
import logging
from attendance_management_bot.model.data import make_button
from attendance_management_bot.externals.send_message import push_message
from attendance_management_bot.actions.message \
    import reminder_message, create_button_actions
from attendance_management_bot.model.processStatusDBHandle \
    import set_status_by_user_date, get_status_by_user

LOGGER = logging.getLogger("attendance_management_bot")


def sign_out_message():
    """
    generate check-out message

    :return: button type message content
    """
    actions = create_button_actions("direct_sign_out", "manual_sign_out")
    return make_button("Please select the clock-out time entry method.",
                       actions)


@tornado.gen.coroutine
def sign_out_content(account_id, current_date):
    """
    Update user status and generate check-out message.

    :param account_id: user account id
    :param current_date: current date by local time.
    :return: button type message content
    """

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_out":
            set_status_by_user_date(account_id, current_date, status="in_done")

    if process is None or process != "sign_in_done":
        return reminder_message(None)

    return sign_out_message()


@tornado.gen.coroutine
def sign_out(account_id, current_date, _, __):
    """
    Handle the user's check-out.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param _: no use
    :param __: no use
    """

    content = yield sign_out_content(account_id, current_date)

    yield push_message(account_id, content)
