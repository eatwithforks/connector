import cloudpassage
import sys
import os
import yaml
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'lib'))
from event import Event

config_file_name = "portal.yml"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
config = yaml.load(file(config_file, 'r'))
key_id = config['key_id']
secret_key = config['secret_key']

date_today = datetime.date.today().isoformat()


class TestUnitEvent:
    def create_event_obj(self):
        options = {
            '--auth': config_file,
            '--starting': date_today
        }

        event = Event(key_id, secret_key, options)
        return event

    def test_event_get_is_not_empty(self):
        event = self.create_event_obj()
        resp = event.get(1, date_today, 1)
        assert resp['events']

    def test_latest_event_is_not_empty(self):
        event = self.create_event_obj()
        resp = event.latest_event(1, date_today, 1)
        assert resp['events']

    def test_historical_limit_date_is_valid(self):
        event = self.create_event_obj()
        resp = event.historical_limit_date()
        today = datetime.date.today()
        expected = (today - datetime.timedelta(days=90)).isoformat()
        assert expected == resp

    def test_sort_by_is_alphabetical(self):
        event = self.create_event_obj()
        data = [{'color': 'red'}, {'color': 'black'}, {'color': 'white'}]
        resp = event.sort_by(data, 'color')
        expected = [{'color': 'black'}, {'color': 'red'}, {'color': 'white'}]
        assert expected == resp

    def test_get_end_date_is_not_nil(self):
        event = self.create_event_obj()
        dates = [
            {"created_at": "2016-08-20"},
            {"created_at": "2016-08-19"},
            {"created_at": "2016-08-18"}
        ]
        resp = event.get_end_date(dates, "2016-08-19")
        expected = "2016-08-18"
        assert expected == resp

    def test_id_exists_check(self):
        event = self.create_event_obj()
        resp = event.get(1, date_today, 1)['events']
        event_id = resp[0]['id']
        id_exists = event.id_exists_check(resp, event_id)
        assert id_exists

    def test_loop_date(self):
        event = self.create_event_obj()
        data = [
            {"created_at": "2016-08-23"},
            {"created_at": "2016-08-22"},
            {"created_at": "2016-08-21"},
            {"created_at": "2016-08-20"}
        ]
        end_date = "2016-08-03"
        resp = event.loop_date(data, end_date)
        assert ("2016-08-20", "2016-08-23") == resp
