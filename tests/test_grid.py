from tests import BaseTestCase

class TestGridCases(BaseTestCase):

    def get_ddns_ace(self):
        """Gets a list of DDNS Access Control Entries (ACE)
        Returns:
            res: The DDNS ACE object 
        """
        res = self.infoblox.grid_dns.get(_return_fields='allow_update')
        return res
    
    def update_ddns_ace(self, ddns_ace):
        """Updates a DDNS Access Control Entries (ACE) list
        Args:
            ddns_ace (dict): List of dicts of DDNS ACE in the format:
                {"allow_update": [{"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}]}
        Returns:
            res: The DDNS ACE object 
        """
        get_res = self.get_ddns_ace()
        objref = get_res[0]['_ref']
        res = self.infoblox.grid_dns.update(allow_update=ddns_ace,
                                            objref=objref)
        return res

    def test_get_ddns_ace_list(self):
        """
        test getting a new a
        and the response is 200
        ande the response body is correct
        """
        ddns_res = self.get_ddns_ace()
        objref = ddns_res[0].pop('_ref')
        assert 'grid:dns' in objref
        assert(ddns_res[0]['allow_update'] == self.ddns_ace_base)
      
    def test_update_ddns_ace_list(self):
        """
        test updating a new a
        and the response is 200
        ande the response body is correct
        """

        update_res = self.update_ddns_ace(self.ddns_ace_base_update)
        ddns_res = self.get_ddns_ace()

        assert 'grid:dns' in update_res
        assert(ddns_res[0]['allow_update'] == self.ddns_ace_base_update)

    def setup_method(self, method):
        # create ddns ACE list to work with
        # since the resource "grid:dns" always exists, only GET/PUT is allowed
        # and PUT can be an upsert
        self.update_ddns_ace(ddns_ace=self.ddns_ace_base)