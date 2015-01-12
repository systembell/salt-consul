# salt-consul
Consul modules for SaltStack

## Prerequisites

`python-consul` is a requisite for these modules.


Execution module example:

`salt-call consul.key_put foo bar`

`salt-call consul.key_get foo`

`salt-call consul.key_delete foo`


State module example:

```
consul-key-present:
    consul_kv.present:
        - name: foo
        - value: bar
```