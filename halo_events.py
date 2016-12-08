#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Event Connector"""
from lib.utility import Utility
from lib.event import Event


def main():
    """Main function for retrieve_events"""
    utility = Utility()
    args = utility.updated_hash()
    for i in args["api_keys"]:
        event = Event(i['key_id'], i['secret_key'])
        event.retrieve_events()


if __name__ == "__main__":
    main()
