import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'lib'))
from jsonkv import JsonKv

class TestUnitJsonkv:
	def create_jsonkv_object(self):
		return JsonKv()

	def event_stub(self):
		stub = [
				{
				"id": "fabc32206f0811e6ade117257b3d2b69",
				"type": "fim_scan_requested",
				"name": "File Integrity scan requested",
				"message": "A file integrity monitoring scan was requested for Linux server <strong>ip-172-31-16-240</strong> (52.8.42.37) by Halo API key <strong>2f08af31 (Beagle-MTG)</strong> from IP address 52.8.10.254 (USA).",
				"server_id": "1528ec8803db11e5ab872fd6dc843290",
				"created_at": "2016-08-30T23:25:03.850Z",
				"critical": False,
				"actor_key_id": "2f08af31",
				"actor_key_label": "Beagle-MTG",
				"actor_ip_address": "52.8.10.254",
				"actor_country": "USA",
				"server_platform": "Linux",
				"server_hostname": "ip-172-31-16-240",
				"server_group_name": "Canary",
				"server_ip_address": "52.8.42.37",
				"server_reported_fqdn": "ip-172-31-16-240.us-west-1.compute.internal",
				"server_label": None,
				"server_primary_ip_address": "172.31.16.240",
				"server_display_name": "ip-172-31-16-240",
				}

			]
		return stub

	def test_format_json(self):
		jsonkv = self.create_jsonkv_object()
		json_data = json.loads(jsonkv.format_json(self.event_stub()))
		assert self.event_stub() == json_data['events']

	def test_format_kv(self):
		jsonkv = self.create_jsonkv_object()
		kv_data = jsonkv.format_kv(self.event_stub())
		for k,v in self.event_stub()[0].items():
			string = "%s=\"%s\" " % (k, v )
			assert string in kv_data[0]
