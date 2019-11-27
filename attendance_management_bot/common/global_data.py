#!/bin/env python
# -*- coding: utf-8 -*-
"""
This is a global variable cache.
"""

__all__ = ['set_value', 'get_value']

_global_dict = {}


def _init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """
    Sets a value into the global variable cache.

    :param key: key
    :param value: value
    :return: no
    """
    _global_dict[key] = value


def get_value(key, def_value=None):
    """
    Gets a value from the global variable cache.

    :param key: key
    :param def_value: default value
    :return: value, If the key does not exist, the default value.
    """
    try:
        return _global_dict[key]
    except KeyError:
        return def_value
