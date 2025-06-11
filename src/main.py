#!/usr/bin/env python3

from pathlib import Path
import os, time
import logging
from prometheus_client import start_http_server
from internal import logr, configs  # Custom modules for logging and configuration management



def discover(namespace, subsystem):
    """
    Discover and instantiate metric collectors from the 'collectors' directory.

    Args:
        namespace (str): The namespace for Prometheus metrics.
        subsystem (str): The subsystem for Prometheus metrics.

    Returns:
        dict: A dictionary of collector instances.
    """
    from collectors.battery import BatteryCollector
    from collectors.fans import FansCollector
    from collectors.thermal import ThermalCollector
    
    return {
        "battery": BatteryCollector(namespace=namespace, subsystem=subsystem),
        "fans": FansCollector(namespace=namespace, subsystem=subsystem),
        "thermal": ThermalCollector(namespace=namespace, subsystem=subsystem),
    }

def update(collectors):
    """
    Update the Prometheus metrics with the latest values from the collectors.

    Args:
        collectors (dict): Dictionary of collector instances.
    """
    for cname, collector in collectors.items():
        collector.collect()

def main():
    """
    Main function to initialize the exporter, load configurations, and start the HTTP server.
    """
    config = configs.load_configs(Path(__file__).parent / "config.yaml")
    logr.configure_logging(config.get("log_level", "INFO"))

    host_proc = os.environ.get("HOST_PROC")
    if host_proc:
        logging.info(f"Using host_proc: {host_proc}")
    else:
        logging.info(f"Not using host_proc")

    node_name = os.getenv("NODE_NAME", "default_node")

    collectors = discover(config["namespace"], config["subsystem"])

    start_http_server(config["port"])
    logging.info(
        f"listening on :{config['port']} "
        f"node={node_name} "
        f"(interval={config['interval']}s, namespace={config['namespace']}, subsystem={config['subsystem']})"
    )

    while True:
        update(collectors)
        time.sleep(float(config["interval"]))

if __name__ == "__main__":
    main()
