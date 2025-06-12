import os
import time
from prometheus_client import Gauge
from .collector import Collector

class CPUPowerCollector(Collector):
    """
    Collector for CPU package power usage (Watts).
    """

    def __init__(self, namespace: str, subsystem: str, **labels):
        self.labels = labels
        
        self.cpu_power_gauge = Gauge(
            "cpu_power_watts", 
            "CPU package power usage in Watts", 
            namespace=namespace,
            subsystem=subsystem,
            labelnames=list(labels.keys()),
        )
        
        self.last_energy = None
        self.last_time = None

    def collect(self):
        energy_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
        if os.path.exists(energy_path):
            with open(energy_path) as f:
                energy_uj = int(f.read())
            now = time.time()
            if self.last_energy is not None and self.last_time is not None:
                delta_e = energy_uj - self.last_energy
                delta_t = now - self.last_time
                if delta_t > 0:
                    watts = (delta_e / 1_000_000) / delta_t
                    self.cpu_power_gauge.labels(**self.labels).set(watts)
            self.last_energy = energy_uj
            self.last_time = now
