#!/bin/env python3
# -*- coding: utf-8 -*-
"""
the url to handler route
"""

__all__ = ['getRouter']

import tornado.web
from attendance_management_bot.callbackHandler import CallbackHandler
from attendance_management_bot.constant import FILE_SYSTEM


def getRouter():
    """
    get the app with route info

        reference
        - https://www.tornadoweb.org/en/stable/web.html

    StaticFileHandler is a simple handler that can serve static content
    from a directory.

        reference
        - https://www.tornadoweb.org/en/stable/web.html#tornado.web.StaticFileHandler
    """

    return tornado.web.Application([
        (r"/callback", CallbackHandler),
        (r'/static/([a-zA-Z0-9\&%_\./-~-]*.([p|P][n|N][g|G]))',
            tornado.web.StaticFileHandler, 
            {"path": FILE_SYSTEM["image_dir"]}),
    ])
