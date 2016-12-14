#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
import copy_reg
import types
import datetime
import os
from functools import partial
import dateutil.parser
import cloudpassage
from lib.utility import Utility
import lib.settings as settings
from lib.config_helper import ConfigHelper


def _pickle_method(message):
    if message.im_self is None:
        return getattr, (message.im_class, message.im_func.func_name)
    else:
        return getattr, (message.im_self, message.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Event(object):
    """Initializing Event

        Args:
        key_id: Halo API key_id
        secret_key: Halo API secret key
    """

    def __init__(self, key_id, secret_key, args=None):
        self.utility = Utility(args)
        self.args = args or self.utility.updated_hash()
        self.event_id_exist = True
        self.key_id = key_id
        self.secret_key = secret_key
        self.data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
        self.has_configdir = False
        self.first_batch = True
        self.config = ConfigHelper()


    def create_halo_session_object(self):
        """create halo session object"""

        session = cloudpassage.HaloSession(self.key_id,
                                           self.secret_key,
                                           integration_string=self.config.ua)
        return session

    def get(self, per_page, date, page):
        """HTTP GET events from Halo"""

        session = self.create_halo_session_object()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/events?per_page=%s&page=%s&since=%s" % (per_page,
                                                           page,
                                                           date)
        return api.get(url)

    def latest_event(self, per_page, date, page):
        """get the latest event from Halo"""

        session = self.create_halo_session_object()
        api = cloudpassage.HttpHelper(session)
        url = "/v1/events?sort_by=created_at.desc&per_page=%s&page=%s&since=%s" % (per_page,
                                                                                   page,
                                                                                   date)
        return api.get(url)

    def batch(self, date):
        """multiprocessing to get all the events"""

        batched = []
        mpool = multiprocessing.Pool(settings.threads(), self.utility.init_worker)
        paginations = list(range(1, settings.pagination_limit() + 1))
        per_page = str(settings.per_page())

        try:
            partial_get = partial(self.get, per_page, date)
            data = mpool.map(partial_get, paginations)
            for i in data:
                batched.extend(i["events"])
            return batched
        except KeyboardInterrupt:
            print "Caught KeyboardInterrupt, terminating workers"
            mpool.terminate()
            mpool.join()

    def historical_limit_date(self):
        """get historical_limit_date (90 days)"""

        historical_limit = settings.historical_limit()
        temp = (datetime.datetime.now() - datetime.timedelta(days=historical_limit))
        date = temp.strftime('%Y-%m-%d')
        return date

    def sort_by(self, data, param):
        """ sorting the events data"""

        sort_data = sorted(data, key=lambda x: x[param])
        return sort_data

    def get_end_date(self, dates, end_date):
        """find the end date of each events batch"""

        if end_date != self.historical_limit_date:
            return dates[-1]["created_at"]
        return dateutil.parser.parse(dates[-1]["created_at"]).strftime('%Y-%m-%d')

    def id_exists_check(self, data, event_id):
        """check event id exist"""
        return any(k['id'] == event_id for k in data)

    def loop_date(self, batched, end_date):
        """grab starting date for the next event batch"""

        sorted_data = self.sort_by(batched, "created_at")
        start_date = sorted_data[0]["created_at"]
        end_date = self.get_end_date(sorted_data, end_date)
        return start_date, end_date

    def initial_date(self):
        """grab the starting date"""

        config_files = os.listdir(self.args["configdir"])
        if config_files:
            for i in config_files:
                if "_" in i:
                    key_id, date = i.split("_")
                    if self.key_id == key_id:
                        return self.normalize_date(date)
        return self.args['starting']


    def check_config_exists(self):
        """check if config dir timestamp exists"""
        config_files = os.listdir(self.args["configdir"])
        if config_files:
            for i in config_files:
                if "_" in i:
                    key_id, date = i.split("_")
                    if self.key_id == key_id:
                        self.has_configdir = True

    def customize_date(self, date):
        """customize timestamp"""

        return date.replace(':', '+')

    def normalize_date(self, date):
        """normalizing timestamp"""
        return date.replace('+', ':')

    def file_exists_check(self, end_date):
        """check if timestamp file exists"""

        end_date = self.customize_date(end_date)
        initial_date = self.customize_date(self.initial_date())

        original = os.path.join(self.args["configdir"], "%s_%s" % (self.key_id, initial_date))
        new = os.path.join(self.args["configdir"], "%s_%s" % (self.key_id, end_date))

        files = os.listdir(self.args["configdir"])
        if any(self.key_id in filename for filename in files):
            self.utility.rename(original, new)
        else:
            newfile = open(new, 'w')
            newfile.close()

    def retrieve_events(self):
        """retrieve events"""

        end_date = self.initial_date()
        initial_event_id = self.latest_event("1", "", "1")["events"][0]["id"]
        self.check_config_exists()
        while self.event_id_exist:
            batched = self.batch(end_date)
            start_date, end_date = self.loop_date(batched, end_date)
            self.file_exists_check(end_date)
            if self.id_exists_check(batched, initial_event_id):
                self.event_id_exist = False

            if self.has_configdir and self.first_batch:
                self.first_batch = False
                batched.pop(0)

            if batched:
                self.utility.output_events(batched)
                print "Wrote: %s to %s" % (start_date, end_date)
