from __global_paths import *
from prometheus_client import Gauge
import subprocess

metrics = []

verbose = 9

def log(level, text):
    if (verbose >= level):
        print(text)

to_add_basic = [ # Name can only contain a limited character set
    {"Name": "Battery_level",   "Loc": BATTERY_DIR + "charge_now"   },
    {"Name": "Battery_max",     "Loc": BATTERY_DIR + "charge_full"    },
]

for metric in to_add_basic:
    name = metric["Name"]
    location = metric["Loc"]
    gauge = Gauge(name, "")
    res = subprocess.run(f"cat {location}", shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log(10, res)
    if res.returncode != 0:
        log(10, f"Error occurred: {res.stderr}")
        gauge.set(float(res.stdout))
    else:
        log(10, f"Output: {res.stdout}")
        gauge.set(-1)
    metrics.append(gauge)

log(10, metrics)

