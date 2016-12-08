"""This module contains methods that load different yml file"""
import os
import yaml


RSYSLOG_CONFIG = os.path.join(os.path.dirname(__file__), '../configs/rsyslog.yml')
PORTAL_CONFIG = os.path.join(os.path.dirname(__file__), '../configs/portal.yml')
CEF_CONFIG = os.path.join(os.path.dirname(__file__), '../configs/cef.yml')
LEEF_CONFIG = os.path.join(os.path.dirname(__file__), '../configs/leef.yml')


def load_rsyslog():
    """This method load the rsyslog.yml"""
    return yaml.load(file(RSYSLOG_CONFIG, 'r'))


def load_portal():
    """This method load the portal.yml"""
    return yaml.load(file(PORTAL_CONFIG, 'r'))


def load_cef():
    """This method load the cef.yml"""
    return yaml.load(file(CEF_CONFIG, 'r'))


def load_leef():
    """This method load the leef.yml"""
    return yaml.load(file(LEEF_CONFIG, 'r'))
