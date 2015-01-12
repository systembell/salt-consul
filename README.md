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

#### Checks

`salt-call consul.check_list`

`salt-call consul.check_get foo`

`salt-call consul.check_register name=foo script=/path/to/script interval=10s`

`salt-call consul.check_deregister name=foo`

### State module examples:

#### Key/Value

```yaml
consul-key-present:
    consul_kv.present:
        - name: foo
        - value: bar

consul-key-absent:
    consul_kv.absent:
        - name: foo
```

#### Services

```yaml
consul-service-present:
    consul_service.present:
        - name: foo
        - port: 6969
        - script: nc -z localhost 6969
        - interval: 10s

consul-service-absent:
    consul_service.absent:
        - name: foo
```

#### Checks

```yaml
consul-check-present:
    consul_check.present:
        - name: foo
        - script: nz -z localhost 6969
        - interval: 10s

consul-check-absent:
    consul_check.absent:
        - name: foo
```

## TODO

- service / check registration
- health status monitoring


