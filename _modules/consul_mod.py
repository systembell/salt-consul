# -*- coding: utf-8 -*-
'''
Execution module to provide consul functionality to Salt

.. versionadded:: 2014.7.0

:configuration: This module requires the python-consul python module and uses the
    following defaults which may be overridden in the minion configuration:

.. code-block:: yaml

    consul.host: 'localhost'
    consul.port: 8500
    consul.consistency: 'default'
'''

import os
import salt.utils
import codecs

# Import third party libs
HAS_CONSUL = False
try:
    import consul as consul
    HAS_CONSUL = True
except ImportError:
    pass

__virtualname__ = 'consul'


def __virtual__():
    '''
    Only load this module if python-consul
    is installed on this minion.
    '''
    if HAS_CONSUL:
        return __virtualname__
    else:
        return False


def _connect(host='localhost', port=8500, consistency='default', **kwargs):
    '''
    Returns an instance of the consul client
    '''
    if not host:
        host = __salt__['config.option']('consul.host')
    if not port:
        port = __salt__['config.option']('consul.port')
    if not consistency:
        consistency = __salt__['config.option']('consul.consistency')
    return consul.Consul(host, port, consistency)


def key_delete(key, recurse=None, **kwargs):
    '''
    Deletes the keys from consul, returns number of keys deleted

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_delete foo
    '''
    c = _connect(**kwargs)
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return c.kv.delete(key, recurse)


def key_exists(key, **kwargs):
    '''
    Return true if the key exists in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_exists foo
    '''
    c = _connect(**kwargs)
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return True
        

def key_get(key, **kwargs):
    '''
    Gets the value of the key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_get foo
    '''
    c = _connect(**kwargs)
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return data['Value']


def key_put(key, value, value_from_file=False, encoding='utf8', **kwargs):
    '''
    Sets the value of a key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_put foo bar
    '''
    c = _connect(**kwargs)

    if value_from_file:
        if not os.path.isfile(value):
            ret = {}
            ret['result'] = False
            ret['comment'] = path + " does not exist"

        if not salt.utils.istextfile(value):
            ret = {}
            ret['result'] = False
            ret['comment'] = path + " is not a text file"

        else:
            file_contents = codecs.open(value, 'rb', encoding=encoding).read()
            c.kv.put(key, file_contents)

    else:
        c.kv.put(key, value)

    index, data = c.kv.get(key)
    return data['Value']


def service_list(catalog=False, dc=None, index=None, **kwargs):
    '''
    List services known to Consul
    CLI Example:
    .. code-block:: bash
        salt '*' consul.service_list
    '''
    c = _connect(**kwargs)
    services = []
    if catalog:
        index, services = c.catalog.services(dc, index)
    else:
        for service, data in c.agent.services().items():
            services.append(service)
    return services


def service_get(name, dc=None, tag=None, index=None, **kwargs):
    '''
    Get a Consul service's details

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_get
    '''
    c = _connect(**kwargs)
    for service, data in c.agent.services().items():
        if name == service:
            return data
    return False


def service_register(name, service_id=None, port=None, tags=None, script=None, interval=None, ttl=None, **kwargs):
    '''
    Register a service with Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_register foo
    '''
    c = _connect(**kwargs)
    return c.agent.service.register(name, service_id, port, tags, script, interval, ttl)


def service_deregister(name, **kwargs):
    '''
    Deregister a service from Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_deregister foo
    '''
    c = _connect(**kwargs)
    if name not in service_list():
        return False
    return c.agent.service.deregister(name)


def check_list(**kwargs):
    '''
    List checks known to Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_list
    '''
    c = _connect(**kwargs)
    checks = []
    for check, data in c.agent.checks().items():
        checks.append(check)
    return checks


def check_get(name, **kwargs):
    '''
    Get the details of a check in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_get
    '''
    c = _connect(**kwargs)
    for check, data in c.agent.checks().items():
        if name == check:
            return data
    return False


def check_register(name, check_id=None, script=None, interval=None, ttl=None, notes=None, **kwargs):
    '''
    Register a check with Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_register foo
    '''
    c = _connect(**kwargs)
    return c.agent.check.register(name, check_id, script, interval, ttl, notes)


def check_deregister(name, **kwargs):
    '''
    Deregister a check from Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_deregister foo
    '''
    c = _connect(**kwargs)
    if name not in check_list():
        return False
    return c.agent.check.deregister(name)


def get_service_status(name,index=None, passing=None, **kwargs):
    '''
    Get the health status of a service in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.get_service_status
    '''
    c = _connect(**kwargs)
    index, nodes = c.health.service(name, index, passing)
    node_list = []
    for node in nodes:
        for check in node['Checks']:
            if name == check['ServiceName']:
                node_list.append({check['Node']: check['Status']})
    return node_list


def node_list(**kwargs):
    '''
    List nodes in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.node_list
    '''
    c = _connect(**kwargs)
    node_list = []
    index, nodes = c.catalog.nodes()
    for node in nodes:    
        node_list.append({node['Node']: node['Address']})
    return node_list


def node_get(name, dc=None, tag=None, index=None, **kwargs):
    '''
    Get a Consul node's details

    CLI Example:

    .. code-block:: bash

        salt '*' consul.node_get
    '''
    c = _connect(**kwargs)
    index, node = c.catalog.node(name, dc, tag, index)
    if not node:
        return False
    return node


def dc_list(**kwargs):
    '''
    List datacenters in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.dc_list
    '''
    c = _connect(**kwargs)
    return c.catalog.datacenters()


def ttl_pass(name, notes=None, type='check', **kwargs):
    '''
    Mark a ttl-based service or check as passing

    CLI Example:

    .. code-block:: bash

        salt '*' consul.ttl_pass foo type=check
        
        salt '*' consul.ttl_pass foo type=service
    '''
    c = _connect(**kwargs)
    if type == 'service':
        name = 'service:' + name
    return c.agent.check.ttl_pass(name, notes)


def ttl_warn(name, notes=None, type='check', **kwargs):
    '''
    Mark a ttl-based service or check as warning

    CLI Example:

    .. code-block:: bash

        salt '*' consul.ttl_warn foo type=check
        
        salt '*' consul.ttl_warn foo type=service
    '''
    c = _connect(**kwargs)
    if type == 'service':
        name = 'service:' + name
    return c.agent.check.ttl_warn(name, notes)


def ttl_fail(name, notes=None, type='check', **kwargs):
    '''
    Mark a ttl-based service or check as failing

    CLI Example:

    .. code-block:: bash

        salt '*' consul.ttl_fail foo type=check
        
        salt '*' consul.ttl_fail foo type=service
    '''
    c = _connect(**kwargs)
    if type == 'service':
        name = 'service:' + name
    return c.agent.check.ttl_fail(name, notes)

