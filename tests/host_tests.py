import sys
sys.path.append('../')
from . import BaseTestCase

class TestHostCases(BaseTestCase):

    def create_host(self, fqdn, ip_address, extattrs=None, aliases=None):
        """Helper func to create hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
            extattrs (dict): The extensible attributes on the host
            aliases (list): Host record aliases
        Returns:
            res (dict): The reponse dict
        """
        res = infoblox.record_host.create(name=fqdn,
                                          ipv4addrs=[{ip_address}],
                                          extattrs={},
                                          aliases=[])
        return res

    def delete_host(self, fqdn):
        """Helper func to delete hosts
        Args:
            fqdn (str): The host fqdn to delete
        Returns:
            res (dict): The reponse dict
        """
        res = infoblox.record_host.delete(name=fqdn,
                                          ipv4addrs=[{ip_address}],
                                          extattrs={},
                                          aliases=[])
        return res

    def get_host(self, fqdn):
        """Helper func to get hosts
        Args:
            fqdn (str): The host fqdn to get
        Returns:
            res (dict): The reponse dict
        """
        res = infoblox.record_host.get(name=fqdnn)
        return res

    def search_host(self, fqdn=None, ipv4addr=None, extattrs=None, aliases=None):
        """Helper func to create hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
        Returns:
            res (dict): The reponse dict
        """
        res = infoblox.record_host.get(name=fqdn,
                                       ipv4addrs=[{ip_address}],
                                       extattrs={},
                                       aliases=[])
        return res

    def update_host(self, fqdn, ip_address, extattrs=None, aliases=None):
        """Helper func to create hosts
        Args:
            fqdn (str): The host fqdn to post
            ip_address (str): The host ip address to post
        Returns:
            res (dict): The reponse dict
        """
        res = infoblox.record_host.create(name=fqdn,
                                          ipv4addrs=[{ip_address}],
                                          extattrs={},
                                          aliases=[])
    
    def test_create_host(self):
        """
        test creating a new host
        and the response is 201
        ande the response body is correct
        """
        fqdn = host_base['name']
        ip_address = host_base['ipv4addrs'][0]
        extattrs = host_base['extattrs']
        aliases = host_base['aliases']
        # try unpacking base_host as arg, pass kwargs to funcs
        res = self.create_host(fqdn, ip_address, extattrs=extattrs, aliases=aliases)
        self.assert res.status_code == 200
        self.assert res['name'] == host_base['name']