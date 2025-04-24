from __global_paths import *
from prometheus_client import Gauge
import subprocess
import os
import re

metrics = []

verbose = 9

def log(level, text):
    if (verbose >= level):
        print(text)

to_add_basic = [ # Name can only contain a limited character set
    {"Name": "Battery_level",   "Loc": BATTERY_DIR + "charge_now"   },
    {"Name": "Battery_max",     "Loc": BATTERY_DIR + "charge_full"  },
    {"Name": "AC_online",       "Loc": AC_ADAPTER_DIR + "online"    },
]

# basic, single-location reads
for m in to_add_basic:
    name, loc = m["Name"], m["Loc"]
    gauge = Gauge(name, name)
    try:
        with open(loc, 'r') as f:
            val = float(f.read().strip())
        log(10, f"{loc}: {val}")
    except Exception as e:
        log(6, f"Error reading {loc}: {e}")
        val = -1.0
    gauge.set(val)
    metrics.append(gauge)

# thermal zones
for entry in os.listdir(THERMAL_DIR):
    if not entry.startswith("thermal_zone"):
        continue
    temp_path = os.path.join(THERMAL_DIR, entry, "temp")
    if not os.path.isfile(temp_path):
        continue
    gauge = Gauge(f"{entry}_temp", "Temperature in {entry}")
    try:
        with open(temp_path) as f:
            val = f.read().strip()
        log(10, f"{temp_path}: {val}")
        gauge.set(int(val))
    except Exception as e:
        log(6, f"Error reading {temp_path}: {e}")
        gauge.set(-1)
    metrics.append(gauge)

# hwmon sensors
hwmon_re   = re.compile(r'^hwmon\d+$')
sensor_re  = re.compile(r'^(temp\d+_(?:input|max))$')

for entry in os.listdir(FAN2_DIR):
    if not hwmon_re.match(entry):
        continue
    hwmon_path = os.path.join(FAN2_DIR, entry)
    for fname in os.listdir(hwmon_path):
        m = sensor_re.match(fname)
        if not m:
            continue
        full = os.path.join(hwmon_path, fname)
        gauge = Gauge(f"{entry}_{fname}", f"{entry} {fname}")
        try:
            with open(full) as f:
                val = f.read().strip()
            log(10, f"{full}: {val}")
            gauge.set(float(val))
        except Exception as e:
            log(6, f"Error reading {full}: {e}")
            gauge.set(-1)
        metrics.append(gauge)

# # ACPI fans in FAN_DIR
# for entry in os.listdir(FAN_DIR):
#     fan_path   = os.path.join(FAN_DIR, entry)
#     state_file = os.path.join(fan_path, "state")
#     if not os.path.isfile(state_file):
#         continue
# 
#     # two metrics: on/off and actual speed in RPM
#     gauge_on    = Gauge(f"{entry}_on",    f"{entry} running (1=on,0=off)")
#     gauge_rpm   = Gauge(f"{entry}_speed", f"{entry} speed in RPM")
# 
#     try:
#         with open(state_file) as f:
#             for line in f:
#                 # e.g. "state:            on"
#                 if line.startswith("state"):
#                     val = 1 if "on" in line else 0
#                     gauge_on.set(val)
#                 # e.g. "speed:            4000"
#                 elif line.startswith("speed"):
#                     rpm = int(line.split()[1])
#                     gauge_rpm.set(rpm)
#     except Exception as e:
#         log(6, f"Error reading {state_file}: {e}")
#         gauge_on.set(-1)
#         gauge_rpm.set(-1)
# 
#     metrics.extend([gauge_on, gauge_rpm])


log(10, "\n\n\n" + str(metrics))

