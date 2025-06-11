import logging
import psutil
from prometheus_client import Gauge
from .collector import Collector

class IdleTimeCollector(Collector):
    """
    Collector for system idle time (seconds).
    """

    def __init__(self, exec_info: bool, **labels):
        self.labels = labels
        self.exec_info = exec_info
        self.idle_time_gauge = Gauge(
            "system_idle_time_seconds", "System idle time in seconds", labelnames=list(labels.keys())
        )

    def collect(self):
        try:
            idle = psutil.cpu_times().idle
            self.idle_time_gauge.labels(**self.labels).set(idle)
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting idle time data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting idle time data")
