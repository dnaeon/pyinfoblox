from ipaddress import IPv4Network
from tests import BaseTestCase
"""
TODO: 
- Add search tests
- Add next_available
- Add VCR
""" 
class TestNetworkCases(BaseTestCase):

    def create_network(self, **kwargs):
        """Helper func to create networks
        Args:
            network (str): The network to post
            extattrs (dict): The extensible attributes on the network
            comment (str): The network comment
        Returns:
            res (dict): The response dict
        """
        res = self.infoblox.network.create(**kwargs)
        return res

    def delete_network(self, network):
        """Helper func to delete networks
        Args:
            network (str): The network to delete
        Returns:
            res (dict): The reponse dict
        """
        network_cidr = self.network_base['network']
        network = self.get_network(network_cidr)
        objref = network[0]['_ref']
        res = self.infoblox.network.delete(objref)
        return res

    def get_network(self, network):
        """Helper func to get networks
        Args:
            network (str): The network cidr to get
            return_fields (str): The return fields
        Returns:
            res (dict): The response dict
        """
        network = self.network_base['network']
        return_fields = "network,comment,extattrs"
        res = self.infoblox.network.get(network=network,
                                        _return_fields=return_fields)
        return res

    def search_network(self, **kwargs):
        """Helper func to search networks
        Args:
            network (str): The network to post
        Returns:
            res (str): The response object string
        """
        res = self.infoblox.network.get(**kwargs)
        return res

    def update_network(self, **kwargs):
        """Helper func to create networks
        Args:
            network (str): The network to post
        Returns:
            res (dict): The reponse dict
        """
        network = self.network_base['network']
        network_res = self.get_network(network)
        objref = network_res[0]['_ref']
        res = self.infoblox.network.update(objref=objref,
                                               **kwargs)
        return res 
        
    def test_create_network(self):
        """
        test creating a new network
        and the response body is correct
        """
        network = self.network_base['network']
        create_res = self.create_network(**self.network_base)
        network_res = self.get_network(network)

        assert 'network' in create_res
        assert(network_res[0]['network'] == self.network_base['network'])
        assert(network_res[0]['extattrs'] == self.network_base['extattrs'])
        assert(network_res[0]['comment'] == self.network_base['comment'])


    def test_delete_network(self):
        """
        test deleting a new network
        and a get is empty
        """
        network = self.network_base['network']

        create_res = self.create_network(**self.network_base)
        del_res = self.delete_network(network)
        network_res = self.get_network(network)

        assert 'network' in del_res
        assert network_res == []

    def test_get_network(self):
        """
        test getting a new network
        ande the response body is correct
        """
        network = self.network_base['network']
        create_res = self.create_network(**self.network_base)
        network_res = self.get_network(network)

        assert 'network' in create_res
        assert(network_res[0]['network'] == self.network_base['network'])
        assert(network_res[0]['extattrs'] == self.network_base['extattrs'])
        assert(network_res[0]['comment'] == self.network_base['comment'])
      
    def test_update_network(self):
        """
        test updating a new network
        ande the response body is correct
        """
        network = self.network_base_update['network']

        create_res = self.create_network(**self.network_base)
        update_res = self.update_network(**self.network_base_update)
        network_res = self.get_network(network)

        assert 'network' in update_res
        assert(network_res[0]['network'] == self.network_base_update['network'])
        assert(network_res[0]['extattrs'] == self.network_base_update['extattrs'])
        assert(network_res[0]['comment'] == self.network_base_update['comment'])

    def setup_method(self, method):
        network = self.network_base['network']
        if self.infoblox.network.get(network=network) == []:
            self.infoblox.network.create(network=network)
        else:
            objref = self.infoblox.network.get(network=network)[0]['_ref']
            self.infoblox.network.delete(objref=objref)

    def teardown_method(self, method):
        network = self.network_base['network']
        if self.get_network(network):
            self.delete_network(network)
