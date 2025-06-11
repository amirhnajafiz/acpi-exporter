from pathlib import Path
import os, time
import logging
from prometheus_client import start_http_server

from internal import logr, configs



def discover(namespace: str, subsystem: str) -> list:
    """
    Discover and instantiate metric collectors from the 'collectors' directory.

    Args:
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
    
    return [
        ACPowerCollector(namespace=namespace, subsystem=subsystem),
        BatteryCycleCollector(namespace=namespace, subsystem=subsystem),
        BatteryCollector(namespace=namespace, subsystem=subsystem),
        CPUPowerCollector(namespace=namespace, subsystem=subsystem),
        EnergyCollector(namespace=namespace, subsystem=subsystem),
        FansCollector(namespace=namespace, subsystem=subsystem),
        IdleTimeCollector(namespace=namespace, subsystem=subsystem),
        NVMePowerCollector(namespace=namespace, subsystem=subsystem),
        PowerCollector(namespace=namespace, subsystem=subsystem),
        ThermalCollector(namespace=namespace, subsystem=subsystem),
        UPSCollector(namespace=namespace, subsystem=subsystem),
    ]

def update(collectors):
    """
    Update the Prometheus metrics with the latest values from the collectors.

    Args:
        collectors (dict): Dictionary of collector instances.
    """
    for collector in collectors:
        collector.collect()

def main():
    """
    Main function to initialize the exporter, load configurations, and start the HTTP server.
    """
    config = configs.load_configs(Path(__file__).parent / "config.yaml")
    logr.configure_logging(config.get("log_level", "INFO"))

    node_name = os.getenv("NODE_NAME", "default_node")
    collectors = discover(config["namespace"], config["subsystem"])

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
