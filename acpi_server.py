from __global_paths import *
from prometheus_client import Gauge, start_http_server
import os, re, time

# basic single-location metrics
basic = [
    ("Battery_level",   BATTERY_DIR + "charge_now"),
    ("Battery_max",     BATTERY_DIR + "charge_full"),
    ("AC_online",       AC_ADAPTER_DIR + "online"),
]

# thermal_zones
thermal_sensors = []
try:
    for d in os.listdir(THERMAL_DIR):
        p = os.path.join(THERMAL_DIR, d, "temp")
        if d.startswith("thermal_zone") and os.path.isfile(p):
            thermal_sensors.append((f"{d}_temp", p))
except:
    pass

# hwmons
hwmon_re  = re.compile(r'^hwmon\d+$')
sensor_re = re.compile(r'^(temp\d+_(?:input|max))$')
hwmon_sensors = []
try:
    for d in os.listdir(FAN2_DIR):
        if hwmon_re.match(d):
            base = os.path.join(FAN2_DIR, d)
            for fname in os.listdir(base):
                if sensor_re.match(fname):
                    hwmon_sensors.append((f"{d}_{fname}", os.path.join(base, fname)))
except:
    pass

# acpi fans
acpi_sensors = []
try:
    for d in os.listdir(FAN_DIR):
        p = os.path.join(FAN_DIR, d, "state")
        if os.path.isfile(p):
            acpi_sensors.append((d, p))
except:
    pass

# create all Gauges once
gauges = {}
for name, _ in basic + thermal_sensors + hwmon_sensors:
    gauges[name] = Gauge(name, name)

# for ACPI we need two per fan
for d, _ in acpi_sensors:
    gauges[f"{d}_on"]    = Gauge(f"{d}_on",    f"{d} on/off")
    gauges[f"{d}_speed"] = Gauge(f"{d}_speed", f"{d} RPM")

start_http_server(8000)

def update_all():
    # basic
    for name, path in basic:
        try:
            val = float(open(path).read().strip())
        except:
            val = -1.0
        gauges[name].set(val)

    # thermal
    for name, path in thermal_sensors:
        try:
            gauges[name].set(int(open(path).read().strip()))
        except:
            gauges[name].set(-1)

    # hwmon
    for name, path in hwmon_sensors:
        try:
            gauges[name].set(float(open(path).read().strip()))
        except:
            gauges[name].set(-1)

    # acpi
    for fan, state_path in acpi_sensors:
        on, speed = -1, -1
        try:
            for line in open(state_path):
                if line.startswith("state"):
                    on = 1 if "on" in line else 0
                elif line.startswith("speed"):
                    speed = int(line.split()[1])
        except:
            pass
        gauges[f"{fan}_on"].set(on)
        gauges[f"{fan}_speed"].set(speed)

if __name__ == "__main__":
    while True:
        update_all()
        time.sleep(10)

