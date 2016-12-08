#!/usr/bin/python
# -*- coding: utf-8 -*-
"""options"""
import argparse


parser = argparse.ArgumentParser(description='Event Connector')
parser.add_argument('--starting', help='Specify start of event time range in ISO-8601 format', required=False)
parser.add_argument('--auth', help='Specify a file containing CloudPassage Halo API keys - Key ID and Key secret pairs (up to 5)', required=True)
parser.add_argument('--threads', help='Start num threads each reading pages of events in parallel', required=False)
parser.add_argument('--batchsize', help='Specify a limit for page numbers, after which we use since', required=False)
parser.add_argument('--configdir', help='Specify directory for configration files (saved timestamps)', required=False)
parser.add_argument('--jsonfile', help='Write events in raw JSON format to file with given filename', required=False)
parser.add_argument('--ceffile', help='Write events in CEF (ArcSight) format to file with given filename', required=False)
parser.add_argument('--leeffile', help='Write events in LEEF (QRadar) format to file with given filename', required=False)
parser.add_argument('--kvfile', help='Write events as key/value pairs to file with given filename', required=False)
parser.add_argument('--facility', help='--facility=<faility,priority> Facility options:'\
                                                    'auth authpriv cron daemon kern local0 local1 local2'\
                                                    'local3 local4 local5 local6 local7 lpr mail news syslog'\
                                                    'user uucp Priority options:  alert crit debug emerg err'\
                                                    'info notice warning [default: user,info]', default='user,info', required=False)
parser.add_argument('--cef', default=False, action='store_true', help='Write events in CEF (ArcSight) format to standard output (terminal)')
parser.add_argument('--kv', default=False, action='store_true', help='Write events as key/value pairs to standard output (terminal)')
parser.add_argument('--leefsyslog', default=False, action='store_true', help='Write events in LEEF (QRadar) format to syslog server')
parser.add_argument('--cefsyslog', default=False, action='store_true', help='Write events in CEF (ArcSight) format to syslog server')
parser.add_argument('--kvsyslog', default=False, action='store_true', help='Write events as key/value pairs to local syslog daemon')


class Options(object):
    """options class"""
    def __new__(cls):
        args = vars(parser.parse_args())
        return args
