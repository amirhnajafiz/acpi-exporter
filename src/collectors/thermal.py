import logging
import psutil
from prometheus_client import Gauge

from .collector import Collector


class ThermalCollector(Collector):
    """
    Thermal collector for gathering temperature metrics.
    This collector uses the psutil library to access temperature information.
    """

    def __init__(self, exec_info: bool, namespace: str, subsystem: str, **labels):
        self.labels = labels
        self.exec_info = exec_info
        
        label_names = list(labels.keys()) + ["device", "sensor"]
        self.temp_gauge = Gauge(
            "temperature_celsius", 
            "Temperature in Celsius", 
            namespace=namespace,
            subsystem=subsystem,
            labelnames=label_names,
        )

    def collect(self):
        try:
            for dev, entries in psutil.sensors_temperatures(fahrenheit=False).items():
                for idx, e in enumerate(entries):
                    sensor_lbl = (e.label or f"{dev}_{idx}").replace(" ", "_").lower()
                    all_labels = {**self.labels, "device": dev, "sensor": sensor_lbl}
                    self.temp_gauge.labels(**all_labels).set(float(e.current))
        except AttributeError:
            logging.warning("psutil.sensors_temperatures() is not supported on this platform")
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting temperature data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting temperature data")
