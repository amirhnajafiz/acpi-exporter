#!/usr/bin/env python3
from pathlib import Path
import os, sys, argparse, time
from prometheus_client import Gauge, start_http_server



def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--interval", type=int, default=5)
    p.add_argument("--namespace", type=str, default="ACPI")
    p.add_argument("--subsystem", type=str, default="EXPT")
    return p.parse_args()

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
    args = parse_args()
    node_name = os.getenv("NODE_NAME", "default_node")

    modules, gauges = discover(args.namespace, args.subsystem)
    start_http_server(args.port)
    print(f"[exporter] Listening on :{args.port} (interval={args.interval}s, namespace={args.namespace}, subsystem={args.subsystem})")
    while True:
        update(modules, gauges, node_name)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
