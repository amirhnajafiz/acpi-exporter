#!/usr/bin/env python3

from pathlib import Path
import os, sys, time
import logging
from prometheus_client import Gauge, start_http_server
from internal import logr, configs  # Custom modules for logging and configuration management



def discover(namespace, subsystem):
    """
    Discover and load metric collectors from the 'collectors' directory.

    Args:
        namespace (str): The namespace for Prometheus metrics.
        subsystem (str): The subsystem for Prometheus metrics.

    Returns:
        tuple: A dictionary of loaded modules and a dictionary of Prometheus Gauge objects.
    """
    here = Path(__file__).parent  # Path to the current script directory (e.g., .../src)
    sys.path.insert(0, str(here))  # Add the current directory to the Python path
    coll_dir = here / "collectors"  # Path to the 'collectors' directory

    modules, gauges = {}, {}
    for file in coll_dir.glob("*.py"):  # Iterate over all Python files in the 'collectors' directory
        mod = __import__(f"collectors.{file.stem}", fromlist=["metrics"])  # Dynamically import the module
        modules[file.stem] = mod  # Store the module in the dictionary
        for key in mod.metrics().keys():  # Iterate over the metrics defined in the module
            if key not in gauges:  # Avoid duplicate Gauge creation
                gauges[key] = Gauge(
                    key,
                    f"ACPI metric {key}",
                    namespace=namespace,
                    subsystem=subsystem,
                    labelnames=["collector", "node"],  # Labels for Prometheus metrics
                )
    logging.info(f"discovered collectors: {list(modules.keys())}")  # Log the discovered collectors
    return modules, gauges


def update(mods, gauges, node_name):
    """
    Update the Prometheus metrics with the latest values from the collectors.

    Args:
        mods (dict): Dictionary of loaded collector modules.
        gauges (dict): Dictionary of Prometheus Gauge objects.
        node_name (str): The name of the node (e.g., hostname).
    """
    for name, mod in mods.items():  # Iterate over all loaded modules
        for k, v in mod.metrics().items():  # Get the metrics from the module
            gauges[k].labels(collector=name, node=node_name).set(v)  # Update the Gauge with the metric value
    logging.debug(f"updated metrics for node: {node_name}")  # Log the update operation


def main():
    """
    Main function to initialize the exporter, load configurations, and start the HTTP server.
    """
    # Load configurations from the YAML file
    config = configs.load_configs(Path(__file__).parent / "config.yaml")

    # Configure logging based on the log level specified in the configuration
    logr.configure_logging(config.get("log_level", "INFO"))

    # Get the node name from the environment variable or use a default value
    node_name = os.getenv("NODE_NAME", "default_node")

    # Discover metric collectors and initialize Prometheus Gauges
    modules, gauges = discover(config["namespace"], config["subsystem"])

    # Start the Prometheus HTTP server on the specified port
    start_http_server(config["port"])
    logging.info(
        f"listening on :{config['port']} "
        f"(interval={config['interval']}s, namespace={config['namespace']}, subsystem={config['subsystem']})"
    )

    # Periodically update metrics and sleep for the configured interval
    while True:
        update(modules, gauges, node_name)
        time.sleep(float(config["interval"]))


if __name__ == "__main__":
    # Entry point of the script
    main()
