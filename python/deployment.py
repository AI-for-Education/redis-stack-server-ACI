import subprocess
import json

from common import ROOT, TEM
from load_config import load_conf
from container_registry import get_regcred
from storage_share import get_storecred


def gen_deploy(conf):
    volname = f'{"".join(conf["ACI"]["NAME"].split("-"))}vol'
    kwargs = dict(
        AZURE_LOCATION=conf["ACI"]["LOCATION"],
        APP_NAME=conf["ACI"]["NAME"],
        NAME_OF_CONTAINER=conf["ACR"]["CONTAINER"]["NAME"],
        VERSION=conf["ACR"]["CONTAINER"]["VERSION"],
        NAME_OF_REGISTRY=conf["ACR"]["NAME"],
        VOLUME_NAME=volname,
        CPU=conf["ACI"]["CPU"],
        MEMGB=conf["ACI"]["MEMGB"],
        REG_PASS=get_regcred(**conf["ACR"]),
        FQDN_NAME=conf["ACI"]["DOMAIN"],
        NAME_OF_SHARE=conf["ASA"]["SHARE"],
        NAME_OF_STORAGE=conf["ASA"]["NAME"],
        STORAGE_KEY=get_storecred(**conf["ASA"]),
    )

    with open(TEM / "deployment_template.txt") as f:
        ngtem = f.read()

    with open(ROOT / "deployment.yml", "w") as f:
        f.write(ngtem.format(**kwargs))


def deploy(conf):
    resource_group = conf["ACI"]["RESOURCE_GROUP"]
    name = conf["ACI"]["NAME"]
    deployfile = ROOT / "deployment.yml"
    runstr = (
        "az container create"
        f" --resource-group {resource_group}"
        f" --name {name}"
        f" -f {deployfile.as_posix()}"
    )
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def delete_container(**kwargs):
    runstr = (
        "az container delete"
        " --resource-group {RESOURCE_GROUP}"
        " --name {NAME}"
        " --yes"
    ).format(**kwargs)
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


if __name__ == "__main__":
    conf = load_conf()
    gen_deploy(conf)
