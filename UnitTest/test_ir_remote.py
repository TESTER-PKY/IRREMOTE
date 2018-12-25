"""
This module is unit test module for IRremote
"""
import unittest
import mock
from Libraries.IRRemote import IRRemote
from requests import HTTPError

# flake8: noqa


class MockResponse(object):
    def __init__(self,xml_response, status_code):
        self.xml_response = xml_response
        self.status_code  = status_code

    def content(self):
        return self.xml_response

    def status_code(self):
        return self.status_code


def mocked_requests_post_success(*args, **kwargs):
    return MockResponse("""
                    <?xml version="1.0"?>
                    <ScripterHandsetCommand xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Command="power button" RepeatCount="0" />
                    """, 200)


def mocked_requests_post_bad_request(*args, **kwargs):
    return MockResponse("""
                    <?xml version="1.0"?>
                    <ScripterHandsetCommand xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" Command="power button" RepeatCount="0" />
                    """, 404)


class TestIRRemote(unittest.TestCase):
    """
    This class contains unit tests for IRRemote class
    """


    def setUp(self):
        self.irremote = IRRemote({'ir_ip':"192.168.1.3", "dut_slot": "1"})

    def tearDown(self):
        self.irremote = None

    @mock.patch('requests.post', side_effect=mocked_requests_post_success)
    def test_send_key_event_success(self,mock_post):
        self.irremote.send_key('CHANNELUP')

    @mock.patch('requests.post', side_effect=mocked_requests_post_bad_request)
    def test_send_key_event_failure(self,mock_post):
        with self.assertRaises(HTTPError):
            self.irremote.send_key('CHANNELUP')



def default_suite():
    """
    This function returns unit test suite composed of all test cases
    for class TestIRRemote
    :return:
    """
    return unittest.TestLoader().loadTestsFromTestCase(TestIRRemote)
