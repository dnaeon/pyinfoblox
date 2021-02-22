import sys
import unittest
sys.path.append('../')
from tests import BaseTestCase

class TestHostCases(BaseTestCase):

    def create_host(self, **kwargs):
        """Helper func to create hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
            extattrs (dict): The extensible attributes on the host
            aliases (list): Host record aliases
        Returns:
            res (dict): The reponse dict
        """
        res = self.infoblox.record_host.create(**kwargs)
        return res

    def delete_host(self, fqdn):
        """Helper func to delete hosts
        Args:
            fqdn (str): The host fqdn to delete
        Returns:
            res (dict): The reponse dict
        """
        host = self.get_host(fqdn)
        objref = host[0]['_ref']
        res = self.infoblox.record_host.delete(objref)
        return res

    def get_host(self, fqdn):
        """Helper func to get hosts
        Args:
            fqdn (str): The host fqdn to get
            return_fields (str): The return fields
        Returns:
            res (dict): The response dict
        """
        self.return_fields = "name,ipv4addrs,aliases,extattrs"
        res = self.infoblox.record_host.get(name=fqdn,
                                            _return_fields=self.return_fields)
        return res

    def search_host(self, **kwargs):
        """Helper func to search hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
        Returns:
            res (str): The response object string
        """
        res = self.infoblox.record_host.get(**kwargs)
        return res

    def update_host(self, **kwargs):
        """Helper func to create hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
        Returns:
            res (dict): The reponse dict
        """
        fqdn = self.host_base['name']
        host = self.get_host(fqdn)
        objref = host[0]['_ref']
        res = self.infoblox.record_host.update(objref=objref,
                                               **kwargs)
        return res 
        
    def test_create_host(self):
        """
        test creating a new host
        and the response is 201
        ande the response body is correct
        """
        fqdn = self.host_base['name']

        create_res = self.create_host(**self.host_base)
        host_res = self.get_host(fqdn)
        self.delete_host(fqdn)
        assert 'record:host' in create_res
        assert(host_res[0]['name'] == self.host_base['name'])
        assert(host_res[0]['aliases'] == self.host_base['aliases'])
        assert(host_res[0]['extattrs'] == self.host_base['extattrs'])
        assert(host_res[0]['ipv4addrs'][0]['ipv4addr'] == self.host_base['ipv4addrs'][0]['ipv4addr'])

    def test_get_host(self):
        """
        test getting a new host
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.host_base['name']
        create_res = self.create_host(**self.host_base)
        host_res = self.get_host(fqdn)
        self.delete_host(fqdn)
        assert 'record:host' in create_res
        assert(host_res[0]['name'] == self.host_base['name'])
        assert(host_res[0]['aliases'] == self.host_base['aliases'])
        assert(host_res[0]['extattrs'] == self.host_base['extattrs'])
        assert(host_res[0]['ipv4addrs'][0]['ipv4addr'] == self.host_base['ipv4addrs'][0]['ipv4addr'])

    def test_delete_host(self):
        """
        test deleting a new host
        and the response is 200
        """
        fqdn = self.host_base['name']

        create_res = self.create_host(**self.host_base)
        del_res = self.delete_host(fqdn)
        host_res = self.get_host(fqdn)
        assert 'record:host' in del_res
        assert host_res == []

        

    def test_update_host(self):
        """
        test updating a new host
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.host_base_update['name']
        create_res = self.create_host(**self.host_base)
        update_res = self.update_host(**self.host_base_update)
        host_res = self.get_host(fqdn)

        assert 'record:host' in update_res
        assert(host_res[0]['name'] == self.host_base_update['name'])
        assert(host_res[0]['aliases'] == self.host_base_update['aliases'])
        assert(host_res[0]['extattrs'] == self.host_base_update['extattrs'])
        assert(host_res[0]['ipv4addrs'][0]['ipv4addr'] == self.host_base_update['ipv4addrs'][0]['ipv4addr'])