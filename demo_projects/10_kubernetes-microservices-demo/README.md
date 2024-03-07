# Microservices in Kubernetes Demo

This demo app is using an [existing microservice](https://github.com/GoogleCloudPlatform/microservices-demo) demo from Google. 

The microservices-demo consists of multiple microservices, which have clear requirements.

Apart from the services itself, a redis cache is needed, which is only used by the cart.
How the services talk to each other can be seen in the architecture diagram below.
![Architecture](./assets/google-microservices-demo-architecture-diagram.png)
For more details, the whole repository is added in `/microservices-demo`.

The whole application is configured in the config.yaml, which describes all services, the redis cache and the frontend.
The only service that is accessible from the outside is the frontend. This is done using a ClusterIP service.

## Files
- `config.yaml` - the configuration file for the application
- `config-best-practice.yaml` - the configuration file for the application with best practices <-- use this one to demo


## Deploy the application

You need access to a Kubernetes cluster, in this example we will use Linode.

- `kubectl create ns microservices` create a namespace
- `kubectl apply -f config-best-practice.yaml -n microservices` deploy the application

Congrats! The application is now running in your Kubernetes cluster and can be accessed via the cloud provider's LoadBalancer (or via any worker node if you used the config.yaml that is bad practice).

## Kubernetes best practices

To illustrate the differences between `config.yaml` and `config-best-practice.yaml`, we will go through the best practices in the config-best-practice.yaml file.

### always specify image version
`image: gcr.io/google-samples/microservices-demo/cartservice:v0.8.0`

### use liveness and readiness probes
- kubernetes restarts pods if they're dying, but it does not know if the application inside the pod is actually running/healthy
- liveness: checks if the container is running; if not, restarts the container
- readiness: checks if the container is ready to accept traffic (important on startup)
- kubernetes can ping the application every x seconds
```yaml
          livenessProbe:
            grpc: # using grpc protocol, but can also be done using httpGet or tcpsocket
              port: 8080
            periodSeconds: 5 # the check is executed every 5 seconds
           # ...
          readinessProbe:
            httpGet:
              path: "/_healthz"
              port: 8080
            periodSeconds: 5
```

### Configure resource requests for each container
- cpu and memory
- requests what the container is guaranteed to get
- k8s scheduler uses this information
```yaml
          resources:
            requests:
              cpu: 100m
              memory: 64Mi
```

### Configure resource limits for each container
- cpu and memory
- limits what the container can use (for example infinite loop with bug)
- container can only go up to the limit
- if the values are higher than the biggest node, the pod will not be scheduled
```yaml
            limits:
              cpu: 200m
              memory: 128Mi
```

### Dont expose a NodePort
- security risk as it opens a port on each worker node
- only use internal services with one entrypoint in the cluster
- the cloud providers loadbalancer can be used or an ingress

### More than 1 replica for Deployment
- replica is 1 by default
- that means if the pod crashes we have down-time until the pod is restarted
