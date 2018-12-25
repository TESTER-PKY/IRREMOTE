#!/usr/bin/env python27
"""
Description         Module handling for interfacing with device, via IR remote
"""

import requests
from requests import HTTPError

IR_KEYMAPPING = {
    'HOME': 'home button',
    'MUTE': 'mute button',
    'PAGEDOWN': 'page down button',
    'PAGEUP': 'page up button',
    'CHANNELUP': 'channel up button',
    'CHANNELDOWN': 'channel down button',
    'VOL-': 'volume down button',
    'VOL-': 'volume up button',
    'BACK': 'back button',
    'OK': 'OK button',
    'LEFT': 'arrow left button',
    'UP': 'arrow up button',
    'RIGHT': 'arrow right button',
    'DOWN': 'arrow down button',
    '0': '0 button',
    '1': '1 button',
    '2': '2 button',
    '3': '3 button',
    '4': '4 button',
    '5': '5 button',
    '6': '6 button',
    '7': '7 button',
    '8': '8 button',
    '9': '9 button',
    'POWER': 'power button',
    'RWD': 'rewind button',
    'FRWD': 'forward button',
    'STOP': 'stop button',
    'PLAY': 'play button',
    'PAUSE': 'pause button',
    'REC': 'record button',
    'GUIDE': 'tvguide button',
    'INFO': 'info button',
    'HELP': 'help button',
}


class IRRemote(object):
    """
    Methods and variables related with sending remote keys via IR. This 
    device provides a REST API, 
    """
    def __init__(self, params):
        """"
        :param url:  urlparse()-return-like object, relevant members:
            ir_ip : IP address of the IR Hub server
            dut_slot : slot id of the device under test
        """
        self.ir_ip = params['ir_ip']
        self.dut_slot = params['dut_slot']

    def send_key(self, remote_key):
        """"
        Invokes the IR device's rest API to send the specified key event
        """
        headers = {'content-type': 'text/xml'}
        url = 'http://{0}/Device{1}/'.format(self.ir_ip, self.dut_slot)
        print "ir_ip: ", self.ir_ip
        print "dut_slot: ", self.dut_slot
        print url
        print str(IR_KEYMAPPING[remote_key])
        xml_string = """<?xml version="1.0"?>
        <ScripterHandsetCommand
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        Command="{0}" RepeatCount="0" />
        """.format(IR_KEYMAPPING[remote_key])
        response = requests.post(url, data=xml_string, headers=headers,
                                 timeout=20)
        if response.status_code != 200:
            raise HTTPError("Sending IR key failed")

