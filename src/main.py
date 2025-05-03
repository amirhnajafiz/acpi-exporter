#!/usr/bin/env python3
from pathlib import Path
import os, sys, time, yaml
from prometheus_client import Gauge, start_http_server



def load_config():
    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def discover(namespace, subsystem):
    here = Path(__file__).parent  # .../src
    sys.path.insert(0, str(here))
    coll_dir = here / "collectors"

    modules, gauges = {}, {}
    for file in coll_dir.glob("*.py"):
        mod = __import__(f"collectors.{file.stem}", fromlist=["metrics"])
        modules[file.stem] = mod
        for key in mod.metrics().keys():
            if key not in gauges:
                gauges[key] = Gauge(
                    key,
                    f"ACPI metric {key}",
                    namespace=namespace,
                    subsystem=subsystem,
                    labelnames=["collector", "node"],
                )
    return modules, gauges

def update(mods, gauges, node_name):
    for name, mod in mods.items():
        for k, v in mod.metrics().items():
            gauges[k].labels(collector=name, node=node_name).set(v)

def main():
    config = load_config()
    node_name = os.getenv("NODE_NAME", "default_node")

    modules, gauges = discover(config["namespace"], config["subsystem"])
    start_http_server(config["port"])
    print(f"[exporter] Listening on :{config['port']} (interval={config['interval']}s, namespace={config['namespace']}, subsystem={config['subsystem']})")
    while True:
        update(modules, gauges, node_name)
        time.sleep(float(config["interval"]))

if __name__ == "__main__":
    main()
