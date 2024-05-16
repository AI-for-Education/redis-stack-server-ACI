import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
TEM = ROOT / "templates"
CONT = ROOT / "container_scripts"

CLEANLIST = ["deployment.yml", "nginx.conf", "redis.conf", "run_first.sh"]
COPYLIST = ["run.sh", "refresh_cert.sh"]


def az_login():
    rc = subprocess.run(["az", "login"], shell=True, check=True, capture_output=True)
    print(rc.stdout)
    print(rc.stderr)
