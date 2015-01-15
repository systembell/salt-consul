# -*- coding: utf-8 -*-
'''
Management of consul checks
==========================

:maintainer: Aaron Bell <aarontbellgmail.com>
:maturity: new
:depends:    - python-consul (http://python-consul.readthedocs.org/en/latest/)
:platform: Linux

.. versionadded:: 2014.7.0

:depends:   - consul Python module
:configuration: See :py:mod:`salt.modules.consul` for setup instructions.

.. code-block:: yaml

    check_in_consul:
        consul_check.present:
            - name: foo
            - script: nc -z localhost 6969
            - interval: 10s

    check_not_in_consul:
        consul_check.absent:
            - name: foo

'''

__virtualname__ = 'consul_check'


def __virtual__():
    '''
    Only load if the consul module is in __salt__
    '''
    if 'consul.key_put' in __salt__:
        return __virtualname__
    return False


def present(name, check_id=None, script=None, interval=None, ttl=None, notes=None):
    '''
    Ensure the named check is present in Consul

    name
        consul check to manage

    check_id
        alternative check id

    script + interval
        path to script for health checks, paired with invocation interval

    ttl
        ttl for status

    notes
        not used internally by consul, meant to be human-readable

    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Check "%s" updated' % (name)}

    if not __salt__['consul.check_get'](name):
        __salt__['consul.check_register'](name, check_id, script, interval, ttl, notes)
        ret['changes'][name] = 'Check created'
        ret['comment'] = 'Check "%s" created' % (name)

    else:
        __salt__['consul.check_register'](name, check_id, script, interval, ttl, notes)
    
    return ret


def absent(name):
    '''
    Ensure the named check is absent in Consul

    name
        consul check to manage
        
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Check "%s" removed' % (name)}

    if not __salt__['consul.check_get'](name):
        ret['comment'] = 'Check "%s" already absent' % (name)

    else:
        __salt__['consul.check_deregister'](name)
    
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

    type = 'check'

    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Check set to %s' % (status)}

    statuses = ['passing', 'warning', 'failing']

    if not __salt__['consul.service_get'](name):
        ret['comment'] = 'Check does not exist' % (name)

    if status not in statuses:
        ret['result'] = False
        ret['comment'] = 'Check must be one of: %s' % (" ".join(s))
        
    else:
        __salt__['consul.ttl_' + status[:-3] ](name, type, notes)
    
    return ret
    