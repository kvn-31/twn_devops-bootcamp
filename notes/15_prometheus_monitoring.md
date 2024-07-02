# Monitoring with Prometheus

- monitoring tool
- mostly used in dynamic container environments (but can also be used in traditional environments)
- in DevOps 100s of processes are connected, if there is no insight into the system, it is difficult to manage
- use cases: monitoring, alerting, ...
  - f.e. check memory usage -> if > threshold -> send alert

## Architecture
- Prometheus can basically monitor anything
  - what is monitored is called a target
  - examples of targets: linux/Windows server, apache, single application, database
  - examples of units (=metrics): CPU, memory, disk, network, requests count ...
    - metrics format: human readable, key-value pairs
    - TYPE (one of 3 metrics types) and HELP (description of metric) attributes
      - counter: always increasing, f.e. requests count
      - gauge: can increase and decrease, f.e. CPU usage -> what is the current value of x
      - histogram: samples observations and counts them in configurable buckets -> how long or how big?
- Main component: Prometheus server
  - does the actual monitoring work
  - time series database which stores metrics data
  - data retrieval worker which pulls data
  - http server which accepts queries to retrieve data
- Prometheus pulls metrics from the target from HTTP endpoint
  - target exposes metrics in a format Prometheus can understand
    - some targets have built-in support for Prometheus, others need an exporter = a small service that converts the metrics to Prometheus format
    - at /metrics endpoint
    - exporters are available for many applications, also as Docker images
  - Prometheus scrapes the metrics from the target
  - Prometheus stores the metrics in its time series database
- Monitoring own applications
  - use client libraries for the programming language of your application

## Pull vs Push
- Prometheus pulls metrics from the target
  - more efficient 
  - multiple Prometheus servers can pull metrics from the same target
  - better detection if a service is up and running
- other monitoring tools push metrics to the monitoring server which creates a high load of traffic -> monitoring can become a bottleneck
- also for pushing the target needs additional software/tools to push the metrics
- for targets that only run for a short time:
  - pushgateway -> target pushes metrics to pushgateway, Prometheus pulls metrics from pushgateway

## Configuration
- Prometheus configuration file: prometheus.yml
  - which targets at what intervals
  - global: scrape_interval and evaluation_interval
  - rule_files: define alerting rules (which conditions trigger an alert)
  - scrape_configs: define targets
    - job_name: name of the target -> can have target specific configurations (f.e. scape time)
    - metrics_path: path to the metrics endpoint
    - static_configs: list of targets
    - relabel_configs: modify the target labels

## Alert Manager
- part of Prometheus ecosystem
- receives alerts from Prometheus and sends notifications (f.e. email, slack, ...)

## Data Storage
- Prometheus stores data in its own time series database
- data is stored on disk locally but can also be stored in remote storage

## PromQL (Query Language)
- query language to retrieve data from Prometheus
- can be used in the Prometheus web interface or in Grafana
- example: `http_requests_total{status!~"4.."}`
  - query all http status codes except 4xx

## Prometheus Characteristics
- reliable
- each server is standalone and self-containing
- works even if other parts of infrastructure are down
- easy to set up
- difficult to scale

## Prometheus Federation
- scalable cloud apps need monitoring that can scale
- allows one Prometheus server to scrape data from another Prometheus server

## Prometheus with Docker and Kubernetes
- fully compatible with Docker and Kubernetes
- available as Docker image
- can easily be deployed in Kubernetes
- supports monitoring of K8s cluster node resources out of the box

## Prometheus in Kubernetes cluster
There are various ways to deploy Prometheus in a Kubernetes cluster:
- creating all configuration YAML files manually, then execute in right order -> inefficient, a lot of effort, not recommended for most cases
- Using an operator
  - manager of all prometheus components
  - manages the combination of all components as one unit
- Using Helm to deploy operator
  - package manager for Kubernetes
  - Helm for initial setup
  - operator to manage setup
  - see [Prometheus Demo](../../demo_projects/16_prometheus-demo/README.md) for an example

## Prometheus Helm Chart
- Helm chart for Prometheus is available under `prometheus-community/kube-prometheus-stack`
- 2 stateful sets: prometheus and alertmanager
- 3 deployments: kube-state-metrics (own helm chart, scrapes K8s components), kube-prometheus-operator, grafana
- daemonset: node-exporter (runs on every single worker node, translates worker node metrics to Prometheus format)
- in simples words: out of the box monitoring solution for K8s cluster
- worker nodes and k8s components are monitored

