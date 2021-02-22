import json
import unittest
from os import getenv
from pyinfoblox import InfobloxWAPI

class BaseTestCase():

    def __init__(self):
        super().__init__()
        self.infoblox = InfobloxWAPI(
                username=getenv("INFOBLOX_USERNAME"),
                password=getenv("INFOBLOX_PASSWORD"),
                wapi=getenv("INFOBLOX_URL_DEV"),
                verify=False)
        
        with open('./test_data/host.json') as jsonfile:
            self.host_base = json.load(jsonfile)
        with open('./test_data/host_update.json') as jsonfile:
            self.host_base_update = json.load(jsonfile)
        # with open('./test_data/network.json') as jsonfile:
        #     self.network_base = json.load(jsonfile)
        # with open('./test_data/subnet.json') as jsonfile:
        #     self.subnet_base = json.load(jsonfile)
        
        
