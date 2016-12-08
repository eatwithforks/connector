#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Utility class"""
import os
import signal
from lib.options import Options
from lib.leef import Leef
from lib.cef import Cef
from lib.rsyslog import Rsyslog
import lib.validate as validate
import lib.jsonkv as jsonkv
import lib.settings as settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Utility(object):
    """Utility class"""
    def __init__(self, options=None):
        self.options = options or Options()
        self.rsyslog = Rsyslog()
        self.leef = Leef(options)
        self.cef = Cef(options)

    def rename(self, original, new):
        """rename"""
        os.rename(original, new)

    def interrupt_handler(self, signum, frame):
        """interruptHandler"""
        print "Beginning shutdown..."

    def init_worker(self):
        """init_worker"""
        signal.signal(signal.SIGINT, self.interrupt_handler)

    def write_output(self, filename, formatted_events):
        """write output"""
        with open(filename, 'a') as outputfile:
            for formatted_event in formatted_events:
                outputfile.write(str(formatted_event))
        outputfile.close()

    def output_events(self, batched):
        """output events"""
        if self.options["ceffile"] is not None:
            self.write_output(self.options["ceffile"], self.cef.format_cef(batched))
        if self.options["jsonfile"] is not None:
            self.write_output(self.options["jsonfile"], jsonkv.format_json(batched))
        elif self.options["kvfile"] is not None:
            self.write_output(self.options["kvfile"], jsonkv.format_kv(batched))
        elif self.options['leeffile'] is not None:
            self.write_output(self.options["leeffile"], self.leef.format_leef(batched))
        elif self.options["cef"]:
            for formatted_event in self.cef.format_cef(batched):
                print formatted_event
        elif self.options["kv"]:
            for formatted_event in jsonkv.format_kv(batched):
                print formatted_event
        elif self.options["cefsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(self.cef.format_cef(batched))
            self.rsyslog.closelog()
        elif self.options["leefsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(self.leef.format_leef(batched))
            self.rsyslog.closelog()
        elif self.options["kvsyslog"]:
            self.rsyslog.process_openlog(self.options["facility"])
            self.rsyslog.process_syslog(jsonkv.format_kv(batched))
            self.rsyslog.closelog()
        else:
            pass

    def parse_auth(self):
        """parse auth file"""
        auth_keys = []
        with open(self.options['auth'], 'r') as outputfile:
            auth_file = map(str.rstrip, outputfile)
        for line in auth_file:
            key, secret = line.split("|")
            auth_keys.append({"key_id": key, "secret_key": secret})
        return auth_keys

    def parse_pagination_limit(self):
        """determine pagination_limit"""
        if self.options['batchsize'] is None:
            return settings.pagination_limit()
        validate.batchsize(self.options['batchsize'])
        return int(self.options['batchsize'])

    def parse_threads(self):
        """determine threads"""
        if self.options['threads'] is None:
            return settings.threads()
        validate.thread(self.options["threads"])
        return self.options['threads']

    def check_starting(self):
        """determine starting date"""
        if self.options["starting"] and self.options["configdir"] is None:
            validate.starting(self.options["starting"])
            return self.options["starting"]
        elif self.options["starting"] is None and self.options["configdir"]:
            return self.parse_configdir()
        else:
            try:
                return self.parse_configdir_file()[0]["end_date"]
            except:
                return self.options["starting"]

    def parse_configdir(self):
        """determine config directory"""
        if self.options["configdir"] is None:
            return os.path.join(os.path.dirname(__file__), os.pardir, 'configs')
        return self.options["configdir"]

    def parse_configdir_file(self):
        """determine configdir date"""
        key_date = []
        files = os.listdir(self.options["configdir"])
        if files:
            for onefile in files:
                if not onefile.startswith('.'):
                    if "_" in onefile:
                        key, end_date = onefile.split("_")
                        validate.starting(end_date)
                        key_date.append({"key_id": key, "end_date": end_date})
        else:
            raise ValueError("Please use --starting to specify a starting date")
        return key_date

    def updated_hash(self):
        """updated hash"""
        self.options["api_keys"] = self.parse_auth()
        self.options["batchsize"] = self.parse_pagination_limit()
        self.options["threads"] = self.parse_threads()
        self.options["starting"] = self.check_starting()
        self.options["configdir"] = self.parse_configdir()
        return self.options
