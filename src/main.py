#!/usr/bin/env python3
from pathlib import Path
import sys, argparse, time, subprocess
from prometheus_client import Gauge, start_http_server

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--interval", type=int, default=5)
    return p.parse_args()

def discover():
    here = Path(__file__).parent # .../src
    sys.path.insert(0, str(here))
    coll_dir = here / "collectors"

    modules, all_keys = {}, set()
    for file in coll_dir.glob("*.py"):
        mod = __import__(f"collectors.{file.stem}", fromlist=["metrics"])
        modules[file.stem] = mod
        all_keys.update(mod.metrics().keys())

    gauges = {k: Gauge(k, f"ACPI metric {k}") for k in all_keys}
    return modules, gauges

def update(mods, gauges):
    for m in mods.values():
        for k, v in m.metrics().items():
            gauges[k].set(v)

def main():
    args = parse_args()

    modules, gauges = discover()
    start_http_server(args.port)
    print(f"[exporter] Listening on :{args.port}  (interval={args.interval}s)")
    while True:
        update(modules, gauges)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

