import logging
import subprocess
from prometheus_client import Gauge
from .collector import Collector

class UPSCollector(Collector):
    """
    Collector for UPS status (requires NUT or apcupsd integration).
    """

    def __init__(self, exec_info: bool, namespace: str, subsystem: str, **labels):
        self.labels = labels
        self.exec_info = exec_info
        
        self.ups_charge_gauge = Gauge(
            "ups_battery_charge_pct", 
            "UPS battery charge percentage", 
            namespace=namespace,
            subsystem=subsystem,
            labelnames=list(labels.keys()),
        )
        self.ups_online_gauge = Gauge(
            "ups_online", 
            "UPS online status (1=online, 0=on battery)", 
            namespace=namespace,
            subsystem=subsystem,
            labelnames=list(labels.keys()),
        )

    def collect(self):
        # Example: parse output from 'upsc' (NUT)
        try:
            output = subprocess.check_output(["upsc", "myups@localhost"]).decode()
            for line in output.splitlines():
                if line.startswith("battery.charge:"):
                    pct = float(line.split(":")[1].strip())
                    self.ups_charge_gauge.labels(**self.labels).set(pct)
                if line.startswith("ups.status:"):
                    status = line.split(":")[1].strip()
                    self.ups_online_gauge.labels(**self.labels).set(1 if status == "OL" else 0)
        except Exception as e:
            if self.exec_info:
                logging.error(
                    f"An error occurred while collecting UPS data: {e}",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                logging.error(f"An error occurred while collecting UPS data")
