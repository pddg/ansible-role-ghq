import os

import pytest
import testinfra.utils.ansible_runner
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


@pytest.fixture(scope='module')
def ansible_vars(host):
    """
    Return a dict of the variable defined in the role tested or the inventory.
    Ansible variable precedence is respected.
    """
    var_files = [
        "../../defaults/main.yml",
        "../../vars/main.yml",
        "./vars.yml"
    ]
    facts = host.ansible("setup", "filter=ansible_system")["ansible_facts"]
    templar = Templar(loader=DataLoader())
    all_vars = facts
    for f in var_files:
        var_from_f = host.ansible(
            "include_vars", f"file={f}")["ansible_facts"]
        for key, val in var_from_f.items():
            templar.available_variables = all_vars
            all_vars[key] = templar.template(val)
    return all_vars


def test_hosts_file(host, ansible_vars):
    install_dir = ansible_vars.get('ghq_install_dir')
    f = host.file(os.path.join(install_dir, 'ghq'))

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o755


def test_unzip_is_installed(host):
    unzip = host.package("unzip")
    assert unzip.is_installed


def test_ghq_executable(host, ansible_vars):
    ghq_ver = host.run("ghq --version")

    assert ghq_ver.succeeded
    # ghq version 1.0.1 (rev:91944fb)
    actual_ver = ghq_ver.stdout.strip().split(" ")[2]
    expected_ver = ansible_vars.get("ghq_version")
    assert actual_ver == str(expected_ver)
