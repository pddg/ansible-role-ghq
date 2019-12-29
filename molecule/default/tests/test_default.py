import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/usr/local/bin/ghq')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o755


def test_unzip_is_installed(host):
    nginx = host.package("unzip")
    assert nginx.is_installed
