import logging
import psutil
from prometheus_client import Gauge
from .collector import Collector

class ACPowerCollector(Collector):
    """
    Collector for AC power connection status.
    """

    def __init__(self, exec_info: bool, **labels):
        self.labels = labels
        self.exec_info = exec_info
        self.ac_power_gauge = Gauge(
            "ac_power_online", "AC power connected (1=online, 0=offline)", labelnames=list(labels.keys())
        )

    def collect(self):
        try:
            bat = psutil.sensors_battery()
            if bat is not None:
                self.ac_power_gauge.labels(**self.labels).set(1 if bat.power_plugged else 0)
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting AC power data: {e}", 
                    exc_info=True, 
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting AC power data")
