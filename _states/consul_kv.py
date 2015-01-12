# -*- coding: utf-8 -*-
'''
Management of consul server
==========================

.. versionadded:: 2014.7.0

:depends:   - consul Python module
:configuration: See :py:mod:`salt.modules.consul` for setup instructions.

.. code-block:: yaml

    key_in_consul:
      consul_kv.present:
        - value: data

The consul server information specified in the minion config file can be
overridden in states using the following arguments: ``host``, ``port``, ``token``,
``consistency``.

.. code-block:: yaml


    key_in_consul:
      consul_kv.present:
        - value: data
        - host: localhost
        - port: 8500
        - token: None
        - consistency: 'default'
'''

__virtualname__ = 'consul_kv'


def __virtual__():
    '''
    Only load if the consul module is in __salt__
    '''
    if 'consul.key_put' in __salt__:
        return __virtualname__
    return False


def present(name, value):
    '''
    Ensure that the named key exists in consul with the value specified

    name
        consul key to manage

    value
        Data to persist in key
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Key already set to defined value'}

    if not __salt__['consul.key_get'](name):
        __salt__['consul.key_put'](name, value)
        ret['changes'][name] = 'Key created'
        ret['comment'] = 'Key "%s" set with value "%s"' % (name, value)

    elif __salt__['consul.key_get'](name) != value:
        __salt__['consul.key_put'](name, value)
        ret['changes'][name] = 'Value updated'
        ret['comment'] = 'Key "%s" updated with value "%s"' % (name, value)
    
    return ret


def absent(name, recurse=False):
    '''
    Ensure that the named key does not exist in consul 

    name
        consul key to manage

    value
        Data to persist in key
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Key(s) specified already absent'}

    if not __salt__['consul.key_get'](name):
        ret['comment'] = 'Key "%s" does not exist' % (name)

    else:
        __salt__['consul.key_delete'](name)
        ret['changes'][name] = 'Value updated'
        ret['comment'] = 'Key "%s" deleted' % (name)
    
    return ret