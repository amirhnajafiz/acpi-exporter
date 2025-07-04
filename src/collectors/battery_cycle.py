import glob
import logging
from prometheus_client import Gauge
from .collector import Collector

class BatteryCycleCollector(Collector):
    """
    Collector for battery cycle count.
    """

    def __init__(self, exec_info: bool, namespace: str, subsystem: str, **labels):
        self.labels = labels
        self.exec_info = exec_info
        
        self.cycle_gauge = Gauge(
            "battery_cycle_count",
            "Battery cycle count",
            namespace=namespace,
            subsystem=subsystem,
            labelnames=list(labels.keys()) + ["battery"],
        )

    def collect(self):
        for path in glob.glob("/sys/class/power_supply/BAT*/cycle_count"):
            try:
                with open(path) as f:
                    count = int(f.read().strip())
                battery = path.split("/")[4]
                self.cycle_gauge.labels(**self.labels, battery=battery).set(count)
            except Exception as e:
                if self.exec_info:
                    logging.error(
                        f"An error occurred while collecting battery cycle count for {path}: {e}",
                        exc_info=True,
                        stack_info=True,
                    )
                else:
                    logging.error(f"An error occurred while collecting battery cycle count for {path}")
