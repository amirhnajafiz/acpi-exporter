# ACPI Exporter

Cloud native Prometheus exporter for exporting Advanced Configuration and Power Interface (ACPI) metrics of nodes, specifically in a Kubernetes cluster.

## Features

ACPI Exporter provides a wide range of hardware and power-related metrics as Prometheus gauges, including:

- **AC Power Status** (`ac_power_online`): Reports if the system is running on AC power or battery.
- **Battery Metrics** (`battery_pct`, `battery_secs_left`): Battery percentage and estimated seconds left.
- **Battery Cycle Count** (`battery_cycle_count`): Number of battery charge/discharge cycles.
- **CPU Power Usage** (`cpu_power_watts`): Real-time CPU package power usage (Watts, via RAPL).
- **Energy Consumption** (`energy_consumed_joules`): Total energy consumed (Joules, via RAPL).
- **Fan Speed** (`fan_speed_rpm`): Fan speeds for all detected fans.
- **Idle Time** (`system_idle_time_seconds`): System idle time in seconds.
- **NVMe Power State** (`nvme_power_state`): Power state of NVMe SSDs.
- **System Power Usage** (`power_usage_watts`): System power usage (Watts, via RAPL).
- **Thermal Sensors** (`temperature_celsius`): Temperatures from all available sensors.
- **UPS Status** (`ups_battery_charge_pct`, `ups_online`): UPS battery charge and online status (requires NUT or apcupsd).

> **Note:** Some metrics require Linux and specific hardware support (e.g., Intel RAPL, NVMe, UPS).

## Test

Run the following command to set up an instance of ACPI exporter with a Prometheus server:

```sh
docker-compose up -d
```

## Configuration

Edit `configs/example.config.yaml` or provide your own config via Docker/Kubernetes. Example:

```yaml
# Metrics server port
port: 8000

# Exporter interval in seconds
interval: 5

# Exporter NS and subsystem
namespace: "ACPI"
subsystem: "exporter"

# Set the desired log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_level: "DEBUG"

# Trace errors
trace_errors: false
```
## Metrics

Each collector exposes one or more Prometheus metrics:

| Metric Name                | Description                                      |
|----------------------------|--------------------------------------------------|
| `ac_power_online`          | Reports if the system is running on AC power or battery |
| `battery_pct`              | Battery percentage                               |
| `battery_secs_left`        | Estimated seconds left on battery                |
| `battery_cycle_count`      | Number of battery charge/discharge cycles        |
| `cpu_power_watts`          | Real-time CPU package power usage (Watts, via RAPL) |
| `energy_consumed_joules`   | Total energy consumed (Joules, via RAPL)         |
| `fan_speed_rpm`            | Fan speeds for all detected fans                 |
| `system_idle_time_seconds` | System idle time in seconds                      |
| `nvme_power_state`         | Power state of NVMe SSDs                         |
| `power_usage_watts`        | System power usage (Watts, via RAPL)             |
| `temperature_celsius`      | Temperatures from all available sensors          |
| `ups_battery_charge_pct`   | UPS battery charge (requires NUT or apcupsd)     |
| `ups_online`               | UPS online status (requires NUT or apcupsd)      |

## Kubernetes

See the `k8s/` directory for manifests to deploy ACPI Exporter as a DaemonSet, Service, and ServiceMonitor.
