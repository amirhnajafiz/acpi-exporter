import logging
import os
from prometheus_client import Gauge
from .collector import Collector

class PowerCollector(Collector):
    """
    Power collector for gathering system power usage metrics.
    This collector may use platform-specific methods (e.g., reading from /sys/class/powercap on Linux).
    """

    def __init__(self, exec_info: bool, namespace: str, subsystem: str, **labels):
        self.labels = labels
        self.exec_info = exec_info
        
        label_names = list(labels.keys()) + ["source"]
        self.power_watts_gauge = Gauge(
            "power_usage_watts",
            "System power usage in Watts",
            namespace=namespace,
            subsystem=subsystem,
            labelnames=label_names,
        )

    def collect(self):
        try:
            power_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
            if os.path.exists(power_path):
                with open(power_path) as f:
                    energy_uj = int(f.read())
                self.power_watts_gauge.labels(**self.labels, source="rapl").set(energy_uj)
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting power data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting power data")
