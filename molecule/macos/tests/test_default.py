import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_ghq_is_installed(host):
    f = host.file('/usr/local/bin/ghq')

    assert f.exists
    assert f.user == 'root'
    assert f.mode == 0o755


def test_ghq_executable(host):
    ghq_ver = host.run("ghq --version")

    assert ghq_ver.succeeded
    # ghq version 1.0.1 (rev:91944fb)
    actual_ver = ghq_ver.stdout.strip().split(" ")[2]
    expected_ver = host.ansible.get_variables().get("ghq_version")
    assert actual_ver == str(expected_ver)
