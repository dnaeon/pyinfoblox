class GridTestCases(BaseTestCase):
    def create_ddns_ace(self, ddns_ace):
        """Creates a list of DDNS Access Control Entries (ACE)
        Args:
            ddns_ace (dict): List of dicts of DDNS ACE in the format:
                {"allow_update": [{"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}]}
        Returns:
            res: The DDNS ACE object 
        """
        res = self.infoblox.grid_dns.create(allow_update=ddns_ace)

    def delete_ddns_ace(self, ddns_ace):
        """Deletes the DDNS Access Control Entry (ACE) list
        Args:
            ddns_ace (dict): List of dicts of DDNS ACE in the format:
                {"allow_update": [{"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"]}
        Returns:
            res: The DDNS ACE object 
        """
        res = self.infoblox.grid_dns.delete(allow_update=ddns_ace)

    def delete_ddns_ace_entry(self, ddns_ace_entry):
        """Deletes a DDNS Access Control Entry (ACE) from the ACE list
        Args:
            ddns_ace_entry (dict): DDNS ACE dict in the format:
                {"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}
        Returns:
            res: The DDNS ACE object 
        """
        ddns_ace = self.infoblox.grid_dns.get(_return_fields=allow_update)
        objref = ddns_ace['_ref']
        ace_list = [x for x in get_res['allow_update'][0]]
        if ddns_ace_entry in ace_list:
            ace_list.remove(ddns_ace_entry)
        update_res = self.infoblox.grid_dns.update(allow_update=ddns_ace,
                                                   objref=objref)
        return update_res

    def get_ddns_ace(self):
        """Gets a list of DDNS Access Control Entries (ACE)
        Args:
            ddns_ace (dict): List of dicts of DDNS ACE in the format:
                {"allow_update": [{"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}]}
        Returns:
            res: The DDNS ACE object 
        """
        res = self.infoblox.grid_dns.get(_return_fields=ddns_ace)
        return res
    
    def update_ddns_ace(self):
        """Adds a DDNS Access Control Entry (ACE) to the ACE list
        Args:
            ddns_ace_entry (dict): DDNS ACE dict in the format:
                {"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}
        Returns:
            res: The DDNS ACE object 
        """
        """Creates a DDNS Access Control Entries (ACE) entry
        Args:
            ddns_ace_entry (dict): DDNS ACE dict in the format:
                {"_struct": "addressac", 
                "address": "10.16.0.0/14", "permission": "ALLOW"}
        Returns:
            res: The DDNS ACE object 
        """
        ddns_ace = self.infoblox.grid_dns.get(_return_fields=allow_update)
        objref = ddns_ace['_ref']
        ace_list = [x for x in get_res['allow_update'][0]]
        if ddns_ace_entry not in ace_list:
            ace_list.append(ddns_ace_entry)
        update_res = self.infoblox.grid_dns.update(allow_update=ddns_ace,
                                                   objref=objref)
        return update_res
    
    