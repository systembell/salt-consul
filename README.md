# salt-consul
Consul modules for SaltStack

## Quickstart

- drop the modules into `{_modules,_states}` into `file_roots` on your `salt-master`
- ensure the pypi `python-consul` package is installed


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

`salt-call consul.get_service_status name=foo`

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

- include access to all api functions in python-consul
- ttls
- acls

## Contributing
- fork
- code
- submit pr


