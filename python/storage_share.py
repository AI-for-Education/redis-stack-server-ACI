import subprocess
import json

from load_config import load_conf


def gen_storacc(**kwargs):
    runstr = (
        "az storage account create"
        " --resource-group {RESOURCE_GROUP}"
        " --name {NAME}"
        " --location {LOCATION}"
        " --sku Standard_LRS"
    ).format(**kwargs)
    print(runstr.split())
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def gen_storshare(**kwargs):
    runstr = (
        "az storage share create" " --account-name {NAME}" " --name {SHARE}"
    ).format(**kwargs)
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def del_storacc(**kwargs):
    runstr = (
        "az storage account delete"
        " --resource-group {RESOURCE_GROUP}"
        " --name {NAME}"
        " --yes"
    ).format(**kwargs)
    print(runstr.split())
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def get_storecred(**kwargs):
    runstr = (
        "az storage account keys list"
        " --resource-group {RESOURCE_GROUP}"
        " --account-name {NAME}"
    ).format(**kwargs)
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    return json.loads(rc.stdout)[-1]["value"]



if __name__ == "__main__":
    conf = load_conf()
    gen_storacc(**conf["ASA"])
    gen_storshare(**conf["ASA"])
    del_storacc(**conf["ASA"])
