# Microservices in Kubernetes Demo

This demo app is using an [existing microservice](https://github.com/GoogleCloudPlatform/microservices-demo) demo from Google. 

The microservices-demo consists of multiple microservices, which have clear requirements.

Apart from the services itself, a redis cache is needed, which is only used by the cart.
How the services talk to each other can be seen in the architecture diagram below.
![Architecture](./assets/google-microservices-demo-architecture-diagram.png)

The whole application is configured in the config.yaml, which describes all services, the redis cache and the frontend.
The only service that is accessible from the outside is the frontend. This is done using a ClusterIP service.

## Deploy the application

You need access to a Kubernetes cluster, in this example we will use Linode.

- `kubectl create ns microservices` create a namespace
- `kubectl apply -f config.yaml -n microservices` deploy the application

Congrats! The application is now running in your Kubernetes cluster and can be accessed via any worker node ip with the port 30007 (<ip>:30007).
