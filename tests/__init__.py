import requests
from pyinfoblox import InfobloxWAPI

class BaseTestCase(object):

    def __init__():
        self.infoblox = InfobloxWAPI(
                 username='admin'
                 password='admin'
                 wapi='https://localhost:8080/wapi/v1.1/',
                 verify=False)
        
        with open('./test_data/host.json') as jsonfile:
            self.host_base = jsonfile
        with open('./test_data/network.json') as jsonfile:
            self.network_base = jsonfile
        with open('./test_data/subnet.json') as jsonfile:
            self.subnet_base = jsonfile
        
        
