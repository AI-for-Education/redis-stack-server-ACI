import subprocess
import json

from load_config import load_conf


def gen_contreg(**kwargs):
    runstr = (
        "az acr create"
        " --resource-group {RESOURCE_GROUP}"
        " --name {NAME}"
        " --location {LOCATION}"
        " --sku Basic"
    ).format(**kwargs)
    print(runstr.split())
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def del_contreg(**kwargs):
    runstr = (
        "az acr delete" " --resource-group {RESOURCE_GROUP}" " --name {NAME}" " --yes"
    ).format(**kwargs)
    print(runstr.split())
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def get_regcred(**kwargs):
    runstr = ("az acr update" " --name {NAME}" " --admin-enabled true").format(**kwargs)
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    runstr = ("az acr credential show" " --name {NAME}").format(**kwargs)
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    return json.loads(rc.stdout)["passwords"][-1]["value"]

if __name__ == "__main__":
    conf = load_conf()
    gen_contreg(**conf["ACR"])
    del_contreg(**conf["ACR"])
