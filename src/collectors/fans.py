import logging
import psutil
from prometheus_client import Gauge
from .collector import Collector

class FansCollector(Collector):
    """
    Fans collector for gathering fan speed metrics.
    This collector uses the psutil library to access fan information.
    """

    def __init__(self, exec_info: bool, **labels):
        self.labels = labels
        self.exec_info = exec_info
        label_names = list(labels.keys()) + ["device", "fan"]
        self.fan_speed_gauge = Gauge(
            "fan_speed_rpm", "Fan speed in RPM", labelnames=label_names
        )

    def collect(self):
        try:
            for dev, entries in psutil.sensors_fans().items():
                for idx, e in enumerate(entries):
                    fan_lbl = (e.label or f"{dev}_{idx}").replace(" ", "_").lower()
                    all_labels = {**self.labels, "device": dev, "fan": fan_lbl}
                    self.fan_speed_gauge.labels(**all_labels).set(float(e.current))
        except AttributeError:
            logging.warning("psutil.sensors_fans() is not supported on this platform")
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting fan data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting fan data")
