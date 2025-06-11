import logging
import os
from prometheus_client import Gauge

from .collector import Collector

class PowerCollector(Collector):
    """
    Power collector for gathering system power usage metrics.
    This collector may use platform-specific methods (e.g., reading from /sys/class/powercap on Linux).
    """

    def __init__(self, **labels):
        self.labels = labels
        label_names = list(labels.keys()) + ["source"]
        self.power_watts_gauge = Gauge(
            "power_usage_watts", "System power usage in Watts", labelnames=label_names
        )

    def collect(self):
        try:
            # Example for Linux systems with RAPL interface
            # You may need to adjust the path or use a library for other platforms
            power_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
            if os.path.exists(power_path):
                with open(power_path) as f:
                    energy_uj = int(f.read())
                # Convert microjoules to watts (requires time delta, so this is a placeholder)
                # You'd need to store previous value and timestamp to compute actual power
                self.power_watts_gauge.labels(**self.labels, source="rapl").set(energy_uj)
        except Exception as e:
            logging.error(f"Error collecting power usage: {e}", exc_info=True)
