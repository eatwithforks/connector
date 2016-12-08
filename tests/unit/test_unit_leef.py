import cloudpassage
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'lib'))
from leef import Leef


class TestUnitLeef:
    def create_leef_object(self):
        leef = Leef({"leefsyslog": None})
        return leef

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

    def test_leef_constants(self):
        leef = self.create_leef_object()
        leef_constants = leef.constants(self.event_stub()[0])
        expected = "LEEF:1.0|CloudPassage|CPHalo" \
                   "|1.0|File Integrity change detected|"
        assert expected == leef_constants

    def test_leef_outliers(self):
        leef = self.create_leef_object()
        mapping = {}
        leef.build_leef_outliers(mapping, self.event_stub()[0])
        expected = {
            'sev': 9,
            'isLogoutEvent': False,
            'leefDateFormat': "yyyy-MM-dd'T'HH:mm:ss.SSS",
            'isLoginEvent': False,
            'cat': 'server_events'
        }
        assert expected == mapping

    def test_build_leef_mapping(self):
        leef = self.create_leef_object()
        leef_mapping = leef.build_leef_mapping(self.event_stub()[0])
        expected = {
            'sev': 9,
            'finding_id': 'e748d9c6688411e6b7b32f750f990d28',
            'srcName': 'ip-10-2-20-76',
            'server_label': 'Jlee-Chef-Node1',
            "message": "A change was detected in file integrity target" \
                       "/opt/cloudpassage/*/* on Linux server" \
                       "Jlee-Chef-Node1 (54.183.177.195) (source: Scan)",
            'id': 'e750d982688411e6b7b32f750f990d28',
            'server_id': '5b1d73b63e3711e68ead7f4b70b6c2b8',
            'isLogoutEvent': False,
            'leefDateFormat': "yyyy-MM-dd'T'HH:mm:ss.SSS",
            'isLoginEvent': False,
            'server_reported_fqdn': 'localhost',
            'critical': True,
            'policy': 'FIM halo',
            'server_primary_ip_address': '10.2.20.76',
            'type': 'fim_target_integrity_changed',
            'src': '54.183.177.195',
            'server_platform': 'Linux',
            'scan_id': 'e730037e688411e6b7b32f750f990d28',
            'server_group_name': 'old_smoke',
            'name': 'File Integrity change detected',
            'cat': 'server_events',
            'devTime': '2016-08-22T16:24:30.726Z'
        }
        assert expected == leef_mapping

    def test_format_leef(self):
        leef = self.create_leef_object()
        leef_format = leef.format_leef(self.event_stub())[0]
        expected = "LEEF:1.0|CloudPassage|CPHalo|1.0|"\
                   "File Integrity change detected|"\
                   "sev=9     "\
                   "finding_id=e748d9c6688411e6b7b32f750f990d28     "\
                   "srcName=ip-10-2-20-76     "\
                   "server_label=Jlee-Chef-Node1     "\
                   "message=A change was detected in file integrity "\
                   "target/opt/cloudpassage/*/* on Linux server"\
                   "Jlee-Chef-Node1 (54.183.177.195) (source: Scan)     "\
                   "id=e750d982688411e6b7b32f750f990d28     " \
                   "server_id=5b1d73b63e3711e68ead7f4b70b6c2b8     "\
                   "isLogoutEvent=False     "\
                   "leefDateFormat=yyyy-MM-dd'T'HH:mm:ss.SSS     "\
                   "isLoginEvent=False     "\
                   "server_reported_fqdn=localhost     "\
                   "critical=True     "\
                   "policy=FIM halo     "\
                   "server_primary_ip_address=10.2.20.76     "\
                   "type=fim_target_integrity_changed     "\
                   "src=54.183.177.195     "\
                   "server_platform=Linux     "\
                   "scan_id=e730037e688411e6b7b32f750f990d28     "\
                   "server_group_name=old_smoke     "\
                   "name=File Integrity change detected     "\
                   "cat=server_events     "\
                   "devTime=2016-08-22T16:24:30.726Z     "
        assert expected == leef_format
