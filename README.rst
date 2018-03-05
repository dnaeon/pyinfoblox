pyinfoblox - Infoblox WAPI module for Python
============================================

.. image:: https://img.shields.io/pypi/v/pyinfoblox.svg
    :target: https://pypi.python.org/pypi/pyinfoblox/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/pyinfoblox.svg
    :target: https://pypi.python.org/pypi/pyinfoblox/
    :alt: Downloads

pyinfoblox is a Python module for interfacing with the Infoblox WAPI.

For more information about the Infoblox WAPI, please refer to the
`Infoblox WAPI documentation <https://ipam.illinois.edu/wapidoc/>`_.

pyinfoblox is Open Source and licensed under the
`BSD License <http://opensource.org/licenses/BSD-2-Clause>`_.

Requirements
============

* `Python 2.7.x or 3.x <https://www.python.org/>`_
* `requests <https://pypi.python.org/pypi/requests>`_

Contributions
=============

pyinfoblox is hosted on
`Github <https://github.com/dnaeon/pyinfoblox>`_. Please contribute
by reporting issues, suggesting features or by sending patches
using pull requests.

Installation
============

The easiest way to install pyinfoblox is by using ``pip``:

.. code-block:: bash

   $ pip install pyinfoblox

In order to install the latest version of pyinfoblox from the
Github repository simply execute these commands instead:

.. code-block:: bash

   $ git clone https://github.com/dnaeon/pyinfoblox.git
   $ cd pyinfoblox
   $ python setup.py install

Examples
========

The first thing we do when using ``pyinfoblox`` is to instantiate a
new ``InfobloxWAPI`` object.

.. code-block:: python

   >>> from __future__ import print_function
   >>> from pyinfoblox import InfobloxWAPI
   >>> infoblox = InfobloxWAPI(
   ...     username='admin',
   ...     password='p4ssw0rd',
   ...     wapi='https://localhost/wapi/v1.1/'
   ... )

Getting Infoblox networks is as easy as doing:

.. code-block:: python

   >>> networks = infoblox.network.get()
   >>> print(networks)

Getting a specific network in Infoblox is easy too:

.. code-block:: python

   >>> network = infoblox.network.get(network='192.168.1.0/24')
   >>> print(network)

Another example that will get all Infoblox ``ipv4address`` objects.

.. code-block:: python

   >>> ipv4address = infoblox.ipv4address.get()
   >>> print(ipv4address)

Here is how to create a new Infoblox network:

.. code-block:: python

   >>> objref = infoblox.network.create(
   ...     network='192.168.1.0/24',
   ...     comment='This is my test network'
   ... )
   >>> print(objref)
   u'network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default'

Creating new objects returns a reference to the newly created
object in Infoblox.

We can also update objects. When we update objects in Infoblox we
need to pass the object reference as well. This is how we can
update the ``network`` we created in the previous example

.. code-block:: python

   >>> infoblox.network.update(
   ...     objref='network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default',
   ...     comment='This is my updated network'
   ... )
   u'network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default'
   >>> network = infoblox.network.get(network='192.168.1.0/24')
   >>> print(network[0]['comment'])
   This is my updated network

When we no longer need an Infoblox object we can always remove it.
Just make sure to pass the object reference when deleting objects.

.. code-block:: python

   >>> infoblox.network.delete(
   ...     objref='network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default'
   ... )
   u'network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default'

As a last example we will see how to call functions on
Infoblox objects.

Here is how to call the ``next_available_ip`` function on a
``network`` object in order to get the next 3 available IP addresses:

.. code-block:: python
   
   >>> infoblox.network.function(
   ...     objref='network/ZG5zLm5ldHdvcmskMTkyLjE2OC4xLjAvMjQvMA:192.168.1.0/24/default',
   ...     _function='next_available_ip',
   ...     num=3
   ... )
   {u'ips': [u'192.168.1.21', u'192.168.1.22', u'192.168.1.23']}

This example below calls the ``restartservices`` function on a
``grid`` object:

.. code-block:: python

   >>> from __future__ import print_function
   >>> from pyinfoblox import InfobloxWAPI
   >>> infoblox = InfobloxWAPI(
   ...     username='admin',
   ...     password='p4ssw0rd',
   ...     wapi='https://localhost/wapi/v1.1/'
   ...)
   >>> grids = infoblox.grid.get()
   >>> print(grids)
   [{'_ref': 'grid/b25lLmNsdXN0ZXIkMA:com'}]
   >>> grid = grids[0]['_ref']
   >>> infoblox.grid.function(
   ...     objref=grid,
   ...     _function='restartservices',
   ...     member_order='SEQUENTIALLY',
   ...     restart_option='RESTART_IF_NEEDED',
   ...     sequential_delay=10,
   ...     service_option='ALL'
   ...)
