# Prometheus Demo

Prometheus will be setup Prometheus in an EKS cluster using a Helm chart. This will automatically deploy Prometheus, Grafana, and other components.
After this is done the Prometheus UI or Grafana can be used to monitor the Kubernetes cluster and the microservices application.
In addition, alert rules are defined to trigger alerts when certain conditions are met.

Already existing alert rules (navigate to Prometheus UI -> Alerts -> Rules):
- most of them are for the Prometheus stack itself
- most of them are inactive or condition not met

Alert rules to be added:
- CPU > 50%
- when a Pod cannot start
They can be found in the `alert-rules.yaml` file.

## Prerequisites
- EKS cluster
  - with deployed microservices application
  - can be done using eksctl
  - `eksctl create cluster` (default options)
  - `kubectl apply -f config-loadbalancer.yaml` to deploy the microservices application

## Steps
1. Deploy Prometheus using Helm
- `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
- `helm repo update`
- `kubectl create ns monitoring`
- `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring`
- `kubectl --namespace monitoring get pods -l "release=monitoring"` to check if all pods are running (alternatively `kubectl get all -n monitoring`)
2. Monitor Kubernetes cluster
3. Monitor microservices application

## Commands
- `kubectl port-forward service/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring &` to access Prometheus UI
- `kubectl port-forward service/monitoring-grafana 8080:80 -n monitoring &` to access Grafana UI (default credentials: admin/prom-operator)
- `kubectl run curl-test --image=radial/busyboxplus:curl -i --tty --rm` to add a pod which will 
- to test the visualization under load it is an option to run the following
  - `kubectl run curl-test --image=radial/busyboxplus:curl -i --tty --rm`
  - `vi test.sh` and add the following to curl the loadbalancer
    ```bash
    for i in $(seq 1 10000); do
      curl http://<loadbalancer-dns-name> > test.txt 
    done
    ```
  - `chmod +x test.sh` make the script executable
- `kubectl apply -f alert-rules.yaml` to add alert rules
- `kubectl get PrometheusRule -n monitoring` to check if the alert rules are added

## Test Alert Rules
- to simulate a high CPU load we will use [containerstack/cpustress dockerhub image](https://hub.docker.com/r/containerstack/cpustress)
  - `kubectl run cpu-test --image=containerstack/cpustress -- --cpu 4 --timeout 30s --metrics-brief` -> the `--` is used to pass arguments to the container, `cpu-test` is the name we gave the pod

## Files
- this project consists of various .yaml files that are used to deploy the shopping example application. They are quite similar, but only the `config-loadbalancer.yaml` is used to deploy the application.
- `alert-rules.yaml` contains the alert rules that are added to Prometheus
