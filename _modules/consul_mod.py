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

# Import third party libs
HAS_CONSUL = False
try:
    import consul as consul
    HAS_CONSUL = True
except ImportError:
    pass


def __virtual__():
    '''
    Only load this module if python-consul
    is installed on this minion.
    '''
    if HAS_CONSUL:
        return __virtualname__
    else:
        return False


def _connect(host='localhost', port=8500, consistency='default'):
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


def key_delete(key, recurse=None):
    '''
    Deletes the keys from consul, returns number of keys deleted

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_delete foo
    '''
    # Get connection args from keywords if set

    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return c.kv.delete(key, recurse)


def key_exists(key):
    '''
    Return true if the key exists in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_exists foo
    '''
    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return True
        

def key_get(key):
    '''
    Gets the value of the key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_get foo
    '''
    c = _connect()
    index, data = c.kv.get(key)
    if not data:
        return False
    else:
        return data['Value']


def key_put(key, value):
    '''
    Sets the value of a key in consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.key_put foo bar
    '''
    c = _connect()
    c.kv.put(key, value)
    index, data = c.kv.get(key)
    return data['Value']


def service_list():
    '''
    List services known to Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_list
    '''
    c = _connect()
    services = []
    for service, data in c.agent.services().items():
        services.append(service)
    return services


def service_get(name):
    '''
    Get a Consul service's details

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_get
    '''
    c = _connect()
    for service, data in c.agent.services().items():
        if name == service:
            return data
    return False


def service_register(name, service_id=None, port=None, tags=None, script=None, interval=None, ttl=None):
    '''
    Register a service with Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_register foo
    '''
    c = _connect()
    return c.agent.service.register(name, service_id, port, tags, script, interval, ttl)


def service_deregister(name):
    '''
    Deregister a service from Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.service_deregister foo
    '''
    c = _connect()
    if name not in service_list():
        return False
    return c.agent.service.deregister(name)


def check_list():
    '''
    List checks known to Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_list
    '''
    c = _connect()
    checks = []
    for check, data in c.agent.checks().items():
        checks.append(check)
    return checks


def check_get(name):
    '''
    Get the details of a check in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_get
    '''
    c = _connect()
    for check, data in c.agent.checks().items():
        if name == check:
            return data
    return False


def check_register(name, check_id=None, script=None, interval=None, ttl=None, notes=None):
    '''
    Register a check with Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_register foo
    '''
    c = _connect()
    return c.agent.check.register(name, check_id, script, interval, ttl, notes)


def check_deregister(name):
    '''
    Deregister a check from Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.check_deregister foo
    '''
    c = _connect()
    if name not in check_list():
        return False
    return c.agent.check.deregister(name)


def get_service_status(name,index=None, passing=None):
    '''
    Get the health status of a service in Consul

    CLI Example:

    .. code-block:: bash

        salt '*' consul.get_service_status
    '''
    c = _connect()
    index, nodes = c.health.service(name, index, passing)
    node_list = []
    for node in nodes:
        for check in node['Checks']:
            if name == check['ServiceName']:
                node_list.append({check['Node']: check['Status']})
    return node_list
