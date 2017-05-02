import os
import yaml
import re
from collections import Counter


tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
en_yml = os.path.join(tests_dir, "configs/", "en.yml")
known_yml = os.path.join(tests_dir, "configs/", "known_events.yml")

en_events = yaml.load(file(en_yml, 'r'))
known_events = yaml.load(file(known_yml, 'r'))


class TestIntegrationEventTypes:
    def server_events(self, events):
        results = []
        for event in events:
            find = re.search('server_events', event)
            if find:
                results.append(event)
        return results

    def test_event_type_count_are_equal(self):
        known = known_events["server_events"].keys()
        en = self.server_events(en_events["en"]["server_events"].keys())
        difference = Counter(en) - Counter(known)
        assert difference == Counter()
