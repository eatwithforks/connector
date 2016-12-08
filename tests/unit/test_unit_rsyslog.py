import cloudpassage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', ''))
from lib.rsyslog import Rsyslog

rsyslog = Rsyslog()


class TestUnitRsyslog:
    def test_valid_parse_facility(self):
        assert rsyslog.parse_facility('user,info') is None

    def test_invalid_parse_facility(self):
        accepted = False
        try:
            rsyslog.parse_facility('foo,bar')
        except:
            accepted = True
        assert accepted
