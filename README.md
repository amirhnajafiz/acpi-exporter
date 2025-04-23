# ACPI Exporter

Cloud native Prometheus exporter for exporting Advanced Configuration and Power Interface metrics of nodes, specifically in a Kubernetes cluster.

## TODO

- [ ] Checkout `/proc/acpi` output
- [ ] Convert the output to separated fields
- [ ] Export the values using Prometheus exporter
  - Using this library [github.com/prometheus/client_python](https://github.com/prometheus/client_python)
- [ ] Create Dockerfile
  - Useful blog [hasura.io/blog/how-to-write-dockerfiles-for-python-web-apps](https://hasura.io/blog/how-to-write-dockerfiles-for-python-web-apps-6d173842ae1d)
- [ ] Deploy using docker-compose
- [ ] Create Kubernetes manifests
- [ ] Deploy over Kubernetes using a simple Pod
- [ ] Deploy over Kubernetes using a daemonset
- [ ] Use Helm Charts for packaging
