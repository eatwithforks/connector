import cloudpassage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'lib'))
from cef import Cef


class TestUnitCef:
    def create_cef_object(self):
        cef = Cef({'cefsyslog': None})
        return cef

    def event_stub(self):
        stub = [
            {
                "id": "e750d982688411e6b7b32f750f990d28",
                "type": "fim_target_integrity_changed",
                "name": "File Integrity change detected",
                "message": "A change was detected in file integrity target" \
                           "/opt/cloudpassage/*/* on Linux server" \
                           "Jlee-Chef-Node1 (54.183.177.195) (source: Scan)",
                "server_id": "5b1d73b63e3711e68ead7f4b70b6c2b8",
                "created_at": "2016-08-22T16:24:30.726Z",
                "critical": True,
                "server_platform": "Linux",
                "server_hostname": "ip-10-2-20-76",
                "server_group_name": "old_smoke",
                "server_ip_address": "54.183.177.195",
                "server_reported_fqdn": "localhost",
                "server_label": "Jlee-Chef-Node1",
                "server_primary_ip_address": "10.2.20.76",
                "scan_id": "e730037e688411e6b7b32f750f990d28",
                "finding_id": "e748d9c6688411e6b7b32f750f990d28",
                "policy_name": "FIM halo"
            }
        ]
        return stub

    def test_cef_constants(self):
        cef = self.create_cef_object()
        cef_constants = cef.cef_constants(self.event_stub()[0])
        expected = "CEF:0|CloudPassage|CPHalo|1.0|" \
                   "130|File Integrity change detected|9|"
        assert expected == cef_constants

    def test_cef_outliers(self):
        cef = self.create_cef_object()
        mapping = {}
        cef.build_cef_outliers(mapping, self.event_stub()[0])
        assert {"deviceDirection": 0} == mapping

    def test_build_cef_mapping(self):
        cef = self.create_cef_object()
        cef_mapping = cef.build_cef_mapping(self.event_stub()[0])
        expected = {
            'rt': '2016-08-22T16:24:30.726Z',
            'dst': '54.183.177.195',
            'cs1label': 'extras',
            'fname': 'File Integrity change detected',
            "msg": "A change was detected in file integrity target" \
                   "/opt/cloudpassage/*/* on Linux server" \
                   "Jlee-Chef-Node1 (54.183.177.195) (source: Scan)",
            'deviceDirection': 0,
            'cs1': {
                'policy_name': 'FIM halo',
                'server_id': '5b1d73b63e3711e68ead7f4b70b6c2b8',
                'finding_id': 'e748d9c6688411e6b7b32f750f990d28',
                'scan_id': 'e730037e688411e6b7b32f750f990d28',
                'server_reported_fqdn': 'localhost',
                'server_group_name': 'old_smoke',
                'server_label': 'Jlee-Chef-Node1',
                'critical': True,
                'server_primary_ip_address': '10.2.20.76',
                'server_platform': 'Linux',
                'type': 'fim_target_integrity_changed',
                'id': 'e750d982688411e6b7b32f750f990d28'
            },
            'dhost': 'ip-10-2-20-76'
        }
        assert expected == cef_mapping

    def test_format_cef(self):
        cef = self.create_cef_object()
        cef_format = cef.format_cef(self.event_stub())[0]
        expected = "CEF:0|CloudPassage|CPHalo|1.0|130|"\
                   "File Integrity change detected|9|"\
                   "rt=2016-08-22T16:24:30.726Z "\
                   "dst=54.183.177.195 "\
                   "cs1label=extras "\
                   "fname=File Integrity change detected "\
                   "msg=A change was detected in file integrity "\
                   "target/opt/cloudpassage/*/* on Linux "\
                   "serverJlee-Chef-Node1 (54.183.177.195) "\
                   "(source: Scan) "\
                   "deviceDirection=0 "\
                   "cs1={'policy_name': 'FIM halo', "\
                   "'server_id': '5b1d73b63e3711e68ead7f4b70b6c2b8', "\
                   "'finding_id': 'e748d9c6688411e6b7b32f750f990d28', "\
                   "'scan_id': 'e730037e688411e6b7b32f750f990d28', "\
                   "'server_reported_fqdn': 'localhost', "\
                   "'server_group_name': 'old_smoke', "\
                   "'server_label': 'Jlee-Chef-Node1', "\
                   "'critical': True, "\
                   "'server_primary_ip_address': '10.2.20.76', "\
                   "'server_platform': 'Linux', "\
                   "'type': 'fim_target_integrity_changed', "\
                   "'id': 'e750d982688411e6b7b32f750f990d28'} "\
                   "dhost=ip-10-2-20-76 "
        assert expected == cef_format
