#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Cef class"""
from lib.options import Options
import lib.loadyaml as loadyaml
import datetime


class Cef(object):
    """Cef class"""
    def __init__(self, options=None):
        self.options = options or Options()
        self.configs = loadyaml.load_cef()

    def cef_constants(self, event):
        """build cef constants"""
        severity = 9 if event["critical"] else 3
        return "CEF:%s|%s|%s|%s|%s|%s|%s|" % (self.configs["cefVersion"],
                                              self.configs["cefVendor"],
                                              self.configs["cefProduct"],
                                              self.configs["cefProductVersion"],
                                              self.configs["eventIdMap"][event["type"]],
                                              event["name"],
                                              severity)

    def build_cef_outliers(self, mapping, event):
        """build cef outliers"""
        mapping['deviceDirection'] = 1 if 'actor_username' in event else 0

    def format_cef_date(self, date):
        date_time = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date_time.strftime('%b %d %Y %H:%M:%S UTC')

    def build_cef_mapping(self, event):
        """build cef mapping"""
        mapping = {}
        self.build_cef_outliers(mapping, event)
        for key, value in self.configs['cefFieldMapping'].items():
            if key in event:
                if key == "created_at":
                    cef_date = self.format_cef_date(event[key])
                    mapping[value] = cef_date
                else:
                    mapping[value] = event[key]
                del event[key]
        if event:
            mapping["cs1Label"] = "extras"
            mapping["cs1"] = event
        return mapping

    def escape_specials(self, cef_str):
        formatted = cef_str.replace("\\","\\\\")
        formatted = cef_str.replace("=","\\=")

        return formatted

    def format_cef(self, batched):
        """format cef"""
        aggregated_cef = []
        for event in batched:
            cef_str = ""
            constants_map = self.cef_constants(event)
            schema = self.build_cef_mapping(event)
            for key, value in schema.items():
                cef_str += "%s=%s " % (key, value)
            cef_raw = "%s%s" % (constants_map, cef_str)
            cef_formatted = self.escape_specials(cef_raw)

            aggregated_cef.append(cef_formatted)
        return aggregated_cef
