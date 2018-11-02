# VyOS Execution Module

This is a SaltStack execution module to allow basic functionality on a VyOS minion.

For example, you can get the current config back from VyOS like so:

```
salt '*' vyos.get_config
```

> **NOTE**: There was a large API change with regards to salt's internal modules. You'll need to look at https://docs.saltstack.com/en/latest/topics/releases/2018.3.0.html when newer examples don't tend to work because the API has changed significantly. The version of salt-minion on VyOS is currently 2014.1 and has a very different API to the current one.

## Installing

The execution module should be installed in your `file_roots` directory (which matches the environment VyOS is in) so the VyOS minion can get hold of the execution module. Use the `install.sh` script provided and pass it the full path to your `file_roots`

```
[root@bar salt_mod_vyos]$ ./install.sh /srv/salt/state
```

After install, you can add the state to one of your minions in the state `top.sls`. Once you've done that, you will need to synchronise the new vyos execution module and vyos state module which both provide the VyOS configuration management functionality:
```
[root@bar salt_mod_vyos]$ salt 'fw*foo' saltutil.sync_states
fw01-pvlm-foo:
    - states.vyos

[root@bar salt_mod_vyos]$ salt 'fw*foo' saltutil.sync_modules
fw01-pvlm-foo:
    - modules.vyos
```

> **NOTE**: CHANGES TO the module will not take effect until you restart the salt-minion on the target!

Then the module is available:

```
[root@bar salt_mod_vyos]$ salt 'fw*foo' vyos.get_config
fw01-pvlm-foo:
    firewall {
        all-ping enable
        broadcast-ping disable
        config-trap disable
        ipv6-receive-redirects disable
        ipv6-src-route disable
        ip-src-route disable
        log-martians enable
        receive-redirects disable
        ...
```

## State

The state is used to manage the configuration with some example yaml like. The `vyos.managed_config` state piggy-backs the `file.managed` state so the functionality is almost identical. However, the `vyos.managed_config` state also uses the vyos execution module to get and set the config.

```yaml
  - manage_vyos_configuration:
      - vyos.managed_config:
          - name: /config/config.boot.salt
          - source: salt://vyos/config.boot.salt.j2
          - template: jinja
```

Although the managed file has a path, this is merely a temporary file that salt can use in order for the `file.managed` state can use to generate the standard diff functionality.

The file is kept up-to-date with the running config by saving the running configuration to this file before compiling the template and generating a diff. It is imperative therefore to get things like the spacing correct so that when `get_config` is used it matches the configuration file you're already using.

This behaviour may change in the future if it becomes troublesome.
