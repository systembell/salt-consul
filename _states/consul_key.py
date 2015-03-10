# -*- coding: utf-8 -*-
'''
Management of consul key/value
==========================

:maintainer: Aaron Bell <aarontbellgmail.com>
:maturity: new
:depends:    - python-consul (http://python-consul.readthedocs.org/en/latest/)
:platform: Linux

.. versionadded:: 2014.7.0

:depends:   - consul Python module
:configuration: See :py:mod:`salt.modules.consul` for setup instructions.

.. code-block:: yaml

    key_in_consul:
        consul_key.present:
            - name: foo
            - value: data

The consul server information in the minion config file can be
overridden in states using the following arguments: ``host``, ``post``, ``consistency``,
``password``.
.. code-block:: yaml
    key_in_consul:
      consul_key.present:
        - name: foo
        - value: bar
        - host: hostname.consul
        - port: 6969
'''

__virtualname__ = 'consul_key'

import os
import salt.utils

def __virtual__():
    '''
    Only load if the consul module is in __salt__
    '''
    if 'consul.key_put' in __salt__:
        return __virtualname__
    return False


def present(name, value, value_from_file=False, **kwargs):
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

    if value_from_file:
        if not os.path.isfile(value):
            ret = {}
            ret['result'] = False
            ret['comment'] = value + " does not exist"
            return ret
        
        if not salt.utils.istextfile(value):
            ret = {}
            ret['result'] = False
            ret['comment'] = value + " is not a text file"
            return ret

        should = open(value,'r').read()
    else:
        should = value

    if not __salt__['consul.key_get'](name, **kwargs):
        __salt__['consul.key_put'](name, value, value_from_file, **kwargs)
        ret['changes'][name] = 'Key created'
        ret['comment'] = 'Key "%s" set with value "%s"' % (name, value)

    elif __salt__['consul.key_get'](name, **kwargs) != should:
        __salt__['consul.key_put'](name, value, value_from_file, **kwargs)
        ret['changes'][name] = 'Value updated'
        ret['comment'] = 'Key "%s" updated with value "%s"' % (name, value)
    
    return ret


def absent(name, recurse=False, **kwargs):
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

    if not __salt__['consul.key_get'](name, **kwargs):
        ret['comment'] = 'Key "%s" does not exist' % (name)

    else:
        __salt__['consul.key_delete'](name, **kwargs)
        ret['changes'][name] = 'Value updated'
        ret['comment'] = 'Key "%s" deleted' % (name)
    
    return ret
