import platform
import subprocess
import json
import os
from shutil import copyfile

from .common import ROOT, CONT, COPYLIST
from .load_config import load_conf

PLATSTR = platform.system()


def build_docker(configfile, conf, rediskey, first=False):
    imagename = conf["ACR"]["CONTAINER"]["NAME"]
    imagever = conf["ACR"]["CONTAINER"]["VERSION"]
    rediskey = rediskey

    if PLATSTR == "Windows":
        exec = (CONT / "build_image.bat").as_posix()
    elif PLATSTR == "Linux":
        exec = (CONT / "build_image.sh").as_posix()
    else:
        raise NotImplementedError("Only Windows and Linux are supported")
    if first:
        dockerfile = (ROOT / "Dockerfile_first").as_posix()
    else:
        for file in COPYLIST:
            infile = ROOT / file
            outfile = configfile.parent / file
            ### force LF on .sh files
            if infile.suffix == ".sh":
                with open(infile) as fin, open(outfile, "w", newline="\n") as fout:
                    fout.write(fin.read())
            else:
                copyfile(infile, outfile)
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
    # print(rc.stderr)


def check_for_docker():
    try:
        subprocess.run(["docker", "info"], shell=True, check=True, capture_output=True)
        return True
    except:
        return False
