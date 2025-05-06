# ACPI Exporter

Cloud native Prometheus exporter for exporting Advanced Configuration and Power Interface metrics of nodes, specifically in a Kubernetes cluster.

## Build

Execute `sudo docker build --no-cache -t acpi-exporter:latest .`

## Run

Execute `sudo docker run -td --privileged --pid=host -p 8000:8000 acpi-exporter:latest --port 8000`

Change ports as needed.

## TODO

- [X] Checkout `/proc/acpi` output
  - Also need data for
    - Battery: `/sys/class/power_supply/BAT0/`
    - AC Adapter: `/sys/class/power_supply/AC/`
    - Thermal Zones: `/sys/class/thermal/thermal_zone*`
    - Fans (if supported): `/proc/acpi/fan/, sometimes /sys/class/hwmon/`
- [X] Convert the output to Prometheus metrics
  - Types [prometheus.io/docs/concepts/metric_types](https://prometheus.io/docs/concepts/metric_types/)
- [X] Export the values using Prometheus exporter
  - Using this library [github.com/prometheus/client_python](https://github.com/prometheus/client_python)
- [X] Create Dockerfile
  - Useful blog [hasura.io/blog/how-to-write-dockerfiles-for-python-web-apps](https://hasura.io/blog/how-to-write-dockerfiles-for-python-web-apps-6d173842ae1d)
- [X] Deploy using docker-compose
- [ ] Host namespace issue
- [ ] Create Kubernetes manifests
- [ ] Deploy over Kubernetes using a simple Pod
- [ ] Deploy over Kubernetes using a daemonset
- [ ] Use Helm Charts for packaging

