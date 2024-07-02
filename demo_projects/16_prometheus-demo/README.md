# Prometheus Demo

Prometheus will be setup using a Helm chart.

## Prerequisites
- EKS cluster
  - with deployed microservices application
  - can be done using eksctl
  - `eksctl create cluster` (default options)
  - `kubectl apply -f config-microservice.yaml` to deploy the microservices application

## Steps
1. Deploy Prometheus using Helm
- `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
- `helm repo update`
- `kubectl create ns monitoring`
- `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring`
- `kubectl --namespace monitoring get pods -l "release=monitoring"` to check if all pods are running (alternatively `kubectl get all -n monitoring`)
2. Monitor Kubernetes cluster
3. Monitor microservices application
