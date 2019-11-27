# !/bin/env python
# -*- coding: utf-8 -*-
"""
common message
"""

__all__ = ['TimeStruct', '__init__', 'create_button_actions',
           'create_quick_replay_items', 'prompt_input', 'number_message',
           'error_message', 'invalid_message', 'reminder_message']

import time
import logging
from attendance_management_bot.model.data import make_message_action, \
    make_postback_action, make_quick_reply_item, make_text
from attendance_management_bot.constant import API_BO, IMAGE_CAROUSEL, RICH_MENUS
from attendance_management_bot.common.local_timezone import local_date_time

LOGGER = logging.getLogger("attendance_management_bot")


class TimeStruct:
    """
    to localize timestamp time
    """

    def __init__(self, sign_time):
        """
        Convert timestamp time to datetime time in a specific time zone.
        And assign it to the corresponding member variable.

        :param sign_time: A user time of timestamp value.
        """

        self.date_time = local_date_time(sign_time)

        self.month = str(self.date_time.month)
        self.date = str(self.date_time.day)
        self.min = str(self.date_time.minute)

        self.interval_en = "AM"

        self.hours = str(self.date_time.hour)
        if self.date_time.hour > 12:
            self.interval_en = "PM"
            self.hours = str(self.date_time.hour - 12)

        self.str_current_time_tick = str(sign_time)
        pos = self.str_current_time_tick.find(".")
        if pos != -1:
            self.str_current_time_tick = self.str_current_time_tick[:pos]


def create_button_actions(direct_sign_callback, manual_sign_callback):
    """
    Create the message body of the button template of two buttons.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500804?lang=en

    :param direct_sign_callback: callback string for the first button.
    :param manual_sign_callback: callback string for the seconds button.
    """
    action1 = make_message_action("Current time", direct_sign_callback)
    action2 = make_message_action("Manually enter", manual_sign_callback)

    return [action1, action2]


def create_quick_replay_items(confirm_callback, previous_callback):
    """
    Building a quick reply floating window for messages.
    Check also: attendance_management_bot/model/data.py

        reference
        - https://developers.worksmobile.com/jp/document/100500807?lang=en

    :param confirm_callback: callback string for the first button.
    :param previous_callback: callback string for the seconds button.
    :return: quick replay items
    """
    action1 = make_postback_action(confirm_callback,
                                   label="yes", display_text="yes",)
    reply_item1 = make_quick_reply_item(action1)

    action2 = make_postback_action(previous_callback,
                                   label="No", display_text="No")
    reply_item2 = make_quick_reply_item(action2)

    return [reply_item1, reply_item2]


def prompt_input():
    """
    Format to remind users to enter time.

    :return: text type message
    """
    return make_text(
        "Please use the military time format "
        "with a total of 4 numerical digits (hhmm) "
        "when entering the time."
        "For example, type 2020 to indicate 8:20 PM. ")


def number_message():
    """
    Non digital message entered.

    :return: text type message
    """
    text1 = make_text("You have created your leave time "
                      "earlier than your leave time. "
                      "Please check your work time and enter again.")

    text2 = prompt_input()
    return [text1, text2]


def error_message():
    """
    Wrong data entered

    :return: text type message
    """
    text1 = make_text("Sorry, but unable to "
                      "comprehend your composed time. "
                      "Please check the time entry method again, "
                      "and enter the time.")

    text2 = prompt_input()
    return [text1, text2]


def invalid_message():
    """
    Invalid input data reminder.

    :return: text type message
    """
    return make_text("I didn't understand the text. "
                     "When you go to work or go home, "
                     "Please select the appropriate "
                     "\"Record\" button for each.")


def reminder_message(process):
    """
    Illegal request reminder.

    :param process: Current user's progress
    :return: text type message
    """
    text = None
    if process == "sign_in_done":
        text = make_text("There is already a clock-in time. "
                         "Please select \"Record\" on the "
                         "bottom of the menu when you clock out.")

    elif process == "sign_out_done":
        text = make_text("There is already a clock-out time."
                         "Please select \"Record\" on the bottom "
                         "of the menu when you clock in.")
    elif process is None:
        text = make_text("Today's clock-in time has not been registered. "
                         "Please select \"Record clock-in\" on the bottom "
                         "of the menu, and enter your clock-in time.")
    return text
