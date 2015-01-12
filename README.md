# salt-consul
Consul modules for SaltStack

## Prerequisites

`python-consul` is a requisite for these modules.


### Execution module examples:

#### Key/Value

`salt-call consul.key_put foo bar`

`salt-call consul.key_get foo`

`salt-call consul.key_delete foo`

#### Services

`salt-call consul.service_list`

`salt-call consul.service_get foo`

`salt-call consul.service_register name=foo port=6969 script=/path/to/script interval=10s`

`salt-call consul.service_deregister name=foo`

### State module examples:

#### Key/Value

```
consul-key-present:
    consul_kv.present:
        - name: foo
        - value: bar
```

## TODO

- service / check registration
- health status monitoring


