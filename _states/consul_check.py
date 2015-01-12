# -*- coding: utf-8 -*-
'''
Management of consul server
==========================

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
    