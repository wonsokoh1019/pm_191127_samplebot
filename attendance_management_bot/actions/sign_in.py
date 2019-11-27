# !/bin/env python
# -*- coding: utf-8 -*-
"""
Handle the user's check-in
"""

__all__ = ['sign_in_message', 'sign_in_content', 'sign_in']

import tornado.web
import logging
from attendance_management_bot.model.data import make_button
from attendance_management_bot.externals.send_message import push_message
from attendance_management_bot.actions.message \
    import reminder_message, create_button_actions
from attendance_management_bot.model.processStatusDBHandle \
    import delete_status_by_user_date, get_status_by_user

LOGGER = logging.getLogger("attendance_management_bot")


def sign_in_message():
    """
    generate check-in message

    :return: button type message content
    """

    actions = create_button_actions("direct_sign_in", "manual_sign_in")

    return make_button("Register current time as clock-in time",
                       actions)


@tornado.gen.coroutine
def sign_in_content(account_id, current_date):
    """
    Update user status and generate check-in message.

    :param account_id: user account id
    :param current_date: current date by local time.
    :retrurn: button type message content
    """

    content = get_status_by_user(account_id, current_date)
    process = None
    if content is not None:
        status = content[0]
        process = content[1]
        if status == "wait_in":
            delete_status_by_user_date(account_id, current_date)

    if process is not None:
        return reminder_message("sign_in_done")

    return sign_in_message()


@tornado.gen.coroutine
def sign_in(account_id, current_date, _, __):
    """
    Handle the user's check-in.

    :param account_id: user account id.
    :param current_date: current date by local time.
    :param _: no use
    :param __: no use
    """

    content = yield sign_in_content(account_id, current_date)

    yield push_message(account_id, content)
