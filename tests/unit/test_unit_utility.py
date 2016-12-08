import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../', 'lib'))
from utility import Utility
from settings import Settings

auth_file_name = "keys.auth"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
auth_file = os.path.join(tests_dir, "configs/", auth_file_name)
configdir = os.path.join(tests_dir, "tests/data/")

class TestUnitUtility:
	def create_utility_object(self, options):
		return Utility(options)

	def create_settings_object(self):
		return Settings()

	def test_parse_auth(self):
		options = {
			'auth': auth_file,
		}
		utility = self.create_utility_object(options)
		resp = utility.parse_auth()
		assert resp[0].has_key('key_id')
		assert resp[0].has_key('secret_key')

	def test_parse_pagination_limit_batchsize_none(self):
		options = {
			'batchsize': None
		}
		utility = self.create_utility_object(options)
		setting = self.create_settings_object()
		resp = utility.parse_pagination_limit()
		assert resp == setting.pagination_limit()

	def test_parse_pagination_limit_batchsize_commandline(self):
		options = {
			'batchsize': 4
		}
		utility = self.create_utility_object(options)
		resp = utility.parse_pagination_limit()
		assert resp == 4

	def test_parse_pagination_limit_batchsize_str(self):
		options = {
			'batchsize': "cat"
		}
		utility = self.create_utility_object(options)
		try:
			utility.parse_pagination_limit()
		except ValueError as e:
			assert "is not an integer" in str(e)

	def test_parse_pagination_limit_batchsize_exceed(self):
		options = {
			'batchsize': 60
		}
		utility = self.create_utility_object(options)
		try:
			utility.parse_pagination_limit()
		except ValueError as e:
			assert "you have exceeded the batchsize limitation" in str(e)

	def test_parse_threads_none(self):
		options = {
			'threads': None
		}
		utility = self.create_utility_object(options)
		setting = self.create_settings_object()
		resp = utility.parse_threads()
		assert resp == setting.threads()

	def test_parse_threads_str(self):
		options = {
			'threads': "cat"
		}
		utility = self.create_utility_object(options)
		try:
			utility.parse_threads()
		except ValueError as e:
			assert "is not an integer" in str(e)

	def test_parse_threads_exceed(self):
		options = {
			'threads': 6
		}
		utility = self.create_utility_object(options)
		try:
			utility.parse_threads()
		except ValueError as e:
			assert "you have exceeded the thread limitation" in str(e)

	def test_check_starting_none(self):
		options = {
			'starting': None,
			'configdir': configdir
		}
		utility = self.create_utility_object(options)
		resp = utility.check_starting()
		assert resp[0].has_key('key_id')
		assert resp[0].has_key('end_date')

	def test_check_configdir_none(self):
		options = {
			'starting': '2016-08-30',
			'configdir': None
		}
		utility = self.create_utility_object(options)
		resp = utility.check_starting()
		assert resp is None

	def test_check_starting_configdir_none(self):
		options = {
			'starting': None,
			'configdir': None
		}
		utility = self.create_utility_object(options)
		try:
			utility.check_starting()
		except ValueError as e:
			assert "Please choose either --starting or --configdir" in str(e)
