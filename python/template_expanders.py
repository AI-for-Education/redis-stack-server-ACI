from argparse import ArgumentParser

from common import ROOT, TEM

def gen_ngconf(first=False, **kwargs):
    if first:
        ngfile = TEM / "nginx_template_first.txt"
    else:
        ngfile = TEM / "nginx_template.txt"
    with open(ngfile) as f:
        ngtem = f.read()

    with open(ROOT / "nginx.conf", "w") as f:
        f.write(
            ngtem.format(**kwargs)
        )

def gen_redconf(**kwargs):
    with open(TEM / "redis_template.txt") as f:
        ngtem = f.read()

    with open(ROOT / "redis.conf", "w") as f:
        f.write(
            ngtem.format(**kwargs)
        )

def gen_runfirst(**kwargs):
    with open(TEM / "run_first_template.txt") as f:
        ngtem = f.read()

    with open(ROOT / "run_first.sh", "w", newline="\n") as f:
        f.write(
            ngtem.format(**kwargs)
        )
