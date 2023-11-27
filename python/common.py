import subprocess
from pathlib import Path

ROOT = Path(__file__).parents[1]
TEM = ROOT / "templates"
CONT = ROOT / "container_scripts"


def az_login():
    subprocess.run(["az", "login"], shell=True, check=True, capture_output=True)
