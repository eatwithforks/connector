import os
import re


class ConfigHelper(object):
    """This class contains all application configuration variables.

    All configuration variables in this class are derived from environment
    variables.

    Attributes:
        halo_api_key (str): Halo API key, sometimes referred to as 'key id'
        halo_api_secret_key (str): Halo API secret associated with halo_api_key
        halo_api_hostname (str): Hostname for Halo API
        halo_api_port (str): Halo API port
        slack_api_token (str): Slack API token
        slack_username (str): Donbot's user name (purely cosmetic)
        slack_icon (str): Donbot's avatar

    """
    def __init__(self):
        self.ua = ConfigHelper.get_ua_string()
        self.product_version = ConfigHelper.get_product_version()

    @classmethod
    def get_ua_string(cls):
        product = "HaloEventConnector"
        version = ConfigHelper.get_product_version()
        ua_string = product + "/" + version
        return ua_string

    @classmethod
    def get_product_version(cls):
        init = open(os.path.join(os.path.dirname(__file__),
                    "__init__.py")).read()
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        version = rx_compiled.search(init).group(1)
        return version