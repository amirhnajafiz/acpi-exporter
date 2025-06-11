import psutil
from prometheus_client import Gauge
from .collector import Collector

class BatteryCollector(Collector):
    """
    Battery collector for gathering battery metrics.
    This collector uses the psutil library to access battery information.
    """

    def __init__(self, **labels):
        self.labels = labels
        label_names = list(labels.keys())
        
        self.battery_pct_gauge = Gauge(
            "battery_pct", "Battery percentage", labelnames=label_names
        )
        self.battery_secs_left_gauge = Gauge(
            "battery_secs_left", "Seconds of battery left", labelnames=label_names
        )

    def collect(self):
        bat = psutil.sensors_battery()
        if bat is not None:
            self.battery_pct_gauge.labels(**self.labels).set(bat.percent)
            self.battery_secs_left_gauge.labels(**self.labels).set(bat.secsleft)
