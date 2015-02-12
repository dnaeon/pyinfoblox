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

        """
        # Special case for 'record' objects.
        #
        # The Infoblox 'record' objects are in the following form:
        #
        #     'record:<objtype>'
        #
        # For example A records in Infoblox are 'record:a' objects.
        #
        # In order to use an Infoblox 'record' object replace the
        # colon character with underscore in your call, e.g. 'record_a'
        if 'record' in attr:
            attr = attr.replace('_', ':', 1)

        return InfobloxWAPIObject(
            objtype=attr,
            wapi=self.wapi,
            session=self.session
        )


class InfobloxWAPIObject(object):
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

    def get(self, **kwargs):
        """
        Get Infoblox objects

        Returns:
            A list of Infoblox objects

        Raises:
            InfobloxWAPIException

        """
        r = self.session.get(
            self.wapi + self.objtype,
            params=kwargs
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def create(self, **kwargs):
        """
        Create a new Infoblox object

        Returns:
            The object reference of the newly created object

        Raises:
            InfobloxWAPIException

        """
        r = self.session.post(
            self.wapi + self.objtype,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.CREATED:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def update(self, objref, **kwargs):
        """
        Update an Infoblox object

        Args:
            objref (str): Infoblox object reference

        Returns:
            The object reference of the updated object

        Raises:
            InfobloxWAPIException

        """
        r = self.session.put(
            self.wapi + objref,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def delete(self, objref):
        """
        Delete an Infoblox object

        Args:
            objref (str): Infoblox object reference

        Returns:
            The reference of the deleted object

        Raises:
            InfobloxWAPIException

        """
        r = self.session.delete(self.wapi + objref)

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()

    def function(self, objref, **kwargs):
        """
        Call a function on an Infoblox object

        Args:
            objref (str): Infoblox object reference

        Raises:
            InfobloxWAPIException

        """
        r = self.session.post(
            self.wapi + objref,
            data=json.dumps(kwargs)
        )

        if r.status_code != requests.codes.ok:
            raise InfobloxWAPIException(r.content)

        return r.json()
