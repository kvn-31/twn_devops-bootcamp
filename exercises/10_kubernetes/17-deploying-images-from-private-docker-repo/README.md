# Deploying images from private docker repo

Instead of deploying images from the local machine, we want to use images from a private docker registry. In this case, we use AWS ECR as an example.
The main learning part of this project is to use a secret to access the private docker registry and using imagePullSecrets in the deployment file.

## Prerequisite

- app images pushed to private docker registry (in this case aws)

## Steps to reproduce

`aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin INSTANCE` login to aws ecr

### Login to AWS with Minikube
as Minikube runs in a VM, we cannot access the docker cred store. as a workaround we can use the `aws ecr get-login-password` command to get the password and use it to login to the registry.

- `aws ecr get-login-password` copy the token
- `minikube ssh` ssh into minikube
- `docker login -username AWS -p TOKEN INSTANCE` login to aws ecr in minikube; .docker/config.json will be created in minikube
- exit minikube
- `minikube cp minikube:/home/docker/.docker/config.json SOME-FOLDER/config-minikube.json` copy the config file to the host system
- `cat FILE | base64 -w 0` base64 encode the config file and paste it into the docker-secret.yaml file
- `kubectl apply -f docker-secret.yaml`

alternative where we do not need to sh into minikube (with the limit to be executed for every secret):
```
kubectl create secret docker-registry my-registry-key \
--docker-server=https://private-repo \
--docker-username=user \
--docker-password=pwd 
```
- `kubectl apply -f my-app-deployment.yaml` deploy the app
- `kubectl get pods` verify the pods are running
