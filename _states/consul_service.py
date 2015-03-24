# -*- coding: utf-8 -*-
'''
Management of consul services
==========================

:maintainer: Aaron Bell <aarontbellgmail.com>
:maturity: new
:depends:    - python-consul (http://python-consul.readthedocs.org/en/latest/)
:platform: Linux`

.. versionadded:: 2014.7.0

:depends:   - consul Python module
:configuration: See :py:mod:`salt.modules.consul` for setup instructions.

.. code-block:: yaml

    service_in_consul:
        consul_service.present:
            - name: foo
            - port: 6969
            - script: nc -z localhost 6969
            - interval: 10s

    service_not_in_consul:
        consul_service.absent:
            - name: foo

    ttl_status_set:
        consul_service.ttl_set:
            - name: foo
            - status: passing
            - notes: bar

'''

__virtualname__ = 'consul_service'


def __virtual__():
    '''
    Only load if the consul module is in __salt__
    '''
    if 'consul.key_put' in __salt__:
        return __virtualname__
    return False


def present(name, service_id=None, port=None, tags=None, script=None, interval=None, ttl=None):
    '''
    Ensure the named service is present in Consul

    name
        consul service to manage

    service_id
        alternative service id

    port
        service port

    tags
        list of tags to associate with this service

    script + interval
        path to script for health checks, paired with invocation interval

    ttl
        length of time a service should remain healthy before being updated
        note: if this is specified, script + interval must not be used        
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service "%s" updated' % (name)}

    if not __salt__['consul.service_get'](name, service_id):
        __salt__['consul.service_register'](name, service_id, port, tags, script, interval, ttl)
        ret['changes'][name] = 'Service created'
        ret['comment'] = 'Service "%s" created' % (name)

    else:
        __salt__['consul.service_register'](name, service_id, port, tags, script, interval, ttl)
    
    return ret


def absent(name):
    '''
    Ensure the named service is absent in Consul

    name
        consul service to manage
        
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service "%s" removed' % (name)}

    if not __salt__['consul.service_get'](name):
        ret['comment'] = 'Service "%s" already absent' % (name)

    else:
        __salt__['consul.service_deregister'](name)
    
    return ret


def ttl_set(name, status, notes=None):
    '''
    Update a ttl-based service check to either passing, warning, or failing

    name
        consul service to manage

    status
        passing, warning, or failing

    notes
        optional notes for operators
        
    '''

    type = 'service'

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service set to %s' % (status)}

    statuses = ['passing', 'warning', 'failing']

    if not __salt__['consul.service_get'](name):
        ret['comment'] = 'Service does not exist' % (name)

    if status not in statuses:
        ret['result'] = False
        ret['comment'] = 'Status must be one of: %s' % (" ".join(s))
        
    else:
        __salt__['consul.ttl_' + status[:-3] ](name, type, notes)
    
    return ret

