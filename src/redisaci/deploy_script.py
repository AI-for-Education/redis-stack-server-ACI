from argparse import ArgumentParser
import os
import time
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from .load_config import load_conf
from .template_expanders import gen_runfirst, gen_redconf, gen_ngconf
from .container_registry import gen_contreg
from .storage_share import gen_storacc, gen_storshare
from .deployment import gen_deploy, deploy, delete_container
from .dockers import build_docker, push_docker, check_for_docker
from .resource_group import gen_reggroup, delete_reggroup

from .common import az_login, ROOT, COPYLIST, CLEANLIST


def first(configfile, dry_run=False):
    conf = load_conf(configfile)
    ##
    gen_runfirst(configfile, **conf["ACI"])
    gen_redconf(configfile, PASS=os.environ.get("REDIS_KEY", ""), **conf["ACI"])
    gen_ngconf(configfile, **conf["ACI"], first=True)
    ##
    if not dry_run:
        gen_reggroup(**conf["GLOBAL"])
        gen_contreg(**conf["ACR"])
        ##
        gen_storacc(**conf["ASA"])
        gen_storshare(**conf["ASA"])
        ##
        gen_deploy(configfile, conf)
        ##
        build_docker(configfile, conf, first=True)
        push_docker(conf)
        ##
        deploy(configfile, conf)
        ##
        clean_files(configfile)


def final(configfile, dry_run=False):
    ##
    conf = load_conf(configfile)
    ##
    redpass = os.environ.get("REDIS_KEY", "")
    if len(redpass) == 0:
        redpass = secrets.token_urlsafe(16)
    gen_redconf(configfile, PASS=redpass, **conf["ACI"])
    gen_ngconf(configfile, **conf["ACI"], first=False)
    gen_deploy(configfile, conf)
    ##
    if not dry_run:
        clean_container_instance(configfile)
        ##
        build_docker(configfile, conf, rediskey=redpass, first=False)
        push_docker(conf)
        ##
        deploy(configfile, conf)
        ##
        clean_files(configfile)


def clean_files(configfile):
    for cleanfile in [*CLEANLIST, *COPYLIST]:
        (configfile.parent / cleanfile).unlink(missing_ok=True)


def clean_container_instance(configfile):
    conf = load_conf(configfile)
    delete_container(**conf["ACI"])


def clean_all(configfile):
    conf = load_conf(configfile)
    clean_files(configfile)
    delete_reggroup(**conf["ACI"])


def runner(opt):
    opt.config = Path(opt.config).resolve()
    if not opt.config.exists():
        raise OSError("Can''t find config file")
    
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
        clean_all(opt.config)
        return

    if opt.clean_files:
        clean_files(opt.config)
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
        first(opt.config, dry_run=opt.dry_run)
        if opt.final:
            conf = load_conf(opt.config)
            print("Waiting for SSL cert...")
            time.sleep(conf["GLOBAL"]["SLEEP"] + 60)
            print("Done")

    if opt.final:
        final(opt.config, dry_run=opt.dry_run)

def main():
    parser = ArgumentParser()
    parser.add_argument("--config", required=True, type=str)
    parser.add_argument("--first", action="store_true")
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--clean-files", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    opt = parser.parse_args()
    runner(opt)
    
if __name__ == "__main__":
    main()
    
