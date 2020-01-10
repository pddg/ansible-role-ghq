# pddg.ghq

[![Actions Status](https://github.com/pddg/ansible-role-ghq/workflows/Test/badge.svg)](https://github.com/pddg/ansible-role-ghq/actions)

The role to install ghq ( https://github.com/motemen/ghq )

## Requirements

If you want to use this role on macOS and `ghq_install_by_brew: yes`, this will require that Homebrew is installed.

## Role Variables

See [defaults/main.yml](defaults/main.yml)

## Dependencies

No other dependencies

## Example Playbook

```yaml
- hosts: servers
  roles:
    - name: pddg.ghq
      become: yes
      vars:
        ghq_install_dir: /usr/local/bin
        ghq_version: 1.0.1
```

## License

Apache 2.0 Software License

## Author Information

pddg

