import cloudpassage
import sys
import os
import pytest
import datetime
import time
import platform
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', ''))
import lib.validate as validate


class TestUnitValidate:
    def test_validate_valid_time(self):
        accepted = True
        try:
            validate.validate_time("2016-08-20")
        except ValueError as e:
            accepted = False
        assert accepted

    def test_validate_invalid_time(self):
        accepted = False
        try:
            validate.validate_time("foobar")
        except ValueError as e:
            accepted = True
        assert accepted

    def test_validate_valid_time_range(self):
        accepted = True
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            validate.validate_time_range(today)
        except ValueError as e:
            accepted = False
        assert accepted

    def test_validate_invalid_time_range(self):
        accepted = False
        today = datetime.datetime.now()
        date = (today - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
        try:
            validate.validate_time_range(date)
        except ValueError as e:
            accepted = True
        assert accepted

    def test_validate_valid_batchsize(self):
        accepted = True
        size = 10
        try:
            validate.batchsize(size)
        except ValueError as e:
            accepted = False
        assert accepted

    def test_validate_invalid_batchsize(self):
        accepted = False
        size = 100
        try:
            validate.batchsize(size)
        except ValueError as e:
            accepted = True
        assert accepted

    def test_validate_valid_thread(self):
        accepted = True
        thread = 1
        try:
            validate.thread(thread)
        except ValueError as e:
            accepted = False
        assert accepted

    def test_validate_invalid_str_thread(self):
        accepted = False
        thread = 'foobar'
        try:
            validate.thread(thread)
        except ValueError as e:
            accepted = True
        assert accepted

    def test_validate_invalid_count_thread(self):
        accepted = False
        thread = 10
        try:
            validate.thread(thread)
        except ValueError as e:
            accepted = True
        assert accepted

    def test_validate_operating_system(self):
        current_platform = platform.system()
        if current_platform is not 'Windows':
            current_platform = 'linux'
        actual = validate.operating_system()
        assert current_platform is actual
