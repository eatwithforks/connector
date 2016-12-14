import cloudpassage


class TestUnitHaloSession:
    def create_halo_session_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return session

    def test_integration_string(self):
        int_string = "integration/v1.0"
        ua_string = "sdk/v1.1"
        session = cloudpassage.HaloSession("", "",
                                           integration_string=int_string,
                                           user_agent=ua_string)
        desired = "%s %s" % (int_string, ua_string)
        assert desired == session.user_agent
