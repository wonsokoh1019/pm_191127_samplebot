#!/bin/env python
# -*- coding: utf-8 -*-
"""
system_init_status table's CRUD operation.
save the system Initialize status。
Check also: scripts/initDB.py
"""

__all__ = ['insert_init_status', 'update_init_status',
           'get_init_status', 'delete_init_status']

import logging
from attendance_management_bot.model.postgreSqlPool import PostGreSql
from psycopg2.errors import DuplicateTable


def insert_init_status(action, extra):
    """
    Inserts the initialization status of an item after initialization.

    :param action: Initialized item
    :param extra: Initialized data or status
    :return: no
    """

    insert_sql = "INSERT INTO system_init_status(action, extra) " \
                 "VALUES('%s', '%s') ON CONFLICT(action) " \
                 "DO UPDATE SET extra='%s', update_time=now()" % \
                 (action, extra, extra)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(insert_sql)


def update_init_status(action, extra):
    """
    Update the initialization status of an item after initialization.

    :param action: Initialized item
    :param extra: Initialized data or status
    :return: no
    """

    update_sql = "UPDATE system_init_status SET update_time=now()," \
                 "extra='%s' " \
                 "WHERE action='%s'" % (extra, action)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(update_sql)


def get_init_status(action):
    """
    Get an item initialized data or status.

    :param action: item
    :return: initialized data or status
    """

    select_sql = "SELECT extra " \
                 "FROM system_init_status WHERE action='%s'" % (action,)

    extra = None
    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) == 1:
            extra = rows[0][0]
    return extra


def delete_init_status(action):
    """
    delete an item initialized data or status.

    :param action: item
    :return: no
    """

    select_sql = "DELETE FROM system_init_status WHERE action='%s'" % (action,)

    post_gre = PostGreSql()
    with post_gre as cursor:
        cursor.execute(select_sql)
