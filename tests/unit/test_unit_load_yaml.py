import cloudpassage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', ''))
import lib.loadyaml as loadyaml


class TestUnitLoadYaml:
    def test_load_rsyslog(self):
        assert loadyaml.load_rsyslog() is not None

    def test_load_portal(self):
        assert loadyaml.load_portal() is not None

    def test_load_cef(self):
        assert loadyaml.load_cef() is not None

    def test_load_leef(self):
        assert loadyaml.load_leef() is not None
