"""Rsyslog class"""

import lib.validate as validate
import lib.loadyaml as loadyaml

try:
    import syslog
except ImportError:
    import socket


class Rsyslog(object):
    """ Initializing Rsyslog class:

        Args:
        operating_system: to check which operating system \
        the script is running on
        rsys: information from rsyslog.yml
        portal: information from portal.yml
        host: rsyslog host
        port: rsyslog port
    """

    def __init__(self):
        self.operating_system = validate.operating_system()
        self.rsys = loadyaml.load_rsyslog()
        self.portal = loadyaml.load_portal()
        self.host = self.portal["windows_syslog_host"]
        self.port = self.portal["windows_syslog_port"]
        self.facility = None
        self.priority = None

    def parse_facility(self, facility_option):
        """read in facility and priority from options"""

        facility, priority = facility_option.split(",")
        self.facility = self.rsys["facility"][self.operating_system][facility]
        self.priority = self.rsys["level"][priority]

    def linux_openlog(self):
        """open syslog for linux machine"""

        syslog.openlog('cpapi', 0, self.facility)

    def linux_syslog(self, data):
        """send message to syslog from linux operating system"""

        syslog.syslog(self.priority, data)

    def windows_openlog(self):
        """open syslog via socket module for windows operating system"""

        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def windows_syslog(self, data):
        """send message to syslog from windows operating system"""

        syslog_num = self.priority + self.facility*8
        self.windows_openlog().sendto('<%d>%s' % (syslog_num, data),
                                      (self.host, self.port))

    def windows_closelog(self):
        """close syslog for windows operating system"""

        self.windows_openlog().close()

    def process_openlog(self, facility_option):
        """open syslog"""

        self.parse_facility(facility_option)
        if self.operating_system is 'linux':
            return self.linux_openlog()
        return self.windows_openlog()

    def process_syslog(self, data):
        """send message to syslog"""

        for i in data:
            if self.operating_system is 'linux':
                self.linux_syslog(i)
            else:
                self.windows_syslog(i)

    def closelog(self):
        """close syslog"""

        if self.operating_system is 'windows':
            return self.windows_openlog().close()
