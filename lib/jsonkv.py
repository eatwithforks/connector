"""Json and key-value formatter"""
import json


def format_json(batched):
    """Format raw data into json format"""
    aggregated_events = []
    for event in batched:
        aggregated_events.append(json.dumps(event))
        aggregated_events.append("\n")
    return aggregated_events

def format_kv(batched):
    """Format raw data into key-value format"""
    aggregated_kv = []
    for event in batched:
        kv_str = ""
        for key, value in event.items():
            kv_str += "%s=\"%s\" " % (key, value)
        kv_str += "\n"
        aggregated_kv.append(kv_str)
    return aggregated_kv
