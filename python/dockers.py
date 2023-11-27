import platform
import subprocess
import json
import os

from common import ROOT, CONT
from load_config import load_conf

PLATSTR = platform.system()


def build_docker(conf, first=False):
    imagename = conf["ACR"]["CONTAINER"]["NAME"]
    imagever = conf["ACR"]["CONTAINER"]["VERSION"]
    rediskey = os.environ.get("REDIS_KEY", "")

    if PLATSTR == "Windows":
        exec = (CONT / "build_image.bat").as_posix()
    elif PLATSTR == "Linux":
        exec = (CONT / "build_image.sh").as_posix()
    else:
        raise NotImplementedError("Only Windows and Linux are supported")
    if first:
        dockerfile = (ROOT / "Dockerfile_first").as_posix()
    else:
        dockerfile = (ROOT / "Dockerfile").as_posix()
    runstr = f"{exec} {imagename} {imagever} {dockerfile} {rediskey}"
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    # print(rc.stdout)
    # else:
    #     print(json.dumps(json.loads(rc.stderr), indent=4))


def push_docker(conf):
    regname = conf["ACR"]["NAME"]
    imagename = conf["ACR"]["CONTAINER"]["NAME"]
    imagever = conf["ACR"]["CONTAINER"]["VERSION"]
    if PLATSTR == "Windows":
        exec = (CONT / "push_image.bat").as_posix()
    elif PLATSTR == "Linux":
        exec = (CONT / "push_image.sh").as_posix()
    else:
        raise NotImplementedError("Only Windows and Linux are supported")
    runstr = f"{exec} {regname} {imagename} {imagever}"
    print(runstr.split())
    rc = subprocess.run(runstr.split(), shell=True, check=True, capture_output=True)
    print(rc.stderr)


if __name__ == "__main__":
    conf = load_conf()
    build_docker(conf, False)
