#!/bin/env python
# -*- coding: utf-8 -*-
"""
Process requests of users
"""

__all__ = ['CallbackHandler', 'post']

import json
import logging
import tornado.web
from attendance_management_bot.check_and_handle_actions import CheckAndHandleActions

LOGGER = logging.getLogger("attendance_management_bot")


class CallbackHandler(tornado.web.RequestHandler):
    """
    Process business requests of users.

    tornado.web.RequestHandler base class for HTTP request handlers.

        reference
        - https://www.tornadoweb.org/en/stable/web.html
    """

    @tornado.gen.coroutine
    def post(self):
        """
        Implement the handle to corresponding HTTP method.
        Check also: attendance_management_bot/router.py
        """

        LOGGER.info("request para path:%s", self.request.uri)
        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            LOGGER.exception('Failed parse json:%s' % self.request.body)
            raise tornado.web.HTTPError(403, "boy is not json.")

        LOGGER.info("request para body:%s", self.request.body)
        checker = CheckAndHandleActions()
        yield checker.execute(body)

        self.finish()
