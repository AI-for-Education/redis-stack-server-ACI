import yaml

from common import ROOT, TEM

def load_conf():
    conffile = ROOT / "config.yml"
    if not conffile.exists():
        raise ValueError(f"{str(conffile)} doesn't exist")

    with open(conffile) as f:
        conf = yaml.safe_load(f)
    
    globald = conf.get("GLOBAL", {})
    for d in conf.values():
        for k, v in globald.items():
            d[k] = v
    if conf["ACI"].get("DOMAIN") is None:
        conf["ACI"]["DOMAIN"] = conf["ACI"]["NAME"]
        
    return conf

if __name__ == "__main__":
    print(load_conf())