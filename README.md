# salt-consul
Consul modules for SaltStack

## Background
I'd been meaning to write this for awhile, then one afternoon just decided I didn't want to lay down json for every service & check, not to mention reload the service. Still a work in progress, but most of the functions I use are represented here.

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

#### Nodes

`salt-call consul.node_list`

`salt-call consul.node_get foo`

#### ttls

`salt-call consul.ttl_pass foo type=service notes=bar`

`salt-call consul.ttl_fail foo type=check notes=bar`

`salt-call consul.ttl_warn foo notes=bar`




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

#### ttls

```yaml
consul-set-service-ttl:
    consul_service.ttl_set:
        - name: foo
        - status: failing
        - notes: bar

consul-set-check-ttl:
    consul_check.ttl_set:
        - name: foo
        - status: failing
        - notes: bar
```


## TODO

- acls

## Contributing
- fork
- code
- submit pr


