#!/usr/bin/python
# -*- coding: utf-8 -*-
"""validator"""
import datetime
import platform
import dateutil.parser
import pytz
import lib.settings as settings


def validate_time(date):
    """validate time"""
    try:
        dateutil.parser.parse(date)
    except:
        raise ValueError(date + " is not in iso8601 time format")

def validate_time_range(date):
    """validate time range"""
    date_parsed = dateutil.parser.parse(date)
    if date_parsed.tzinfo is None:
        date_parsed = pytz.utc.localize(date_parsed)
    time_range = (datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=settings.historical_limit()))
    if date_parsed < time_range:
        raise ValueError(date + " is out of range")

def batchsize(page):
    """validate batchsize"""
    try:
        int(page)
    except:
        raise ValueError(page + " is not an integer")
    if int(page) > settings.pagination_limit():
        raise ValueError("you have exceeded the batchsize limitation")

def thread(thread_count):
    """validate threads"""
    try:
        int(thread_count)
    except:
        raise ValueError(thread_count + "is not an integer")
    if int(thread_count) > settings.threads():
        raise ValueError("you have exceeded the thread limitation")

def starting(date):
    """validate starting"""
    validate_time(date)
    validate_time_range(date)

def operating_system():
    """determine operating_system"""
    if platform.system() is 'Windows':
        return "windows"
    return "linux"
