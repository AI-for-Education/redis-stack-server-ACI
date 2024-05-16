import yaml

from .common import ROOT, TEM

def load_conf(configfile):
    if not configfile.exists():
        raise ValueError(f"{str(configfile)} doesn't exist")

    with open(configfile) as f:
        conf = yaml.safe_load(f)
    
    globald = conf.get("GLOBAL", {})
    for d in conf.values():
        for k, v in globald.items():
            d[k] = v
    if conf["ACI"].get("DOMAIN") is None:
        conf["ACI"]["DOMAIN"] = conf["ACI"]["NAME"]
        
    return conf