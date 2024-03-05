# Helm Demo

## Important Note
> The secret is exposed in the helm-mongodb.yaml file. This is not a secure way to store secrets.
> No real cluster is built using this project.

## Description
This is a simple demo to show how to use Helm to deploy a mongodb and mongoexpress to a kubernetes cluster on Linode.
In the end this creates a mongodb database with mongoexpress, exposed to the internet using an ingress.
Also, by using physical storage, the data is persistent and will not be lost when the pods are deleted.
The entrypoint to the application is the Linode NodeBalancer Hostname. It can also be extended to use a "real" domain name.

## Files

- `helm-mongodb.yaml`: value file to use for bitnami/mongodb 
- `helm-mongoexpress.yaml`: creates mongodb express deployment accessing our mongodb and internal service
- `heml-ingress.yaml`: creates an ingress to access the mongoexpress service from the internet

## Steps to reproduce

### Linode
- Create a Linode account
- Create Kubernetes Cluster (f.e.: 2 * Dedicated 4GB)
- Download kubeconfig.yaml and connect to the cluster using kubectl
  - `chmod 400 kubeconfig.yaml` best practice to ensure no unauthorized user can access`
  - `export KUBECONFIG=kubeconfig.yaml` set the environment variable
  - `kubectl get node` to verify the connection

### Kubernetes
- Install Helm
- Add the Helm repository `helm repo add bitnami https://charts.bitnami.com/bitnami`
- `helm install mongodb bitnami/mongodb --values helm-mongodb.yaml` connects to Linode, creates physical storage and attaches them to the mongodb pods
- `kubectl get all` to verify the pods are running
- `kubectl apply -f helm-mongoexpress.yaml`
- `kubectl get pods` to verify the pods are running
- `helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx` add the official ingress-nginx repository
- `helm install nginx-ingress ingress-nginx/ingress-nginx --set controller.publishService.enabled=true` install the ingress controller, automatically allocate a public ip, create and provision a linode node balancer -> this node balancer is the entrypoint to the cluster
- find linode node balancer host name in UI and set in the `helm-ingress.yaml` file


### To demo the persistence
`kubectl scale --replicas=0 statefulset/mongodb` to delete the mongodb pods; the volumes are still there
`kubectl scale --replicas=3 statefulset/mongodb` to recreate the mongodb pods; the still existing volumes are attached to the new pods again -> no data is lost

### To remove the components
- `helm uninstall mongodb`
