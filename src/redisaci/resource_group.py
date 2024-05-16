import subprocess


def gen_reggroup(**kwargs):
    runstr = (
        "az group create" " --name {RESOURCE_GROUP}" " --location {LOCATION}"
    ).format(**kwargs)
    print(runstr.split())
    subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)


def delete_reggroup(**kwargs):
    runstr = ("az group delete" " --name {RESOURCE_GROUP} --yes").format(**kwargs)
    print(runstr.split())
    try:
        subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    except:
        pass

