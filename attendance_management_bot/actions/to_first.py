# !/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import logging
from attendance_management_bot.model.data import make_text
from attendance_management_bot.externals.send_message import push_message

LOGGER = logging.getLogger("attendance_management_bot")


@tornado.gen.coroutine
def to_first(account_id, _, __, ___):
    content = make_text("Please select \"Record\" on the bottom of "
                     "the menu each time when you clock in and clock out.")
    yield push_message(account_id, content)
