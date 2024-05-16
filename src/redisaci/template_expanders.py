from argparse import ArgumentParser

from .common import ROOT, TEM

def gen_ngconf(configfile, first=False, **kwargs):
    if first:
        ngfile = TEM / "nginx_template_first.txt"
    else:
        ngfile = TEM / "nginx_template.txt"
    with open(ngfile) as f:
        ngtem = f.read()

    with open(configfile.parent / "nginx.conf", "w") as f:
        f.write(
            ngtem.format(**kwargs)
        )

def gen_redconf(configfile, **kwargs):
    with open(TEM / "redis_template.txt") as f:
        ngtem = f.read()

    with open(configfile.parent / "redis.conf", "w") as f:
        f.write(
            ngtem.format(**kwargs)
        )

    with open(configfile.parent / "redis_pass.txt", "w") as f:
        f.write(kwargs["PASS"])

def gen_runfirst(configfile, **kwargs):
    with open(TEM / "run_first_template.txt") as f:
        ngtem = f.read()

    with open(configfile.parent / "run_first.sh", "w", newline="\n") as f:
        f.write(
            ngtem.format(**kwargs)
        )
