# Copyright (c) 2014 Marin Atanasov Nikolov <dnaeon@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer
#    in this position and unchanged.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR(S) ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR(S) BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Infoblox WAPI module for Python

"""

import json

import requests

class InfobloxWAPIException(Exception):
    """
    Generic Infoblox WAPI Exception

    """
    pass


class InfobloxWAPI(object):
    """
    Abstracted, generic implementation of an Infoblox Object and connector
    """
    def __init__(self,
                 username,
                 password,
                 wapi='https://localhost/wapi/v1.1/',
                 verify=False):
        """
        Create a new Infoblox WAPI instance

        Args:
            username (str): Username to use for authentication
            password (str): Password to use for authentication
            wapi     (str): URL to the Infoblox WAPI
            verify  (bool): Verify or not SSL certificate

        Attributes:
            username (str): Username to use for authentication
            password (str): Password to use for authentication
            wapi     (str): URL to the Infoblox WAPI
            verify  (bool): Verify or not SSL certificate
            session  (obj): Session connector and auth
        """
        self.username = username
        self.password = password
        self.wapi = wapi
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({'content-type': 'application/json'})
        self.session.verify = verify

    def __getattr__(self, attr):
        """
        Dynamically create a new Infoblox object class, e.g. 'network'

        Args:
            attr (str): The WAPI Object name that's requested

        Returns:
            InfobloxWAPIObject (obj): The Infoblox Object session output/payload

        """
        # Special case for root objects, with subobjects under them.
        #
        # Infoblox objects with children are in the following form:
        #
        #     'record:<objtype>'
        #
        # For example A records in Infoblox are 'record:a' objects.
        #
        # In order to use an Infoblox child-object replace the
        # colon character with underscore in your call, e.g. 'record_a'

        # all root objects that have children, according to WAPI v2.9
        root_objects_res = self.session.get(self.wapi,
                                            params='_schema').json()['supported_objects']
        root_objects = sorted(set([x.split(':')[0] for x in root_objects_res if ':' in x]))
        # root_objects = ['certificate','ciscoise','ddns','dhcp','discovery',
        #                 'dtc','dxl','grid','hsm','ipam','license','localuser',
        #                 'member','msserver','notification','nsgroup','outbound',
        #                 'parentalcontrol','record','rir','sharedrecord'
        #                 'smartfolder','tacacsplus','threatanalytics'
        #                 'threatinsight','threatprotection']

        # trailing child objects that have underscores, deterministic enough \
        # to fix with single replace
        exclusions = ['container','ipv4addr','ipv6addr','pool']

        if '_' in attr:
            if attr.split('_')[0] in root_objects\
                    and attr.split('_')[-1] not in exclusions:
                # catch all with no underscores
                attr = attr.replace('_', ':') 
            elif attr.split('_')[0] in root_objects\
                    and attr.split('_')[-1] in exclusions:
                # catch all with underscores
                attr = attr.replace('_', ':', 1)

        return InfobloxWAPIObject(
            objtype=attr,
            wapi=self.wapi,
            session=self.session
        )


class InfobloxWAPIObject(object):
    """
    The Infoblox Object instantiation with CRUD operators
    """
    def __init__(self, objtype, wapi, session):
        """
        Create a new Infoblox WAPI object class, e.g. 'network'

        Args:
            objtype (str): The Infoblox object type
            wapi    (str): URL to the Infoblox WAPI
            session (str): A valid Infoblox WAPI session

        """
        self.objtype = objtype
        self.wapi = wapi
        self.session = session

    def get(self, objref=None, timeout=None, **kwargs):
        """
        Get Infoblox objects

        Args:
            objref (str, optional): The _ref/object reference of the \
                                    InfobloxObject for PUT operations
            timeout (int, optional): The request timeout
            **kwargs: Keyword Arguments, unpacked

        Returns:
            With objref, one Infoblox object,
            in search form, a list of Infoblox objects

        Raises:
            InfobloxWAPIException

        """
        r = self.session.get(
            self.wapi + (objref if objref is not None else self.objtype),
            params=kwargs, timeout=timeout
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def create(self, timeout=None, **kwargs):
        """
        Create a new Infoblox object

        Args:
            timeout (int, optional): The request timeout
            **kwargs: Keyword Arguments, unpacked

        Returns:
            The object reference of the newly created object

        Raises:
            InfobloxWAPIException

        """
        # Parameters with leading underscores are options, and
        # must be sent as params, not data.
        # Make sure that parameters with leading underscores are
        # also removed from kwargs as well
        params = {k:kwargs[k] for k in kwargs if k.startswith('_')}
        _ = [kwargs.pop(k) for k in params]

        r = self.session.post(
            self.wapi + self.objtype,
            params=params,
            timeout=timeout,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.CREATED:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def update(self, objref, timeout=None, **kwargs):
        """
        Update an Infoblox object

        Args:
            objref (str): Infoblox object reference
            timeout (int, optional): The request timeout
            **kwargs: Keyword Arguments, unpacked

        Returns:
            The object reference of the updated object

        Raises:
            InfobloxWAPIException

        """
        # Parameters with leading underscores are options, and
        # must be sent as params, not data.
        # Make sure that parameters with leading underscores are
        # also removed from kwargs as well
        params = {k:kwargs[k] for k in kwargs if k.startswith('_')}
        _ = [kwargs.pop(k) for k in params]
        r = self.session.put(
            self.wapi + objref,
            params=params,
            timeout=timeout,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def delete(self, objref, timeout=None):
        """
        Delete an Infoblox object

        Args:
            objref (str): Infoblox object reference
            timeout (int, optional): The request timeout

        Returns:
            The reference of the deleted object

        Raises:
            InfobloxWAPIException

        """
        r = self.session.delete(self.wapi + objref, timeout=timeout)

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def function(self, objref, timeout=None, **kwargs):
        """
        Call a function on an Infoblox object

        Args:
            objref (str): Infoblox object reference
            timeout (int, optional): The request timeout
            **kwargs: Keyword Arguments, unpacked

        Raises:
            InfobloxWAPIException

        """
        # Parameters with leading underscores are options, and
        # must be sent as params, not data.
        # Make sure that parameters with leading underscores are
        # also removed from kwargs as well
        params = {k:kwargs[k] for k in kwargs if k.startswith('_')}
        _ = [kwargs.pop(k) for k in params]

        r = self.session.post(
            self.wapi + objref,
            params=params,
            timeout=timeout,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()
