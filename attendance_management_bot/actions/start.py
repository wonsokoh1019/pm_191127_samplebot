# !/bin/env python
# -*- coding: utf-8 -*-
"""
Start using robots
"""

__all__ = ['image_introduce', 'sign', 'start']

import tornado.web
import logging
from attendance_management_bot.model.data import make_text, \
    make_postback_action, make_image_carousel_column, make_image_carousel
from attendance_management_bot.constant import RICH_MENUS, IMAGE_CAROUSEL
from attendance_management_bot.externals.send_message import push_messages
from attendance_management_bot.common.global_data import get_value
from attendance_management_bot.externals.richmenu \
    import set_user_specific_rich_menu

LOGGER = logging.getLogger("attendance_management_bot")


def image_introduce():
    """
    This function constructs three image carousels for self introduction.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500809?lang=en

    :return: image carousels type message content.
    """

    action1 = make_postback_action("a",
                                   display_text="Timeclock can be recorded "
                                                "easily just by clicking buttons",
                                   label="Try it now")

    column1 = make_image_carousel_column(
        image_url=IMAGE_CAROUSEL["resource_url"][0],
        action=action1)

    action2 = make_postback_action("b",
                                   display_text="Entered attendance records "
                                                "are automatically entered "
                                                "in Shared Calendar",
                                   label="Try it now",)
    column2 = make_image_carousel_column(
        image_url=IMAGE_CAROUSEL["resource_url"][1],
        action=action2)

    action3 = make_postback_action("c",
                                   display_text="Attendance records of all "
                                                "employees can be checked at a"
                                                " glance via Attendance "
                                                "Management Shared Calendar",
                                   label="Try it now")

    column3 = make_image_carousel_column(
        image_url=IMAGE_CAROUSEL["resource_url"][2],
        action=action3)

    columns = [column1, column2, column3]
    return make_image_carousel(columns)


@tornado.gen.coroutine
def sign(account_id):
    """
    Set up rich menu for chat with users.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/1005040?lang=en

    :param account_id: user account id
    """
    if account_id is None:
        LOGGER.error("account_id is None.")
        return False
    rich_menu_id = get_value("rich_menu", None)
    if rich_menu_id is None:
        LOGGER.error("get rich_menu_id failed.")
        raise Exception("get rich_menu_id failed.")

    return set_user_specific_rich_menu(rich_menu_id, account_id)


@tornado.gen.coroutine
def start_content(account_id):
    yield sign(account_id)

    content1 = make_text("Hello, I'm an attendance management bot of "
                         "LINE WORKS that helps your timeclock "
                         "management and entry.")
    content2 = image_introduce()

    return [content1, content2]


@tornado.gen.coroutine
def start(account_id, _, __, ___):
    """
    Handle the user start using robots.
    Send the robot's self introduction information,
    and the chat room is bound with rich menu.

    :param account_id: user account id.
    """
    contents = yield start_content(account_id)

    yield push_messages(account_id, contents)
