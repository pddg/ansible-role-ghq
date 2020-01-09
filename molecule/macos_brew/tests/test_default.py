import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_ghq_is_installed(host):
    f = host.file('/usr/local/bin/ghq')

    assert f.exists
    assert f.user == os.getenv('USER')
    assert f.is_symlink
    # assert f.mode == 0o755


def test_ghq_executable(host):
    host.run_test("ghq --version")
