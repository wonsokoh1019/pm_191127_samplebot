#!/bin/bash python3
# -*- coding: UTF-8 -*-
"""
constants.py Defining the constant used for a project.

"""
import os
from conf.config import *
# ---------------------------------------------------------------------
# Constants and global variables
# ---------------------------------------------------------------------

# ROOT PATH
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)

HEROKU_SERVER_ID = SERVER_ID
PRIVATE_KEY_PATH = ABSDIR_OF_PARENT + "/key/" + SECRET_KEY_NAME

# DOMAIN
STORAGE_DOMAIN = "storage.worksmobile.com"
AUTH_DOMAIN = "auth.worksmobile.com"
DEVELOP_API_DOMAIN = "apis.worksmobile.com"

# RICH_MENUS
RICH_MENUS = {
                "name": "attendance_management_bot_rich_menu_en",
                "path": ABSDIR_OF_PARENT + "/image/en/Rich_Menu.png"
             }

# IMAGE CAROUSEL
IMAGE_CAROUSEL = {
                    "resource_url":
                    [
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_01.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_02.png",
                        LOCAL_ADDRESS + "static/en/IMG_Carousel_03.png"
                    ]
                }

# API ADDRESS
API_BO = {
            "headers": {
                "content-type": "application/json",
                "charset": "UTF-8"
            },
            "upload_url": "http://" + STORAGE_DOMAIN
                          + "/openapi/message/upload.api",
            "push_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                        + API_ID + "/message/v1/bot/_BOT_NO_/message/push",
            "rich_menu_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                             + API_ID + "/message/v1/bot/_BOT_NO_/richmenu",

            "calendar":
            {
                "name": "calendar bot",
                "create_calendar_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/"
                                       "calendarList",
                "create_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/calendars/"
                                       "_CALENDAR_ID_/events",
                "modify_schedule_url": "https://" + DEVELOP_API_DOMAIN + "/r/"
                                       + API_ID +
                                       "/calendar/v1/_ACCOUNT_ID_/calendars/"
                                       "_CALENDAR_ID_/events/_CALENDAR_UUID_",
            },

            "TZone":
            {
                "contacts_url": "https://" + DEVELOP_API_DOMAIN + "/"
                                    + API_ID
                                    + "/contact/getDomainContact/v1"
            },
            "auth_url": "https://" + AUTH_DOMAIN + "/b/" + API_ID
                        + "/server/token?grant_type=urn%3Aietf%3Aparams%3Aoauth"
                          "%3Agrant-type%3Ajwt-bearer&assertion="
        }

# OPEN API
OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": SERVER_CONSUMER_KEY
    }

# DB CONFIG
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "sslmode": "prefer"
}

# FILE SYSTEM
FILE_SYSTEM = {
    "image_dir": ABSDIR_OF_PARENT+"/image",
}
