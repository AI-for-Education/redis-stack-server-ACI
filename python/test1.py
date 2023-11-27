import time
import os

from dotenv import load_dotenv
load_dotenv()

from load_config import load_conf
from template_expanders import gen_rf, gen_redconf, gen_ngconf
from container_registry import gen_contreg
from storage_share import gen_storacc, gen_storshare
from deployment import gen_deploy, deploy, delete_container
from dockers import build_docker, push_docker
from resource_group import gen_reggroup

conf = load_conf()

gen_reggroup(**conf["GLOBAL"])

gen_rf(**conf["ACI"])
gen_contreg(**conf["ACR"])
gen_redconf(PASS=os.environ.get("REDIS_KEY", ""), **conf["ACI"])
gen_ngconf(**conf["ACI"], first=True)
gen_storacc(**conf["ASA"])
gen_storshare(**conf["ASA"])
gen_deploy(conf)

build_docker(conf, first=True)
push_docker(conf)

deploy(conf)

print("Waiting for SSL cert...")
time.sleep(360)
print("Done")

delete_container(conf)

gen_ngconf(**conf["ACI"], first=False)
build_docker(conf, first=False)
push_docker(conf)
deploy(conf)