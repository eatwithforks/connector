#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Leef class"""
from lib.options import Options
import lib.loadyaml as loadyaml


class Leef(object):
    """Leef class"""
    def __init__(self, options=None):
        self.options = options or Options()
        self.configs = loadyaml.load_leef()

    def constants(self, event):
        """build leef constants"""
        return "LEEF:%s|%s|%s|%s|%s|" % (self.configs['leefFormatVersion'],
                                         self.configs['leefVendor'],
                                         self.configs['leefProduct'],
                                         self.configs['leefProductVersion'],
                                         event['name'])

    def event_category(self, event):
        """determine event category"""
        for key, value in self.configs['leefCategoriesByName'].items():
            if event['type'] in value:
                return key

    def build_leef_outliers(self, mapping, event):
        """build leef outliers"""
        category = self.event_category(event)
        mapping['cat'] = category if category else "unknown"
        mapping['leefDateFormat'] = self.configs['leefDateFormat']
        mapping['sev'] = 9 if event['critical'] else 3
        mapping['isLoginEvent'] = True if event['type'] in self.configs['leefLoginEventNames'] else False
        mapping['isLogoutEvent'] = True if event['type'] in self.configs['leefLogoutEventNames'] else False

    def build_leef_mapping(self, event):
        """build leef mapping"""
        mapping = {}
        self.build_leef_outliers(mapping, event)
        for key, value in self.configs['leefFieldMapping'].items():
            if key in event:
                mapping[value] = event[key]
                del event[key]
        if event:
            for ekey, evalue in event.items():
                mapping[ekey] = evalue
        return mapping

    def format_leef(self, batched):
        """format leef"""
        aggregated_leef = []
        for event in batched:
            leef_str = ""
            constants_map = self.constants(event)
            schema = self.build_leef_mapping(event)
            for key, value in schema.items():
                leef_str += "%s=%s     " % (key, value)
            aggregated_leef.append("%s%s" % (constants_map, leef_str))
        return aggregated_leef
