import glob
import logging
from prometheus_client import Gauge

from .collector import Collector

class NVMePowerCollector(Collector):
    """
    Collector for NVMe SSD power state.
    """

    def __init__(self, **labels):
        self.labels = labels
        self.nvme_power_state_gauge = Gauge(
            "nvme_power_state", "NVMe SSD power state", labelnames=list(labels.keys()) + ["device"]
        )

    def collect(self):
        for path in glob.glob("/sys/class/nvme/nvme*/power/state"):
            try:
                with open(path) as f:
                    state = int(f.read().strip())
                device = path.split("/")[4]
                self.nvme_power_state_gauge.labels(**self.labels, device=device).set(state)
            except Exception as e:
                logging.error(
                    f"An error occurred while collecting NVMe power state for {path}: {e}",
                    exc_info=True,
                )
