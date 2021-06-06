from tests import BaseTestCase
"""
TODO: 
- Add next_available
- Add VCR
""" 
class Testnetwork_containerContainerCases(BaseTestCase):

    def create_networkcontainer(self, **kwargs):
        """Helper func to create network_containers
        Args:
            network_container (str): The network_container to post
            extattrs (dict): The extensible attributes on the network_container
            comment (str): The network_container comment
        Returns:
            res (dict): The response dict
        """
        res = self.infoblox.networkcontainer.create(**kwargs)
        return res

    def delete_networkcontainer(self, network_container):
        """Helper func to delete network_containers
        Args:
            network_container (str): The network_container to delete
        Returns:
            res (dict): The reponse dict
        """
        network_container_cidr = self.network_container_base['network']
        network_container = self.get_networkcontainer(network_container_cidr)
        objref = network_container[0]['_ref']
        res = self.infoblox.networkcontainer.delete(objref)
        return res

    def get_networkcontainer(self, network_container):
        """Helper func to get network_containers
        Args:
            network_container (str): The network_container cidr to get
            return_fields (str): The return fields
        Returns:
            res (dict): The response dict
        """
        network_container = self.network_container_base['network']
        return_fields = "network,comment,extattrs"
        res = self.infoblox.networkcontainer.get(network=network_container,
                                                 _return_fields=return_fields)
        return res

    def search_networkcontainer(self, **kwargs):
        """Helper func to search network_containers
        Args:
            network_container (str): The network_container to post
        Returns:
            res (str): The response object string
        """
        res = self.infoblox.networkcontainer.get(**kwargs)
        return res

    def update_networkcontainer(self, **kwargs):
        """Helper func to create network_containers
        Args:
            network_container (str): The network_container to post
        Returns:
            res (dict): The reponse dict
        """
        network_container = self.network_container_base['network']
        network_container_res = self.get_networkcontainer(network_container)
        objref = network_container_res[0]['_ref']
        kwargs.pop('network')
        res = self.infoblox.networkcontainer.update(objref=objref,
                                                    **kwargs)
        return res 
        
    def test_create_networkcontainer(self):
        """
        test creating a new network_container
        and the response is 201
        ande the response body is correct
        """
        network_container = self.network_container_base['network']
        create_res = self.create_networkcontainer(**self.network_container_base)
        network_container_res = self.get_networkcontainer(network_container)

        assert 'networkcontainer' in create_res
        assert(network_container_res[0]['network'] == self.network_container_base['network'])
        assert(network_container_res[0]['extattrs'] == self.network_container_base['extattrs'])
        assert(network_container_res[0]['comment'] == self.network_container_base['comment'])


    def test_delete_networkcontainer(self):
        """
        test deleting a new network_container
        and the response is 200
        """
        network_container = self.network_container_base['network']

        create_res = self.create_networkcontainer(**self.network_container_base)
        del_res = self.delete_networkcontainer(network_container)
        network_container_res = self.get_networkcontainer(network_container)

        assert 'networkcontainer' in del_res
        assert network_container_res == []

    def test_get_networkcontainer(self):
        """
        test getting a new network_container
        and the response is 200
        ande the response body is correct
        """
        network_container = self.network_container_base['network']
        create_res = self.create_networkcontainer(**self.network_container_base)
        network_container_res = self.get_networkcontainer(network_container)

        assert 'networkcontainer' in create_res
        assert(network_container_res[0]['network'] == self.network_container_base['network'])
        assert(network_container_res[0]['extattrs'] == self.network_container_base['extattrs'])
        assert(network_container_res[0]['comment'] == self.network_container_base['comment'])
      
    def test_update_networkcontainer(self):
        """
        test updating a new network_container
        and the response is 200
        ande the response body is correct
        """
        network_container = self.network_container_base_update['network']

        create_res = self.create_networkcontainer(**self.network_container_base)
        update_res = self.update_networkcontainer(**self.network_container_base_update)
        network_container_res = self.get_networkcontainer(network_container)

        assert 'networkcontainer' in update_res
        assert(network_container_res[0]['network'] == self.network_container_base_update['network'])
        assert(network_container_res[0]['extattrs'] == self.network_container_base_update['extattrs'])

    def teardown_method(self, method):
        network = self.network_container_base['network']
        if self.get_networkcontainer(network):
            self.delete_networkcontainer(network)