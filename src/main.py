from pathlib import Path
import os, time
import logging
from prometheus_client import start_http_server

from internal import logr, configs



def discover(ei: bool, namespace: str, subsystem: str, nodename: str) -> dict:
    """
    Discover and instantiate metric collectors from the 'collectors' directory.

    Args:
        ei (bool): Whether to include execution info in logging.
        namespace (str): The namespace for Prometheus metrics.
        subsystem (str): The subsystem for Prometheus metrics.

    Returns:
        dict: A dictionary of collector instances.
    """
    from collectors.ac_power import ACPowerCollector
    from collectors.battery_cycle import BatteryCycleCollector
    from collectors.battery import BatteryCollector
    from collectors.cpu_power import CPUPowerCollector
    from collectors.energy import EnergyCollector
    from collectors.fans import FansCollector
    from collectors.idle_time import IdleTimeCollector
    from collectors.nvme_power import NVMePowerCollector
    from collectors.power import PowerCollector
    from collectors.thermal import ThermalCollector
    from collectors.ups import UPSCollector
    
    labels = {
        "node": nodename,
    }

    return {
        "acp": ACPowerCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "battery_cycle": BatteryCycleCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "battery": BatteryCollector(namespace=namespace, subsystem=subsystem, **labels),
        "cpu_power": CPUPowerCollector(namespace=namespace, subsystem=subsystem, **labels),
        "energy": EnergyCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "fans": FansCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "idle_time": IdleTimeCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "nvme_power": NVMePowerCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "power": PowerCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "thermal": ThermalCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
        "ups": UPSCollector(ei, namespace=namespace, subsystem=subsystem, **labels),
    }

def update(collectors):
    """
    Update the Prometheus metrics with the latest values from the collectors.

    Args:
        collectors (dict): Dictionary of collector instances.
    """
    for cnam, collector in collectors.items():
        collector.collect()
        logging.debug(f"updated collector: {cnam} ({collector.__class__.__name__})")

def main():
    """
    Main function to initialize the exporter, load configurations, and start the HTTP server.
    """
    config = configs.load_configs(Path(__file__).parent / "config.yaml")
    logr.configure_logging(config.get("log_level", "INFO"))

    node_name = os.getenv("NODE_NAME", "default_node")
    collectors = discover(config["trace_errors"], config["namespace"], config["subsystem"], node_name)

    start_http_server(config["port"])
    logging.info(
        f"listening on :{config['port']} "
        f"node={node_name} "
        f"(interval={config['interval']}s, namespace={config['namespace']}, subsystem={config['subsystem']})"
    )

    # internal main loop
    while True:
        update(collectors)
        time.sleep(float(config["interval"]))

if __name__ == "__main__":
    main()
