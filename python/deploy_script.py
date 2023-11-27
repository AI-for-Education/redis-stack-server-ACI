from argparse import ArgumentParser
import os
import time

from dotenv import load_dotenv

load_dotenv()

from load_config import load_conf
from template_expanders import gen_runfirst, gen_redconf, gen_ngconf
from container_registry import gen_contreg
from storage_share import gen_storacc, gen_storshare
from deployment import gen_deploy, deploy, delete_container
from dockers import build_docker, push_docker, check_for_docker
from resource_group import gen_reggroup, delete_reggroup

from common import az_login, ROOT

CLEANLIST = ["deployment.yml", "nginx.conf", "redis.conf", "run_first.sh"]


def first(dry_run=False):
    conf = load_conf()
    ##
    gen_runfirst(**conf["ACI"])
    gen_redconf(PASS=os.environ.get("REDIS_KEY", ""), **conf["ACI"])
    gen_ngconf(**conf["ACI"], first=True)
    ##
    if not dry_run:
        gen_reggroup(**conf["GLOBAL"])
        gen_contreg(**conf["ACR"])
        ##
        gen_storacc(**conf["ASA"])
        gen_storshare(**conf["ASA"])
        ##
        gen_deploy(conf)
        ##
        build_docker(conf, first=True)
        push_docker(conf)
        ##
        deploy(conf)
        ##
        clean_files()


def final(dry_run=False):
    ##
    conf = load_conf()
    ##
    gen_redconf(PASS=os.environ.get("REDIS_KEY", ""), **conf["ACI"])
    gen_ngconf(**conf["ACI"], first=False)
    gen_deploy(conf)
    ##
    if not dry_run:
        clean_container_instance()
        ##
        build_docker(conf, first=False)
        push_docker(conf)
        ##
        deploy(conf)
        ##
        clean_files()


def clean_files():
    for cleanfile in CLEANLIST:
        (ROOT / cleanfile).unlink(missing_ok=True)


def clean_container_instance():
    conf = load_conf()
    delete_container(**conf["ACI"])


def clean_all():
    conf = load_conf()
    clean_files()
    delete_reggroup(**conf["ACI"])


def main(opt):
    if opt.full:
        opt.first = True
        opt.final = True

    if opt.clean or opt.clean_files:
        if opt.first or opt.final:
            raise ValueError(
                "If '--clean' or '--clean-files' can't also be 'first', 'final', or 'full'"
            )

    if opt.clean:
        az_login()
        clean_all()
        return

    if opt.clean_files:
        clean_files()
        return

    if (opt.first or opt.final) and not opt.dry_run:
        if not check_for_docker():
            print(
                "\nDocker doesn't appear to be running."
                " Check that you have docker installed and it is running.\n"
            )
            return
        az_login()

    if opt.first:
        first(dry_run=opt.dry_run)
        if opt.final:
            print("Waiting for SSL cert...")
            time.sleep(360)
            print("Done")

    if opt.final:
        final(dry_run=opt.dry_run)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--clean-files", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    opt = parser.parse_args()
    main(opt)
