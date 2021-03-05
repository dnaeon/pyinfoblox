import json
import unittest
from os import getenv
from unittest import TestCase
from pyinfoblox import InfobloxWAPI

class BaseTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)
        self.infoblox = InfobloxWAPI(username=getenv("INFOBLOX_USERNAME"),
                                     password=getenv("INFOBLOX_PASSWORD"),
                                     wapi=getenv("INFOBLOX_URL_DEV"),
                                     verify=False)

        # load the data for testing
        with open('./tests/test_data/a.json') as jsonfile:
            self.a_base = json.load(jsonfile)
        with open('./tests/test_data/a_update.json') as jsonfile:
            self.a_base_update = json.load(jsonfile)
        with open('./tests/test_data/host.json') as jsonfile:
            self.host_base = json.load(jsonfile)
        with open('./tests/test_data/host_update.json') as jsonfile:
            self.host_base_update = json.load(jsonfile)
        with open('./tests/test_data/network_container.json') as jsonfile:
            self.network_container_base = json.load(jsonfile)
        with open('./tests/test_data/network_container_update.json') as jsonfile:
            self.network_container_base_update = json.load(jsonfile)
        with open('./tests/test_data/network.json') as jsonfile:
            self.network_base = json.load(jsonfile)
        with open('./tests/test_data/network_update.json') as jsonfile:
            self.network_base_update = json.load(jsonfile)
        with open('./tests/test_data/ptr.json') as jsonfile:
            self.ptr_base = json.load(jsonfile)
        with open('./tests/test_data/ptr_update.json') as jsonfile:
            self.ptr_base_update = json.load(jsonfile)
        
        network = self.network_base['network']
        if self.infoblox.network.get(network=network) == []:
            self.infoblox.network.create(network=network)