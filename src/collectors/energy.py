import logging
import os
from prometheus_client import Gauge
from .collector import Collector

class EnergyCollector(Collector):
    """
    Energy collector for gathering total energy consumption metrics.
    """

    def __init__(self, exec_info: bool, namespace: str, subsystem: str, **labels):
        self.labels = labels
        self.exec_info = exec_info
        
        label_names = list(labels.keys()) + ["source"]
        self.energy_joules_gauge = Gauge(
            "energy_consumed_joules", 
            "Total energy consumed in Joules", 
            namespace=namespace,
            subsystem=subsystem,
            labelnames=label_names,
        )

    def collect(self):
        try:
            # Example for Linux systems with RAPL interface
            energy_path = "/sys/class/powercap/intel-rapl:0/energy_uj"
            if os.path.exists(energy_path):
                with open(energy_path) as f:
                    energy_uj = int(f.read())
                self.energy_joules_gauge.labels(**self.labels, source="rapl").set(energy_uj / 1_000_000)
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting energy data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting energy data")
