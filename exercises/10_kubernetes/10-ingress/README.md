```
minikube start --driver=docker
minikube addons enable ingress
minikube dashboard
kubectl apply -f dashboard-ingress.yaml
minikube tunnel
```
Edit Hosts file
```
127.0.0.1  dashboard.com
```
