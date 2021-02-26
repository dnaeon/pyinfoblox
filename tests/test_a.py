from tests import BaseTestCase

"""
TODO: 
- Add search tests
- Add VCR
""" 
class TestACases(BaseTestCase):

    def create_a(self, **kwargs):
        """Helper func to create As
        Args:
            fqdn (str): The a fqdn to post
            ip_address (str): The a ip address to post
            extattrs (dict): The extensible attributes on the a
            aliases (list): a record aliases
        Returns:
            res (dict): The response dict
        """
        res = self.infoblox.record_a.create(**kwargs)
        return res

    def delete_a(self, fqdn):
        """Helper func to delete as
        Args:
            fqdn (str): The a fqdn to delete
        Returns:
            res (dict): The response dict
        """
        a = self.get_a(fqdn)
        objref = a[0]['_ref']
        res = self.infoblox.record_a.delete(objref)
        return res

    def get_a(self, fqdn):
        """Helper func to get as
        Args:
            fqdn (str): The a fqdn to get
            return_fields (str): The return fields
        Returns:
            res (dict): The response dict
        """
        return_fields = "name,ipv4addr,extattrs"
        res = self.infoblox.record_a.get(name=fqdn,
                                            _return_fields=return_fields)
        return res

    def get_next_address(self, subnet):
        """Helper func for get_next_ip
        Args:
            subnet (str): The parent network to get an IP from
        Returns:
            ip (str): The IP address
        """
        net_data = self.network_base
        network = self.infoblox.network.get(network=net_data['network'])
        objref = network[0]['_ref']
        addresses = self.infoblox.network.function(objref,
                                                   _function='next_available_ip', 
                                                   num=1)
        ip = addresses['ips'][0]
        return ip

    def search_a(self, **kwargs):
        """Helper func to search as
        Args:
            fqdn (str): The a fqdn to post
            ip_address (str): The a ip address to post
        Returns:
            res (str): The response object string
        """
        res = self.infoblox.record_a.get(**kwargs)
        return res

    def update_a(self, **kwargs):
        """Helper func to create as
        Args:
            fqdn (str): The a fqdn to post
            ip_address (str): The a ip address to post
        Returns:
            res (dict): The response dict
        """
        fqdn = self.a_base['name']
        a = self.get_a(fqdn)
        objref = a[0]['_ref']
        res = self.infoblox.record_a.update(objref=objref,
                                            **kwargs)
        return res 
        
    def test_create_a(self):
        """
        test creating a new a
        and the response is 201
        and the response body is correct
        """
        fqdn = self.a_base['name']

        create_res = self.create_a(**self.a_base)
        a_res = self.get_a(fqdn)

        assert 'record:a' in create_res
        assert(a_res[0]['name'] == self.a_base['name'])
        assert(a_res[0]['extattrs'] == self.a_base['extattrs'])
        assert(a_res[0]['ipv4addr'] == self.a_base['ipv4addr'])

    def test_create_a_next_available_ip(self):
        """
        test creating a a with get_next_ip function
        and the response body is correct
        """
        fqdn = self.a_base['name']
        subnet = self.network_base['network']
        self.a_base['ipv4addr'] = self.get_next_address(subnet)
        create_res = self.create_a(**self.a_base)
        a_res = self.get_a(fqdn)

        assert 'record:a' in create_res
        assert(a_res[0]['name'] == self.a_base['name'])
        assert(a_res[0]['extattrs'] == self.a_base['extattrs'])
        assert(a_res[0]['ipv4addr'] == self.a_base['ipv4addr'])

    def test_delete_a(self):
        """
        test deleting a new a
        and the response is 200
        """
        fqdn = self.a_base['name']

        create_res = self.create_a(**self.a_base)
        del_res = self.delete_a(fqdn)
        a_res = self.get_a(fqdn)

        assert 'record:a' in del_res
        assert a_res == []

    def test_get_a(self):
        """
        test getting a new a
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.a_base['name']
        create_res = self.create_a(**self.a_base)
        a_res = self.get_a(fqdn)

        assert 'record:a' in create_res
        assert(a_res[0]['name'] == self.a_base['name'])
        assert(a_res[0]['extattrs'] == self.a_base['extattrs'])
        assert(a_res[0]['ipv4addr'] == self.a_base['ipv4addr'])
      
    def test_update_a(self):
        """
        test updating a new a
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.a_base_update['name']

        create_res = self.create_a(**self.a_base)
        update_res = self.update_a(**self.a_base_update)
        a_res = self.get_a(fqdn)

        assert 'record:a' in update_res
        assert(a_res[0]['name'] == self.a_base_update['name'])
        assert(a_res[0]['extattrs'] == self.a_base_update['extattrs'])
        assert(a_res[0]['ipv4addr'] == self.a_base_update['ipv4addr'])

    def teardown_method(self, method):
        fqdn = self.a_base['name']
        if self.get_a(fqdn):
            self.delete_a(fqdn)
