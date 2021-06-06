from tests import BaseTestCase

"""
TODO: 
- Add VCR
""" 
class TestPtrCases(BaseTestCase):

    def create_ptr(self, **kwargs):
        """Helper func to create ptrs
        Args:
            fqdn (str): The ptr fqdn to post
            ip_address (str): The ptr ip address to post
            extattrs (dict): The extensible attributes on the ptr
        Returns:
            res (dict): The response dict
        """
        res = self.infoblox.record_ptr.create(**kwargs)
        return res

    def delete_ptr(self, fqdn):
        """Helper func to delete ptrs
        Args:
            fqdn (str): The ptr fqdn to delete
        Returns:
            res (dict): The response dict
        """
        ptr = self.get_ptr(fqdn)
        objref = ptr[0]['_ref']
        res = self.infoblox.record_ptr.delete(objref)
        return res

    def get_ptr(self, fqdn):
        """Helper func to get ptrs
        Args:
            fqdn (str): The ptr fqdn to get
            return_fields (str): The return fields
        Returns:
            res (dict): The response dict
        """
        return_fields = "ptrdname,ipv4addr,extattrs"
        res = self.infoblox.record_ptr.get(ptrdname=fqdn,
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
        addresses = self.infoblox.network.function(objref, _function='next_available_ip', num=1)
        ip = addresses['ips'][0]
        return ip

    def search_ptr(self, **kwargs):
        """Helper func to search ptrs
        Args:
            fqdn (str): The ptr fqdn to post
            ip_address (str): The ptr ip address to post
        Returns:
            res (str): The response object string
        """
        res = self.infoblox.record_ptr.get(**kwargs)
        return res

    def update_ptr(self, **kwargs):
        """Helper func to create ptrs
        Args:
            fqdn (str): The ptr fqdn to post
            ip_address (str): The ptr ip address to post
        Returns:
            res (dict): The response dict
        """
        fqdn = self.ptr_base['ptrdname']
        ptr = self.get_ptr(fqdn)
        objref = ptr[0]['_ref']
        res = self.infoblox.record_ptr.update(objref=objref,
                                               **kwargs)
        return res 
        
    def test_create_ptr(self):
        """
        test creating a new ptr
        and the response is 201
        and the response body is correct
        """
        fqdn = self.ptr_base['ptrdname']

        create_res = self.create_ptr(**self.ptr_base)
        ptr_res = self.get_ptr(fqdn)
        assert 'record:ptr' in create_res
        assert(ptr_res[0]['ptrdname'] == self.ptr_base['ptrdname'])
        assert(ptr_res[0]['extattrs'] == self.ptr_base['extattrs'])
        assert(ptr_res[0]['ipv4addr'] == self.ptr_base['ipv4addr'])

    def test_create_ptr_next_available_ip(self):
        """
        test creating a ptr with get_next_ip function
        and the response body is correct
        """
        fqdn = self.ptr_base['ptrdname']
        subnet = self.network_base['network']
        self.ptr_base['ipv4addr'] = self.get_next_address(subnet)
        create_res = self.create_ptr(**self.ptr_base)
        ptr_res = self.get_ptr(fqdn)

        assert 'record:ptr' in create_res
        assert(ptr_res[0]['ptrdname'] == self.ptr_base['ptrdname'])
        assert(ptr_res[0]['extattrs'] == self.ptr_base['extattrs'])
        assert(ptr_res[0]['ipv4addr'] == self.ptr_base['ipv4addr'])

    def test_delete_ptr(self):
        """
        test deleting a new ptr
        and the response is 200
        """
        fqdn = self.ptr_base['ptrdname']

        create_res = self.create_ptr(**self.ptr_base)
        del_res = self.delete_ptr(fqdn)
        ptr_res = self.get_ptr(fqdn)

        assert 'record:ptr' in del_res
        assert ptr_res == []

    def test_get_ptr(self):
        """
        test getting a new ptr
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.ptr_base['ptrdname']
        create_res = self.create_ptr(**self.ptr_base)
        ptr_res = self.get_ptr(fqdn)

        assert 'record:ptr' in create_res
        assert(ptr_res[0]['ptrdname'] == self.ptr_base['ptrdname'])
        assert(ptr_res[0]['extattrs'] == self.ptr_base['extattrs'])
        assert(ptr_res[0]['ipv4addr'] == self.ptr_base['ipv4addr'])
      
    def test_update_ptr(self):
        """
        test updating a new ptr
        and the response is 200
        ande the response body is correct
        """
        fqdn = self.ptr_base_update['ptrdname']

        create_res = self.create_ptr(**self.ptr_base)
        update_res = self.update_ptr(**self.ptr_base_update)
        ptr_res = self.get_ptr(fqdn)

        assert 'record:ptr' in update_res
        assert(ptr_res[0]['ptrdname'] == self.ptr_base_update['ptrdname'])
        assert(ptr_res[0]['extattrs'] == self.ptr_base_update['extattrs'])
        assert(ptr_res[0]['ipv4addr'] == self.ptr_base_update['ipv4addr'])
    
    def setup_method(self, method):
        self.infoblox.network.create(**self.network_base)

    def teardown_method(self, method):
        objref = self.infoblox.network.get(network=self.network_base['network'])[0]['_ref']
        self.infoblox.network.delete(objref=objref)
        fqdn = self.ptr_base['ptrdname']
        if self.get_ptr(fqdn):
            self.delete_ptr(fqdn)