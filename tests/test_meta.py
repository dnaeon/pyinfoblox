import requests
from os import getenv
from tests import BaseTestCase

class MetaTestCases(BaseTestCase):
    
    def get_attrs(self):
        """Get Infoblox attributes from the grid at /wapi/vX/?_schema
        Returns:
            res.json() (json list): the Infoblox grid supported objects
        """
        res = requests.get(url=f'{getenv("INFOBLOX_URL_DEV")}?_schema',
                           headers={'Content-Type': 'application/json'},
                           auth=(getenv("INFOBLOX_USERNAME"),
                                 getenv("INFOBLOX_PASSWORD")),
                           verify=False)
        if res.status_code == requests.codes.ok:
            return res.json()['supported_objects']
        return res.json()

    def interpolate(self, attr, attrs):
        """foo
        """
        self.root_objects = sorted(set([x.split(':')[0] for x in attrs if ':' in x]))

        self.exclusions = ['container','ipv4addr','ipv6addr','pool']
        self.attr = attr.replace(':', '_')
        if '_' in attr:
            # test if string returns foo:bar for objects following that pattern
            # that aren't in the list of objects not including a '_' in the object 
            # name
            if attr.split('_')[0] in self.root_objects \
                    and attr.split('_')[-1] not in self.exclusions:
                return True
            # test if string returns foo:bar_boaz for objects following that pattern
            # with a '_' in the object name
            elif attr.split('_')[0] in self.root_objects \
                    and attr.split('_')[-1] in self.exclusions:
                return True
            # catch root objects
            elif attr.split('_')[0] not in self.root_objects:
                return True
            # catch everything else, signaling a failure
            else:
                return False
        return True

    def test_string_interpolation(self):
        """
        test string interpolation 
        of objects
        """
        attrs = self.get_attrs()
        for attr in attrs:
            is_valid = self.interpolate(attr, attrs)
            assert is_valid
