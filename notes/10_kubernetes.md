# 10 - Kubernetes

- real-world: applications with hundreds of containers, especially considering microservices
- -> we need container orchestration tools
- open-source container orchestration tool, developed by google
- helps manage containerized applications in different deployment environments

## Features
- high availability, no downtime
- scalability (scale up and down)
- disaster recovery - backup + restore

## Components
- node
    - virtual/physical machine
- pod
    - smallest unit in kubernetes
    - abstraction over a container -> creates running environment/layer on top of container
    - usually 1 application per pod
    - each pod has its own ip address
    - ephemeral -> can die easily -> new ip address is assigned -> this why services are needed
    - normally no interaction with pod, but with the abstraction layer (Deployment)
- service
    - attached to a pod
    - permanent ip address which can be attached to each pod
    - does not die if the pod dies
    - external service: opens communication from external sources
    - internal service: for database f.e.
    - is also a load-balancer
- ingress
    - does the forwarding from a request (to a domain f.e.) to the service (ip)
- config map
    - pods communicate with each other using services (f.e. mongo-db-service), but db url is defined in the application properties/config file/env variable -> what if the name of db service or db url needs to be changed?
    - to solve this problem and avoid a rebuild of the application we use ConfigMap
    - external config of application
    - connected to pod
    - if name of service/endpoint is changed we just change it in config map -> no rebuild is needed
    - used inside the pod with env variables or properties file
    - no confidential data (username pw)
- secret
    - is like ConfigMap, but used for secret data such as credentials
    - important: it is not secure out of the box
    - also connected to pod
    - used inside the pod with env variables or properties file
- Volumes
    - if pod restarts, data would be gone
    - to avoid this we use Volumes
    - attaches a physical storage to a pod
    - storage can be on local machine/remote/outside the cluster
    - kubernetes does not manage data persistence!
- Deployment
    - kubernetes uses distributed systems
    - -> instead of relying on one pod, everything is replicated -> if one pod fails the prod app is not down
    - to do this: blueprint of pod is defined and specified how many replicas are needed
    - this blueprint is called Deployment
    - is an abstraction on top of pods
    - container -> pods -> deployment
- Statefulset
    - Databases cannot be replicated because it has state (risk to have data inconsistencies)
    - for all stateful apps (mysql, psql, ..)
    - makes sure that db reads & writes are synchronized
    - DBs are often hosted outside of K8s cluster
- DaemonSet
    - calculates how many replicas are needed based on existing nodes
    - deploys just one replica per node
    - adds pods if nodes are added
    - removes pods (garbage collected) if nodes are removed
    - no need to define replica count
    - automatically scales up & down by number of nodes

## Architecture

- each node has multiple pods on it (sometimes also called worker nodes)
- to manage: 3 processes are installed
    - container runtime
    - kubelet: interacts with container and node; responsible to actually start the pod with container inside
    - kube proxy: forwards the requests from services to pods
- different container runtimes:
    - docker
    - containerd (most used, more lightweight)
    - cri-o
- docker can run on any container runtime

### Control Plane Nodes
in order to interact with a cluster (schedule pods, monitor, re-start, join new node, ..) control plane nodes are used

4 processes run on every control plane node

- Api server: cluster gateway -> main entrypoint; validates requests and forwards; can be accessed via ui, api or cli (kubectl)
- Scheduler: API server receives request to schedule a new node and sends it to scheduler; has intelligent logic where to put the node; Kubelet actually starts the pod on the node
- Controller Manager: detects state changes (f.e. pod dies), tries to recover state; Controller Manager -> Scheduler -> Kubelet
- etcd: Key-Value store of cluster; cluster's brain; every change in the cluster is updated in the etcd state; must be stored reliable and replicated; no application data stored here

## Example cluster setup

- 2 control plane nodes (more important, but need less resources)
- 3 worker nodes
- can be extended with growing application complexity / demand

## Local Setup Minikube & kubectl

### Minikube
a whole cluster cannot be tested on local machine because of potential lack of memory/processing power -> we use minikube

- is a one node cluster where control plane and worker node processes run on one node/machine
- must start either as container or VM
- the preferred driver is Docker
    - means minikube runs as docker container
    - but inside minikube the applications are also run using docker
- setup: https://minikube.sigs.k8s.io/docs/start/ -> if docker is not installed, have look at drivers page
- start: minikube start --driver docker

#### Minikube commands
```
minikube start
minikube addons enable NAME
minikube dashboard #opens the dashboard in a new window
```

### Assign external service a public ip address with minikube

minikube service NAME

- creates a tunnel and uses the local ip address (no real public ip address)

## Kubectl
used to interact with a cloud or Minikube cluster

- cli tool for K8s cluster
- used to talk to the api server

### Kubectl commands
```
# create a deployment, get latest image from dockerhub
kubectl create deployment NAME --image=IMAGE
kubectl create X

# get all elements of type
kubectl get all
kubectl get node
kubectl get deployment
kubectl get replicaset
kubectl get namespace
kubectl get pod -o wide # with more details such as ip address (handy to see if service is referencing the right pod)
kubectl get deployment nginx-deployment -o yaml > nginx-deployment-result.yaml # save to file with auto-generated status section

# update
kubectl edit deployment NAME

# delete deployment
kubectl delete deployment NAME -> cascades, so that also the replicaset and pod are deleted
kubectl delete -f nginx-deployment.yaml #by file

# logs & information (status changes)
kubectl logs NAME #log to console
kubectl describe pod NAME #info about pod

# port forwarding
kubectl port-forward service/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
kubectl port-forward service/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring & #run in background

# interactive terminal inside pod
kubectl exec -it NAME -- /bin/bash #alternatively use /bin/sh
```

## Layers of Abstraction

- Deployment manages a ..
- Recplicaset manages a ..
- Pod is an abstraction a ..
- Container

## Configuration File
instead of writing a lot of cli commands to create deployments, we use configuration files which are executed using apply

```
kubectl apply -f FILE
```
Can be used to create or even to update

## YAML Kubernetes Configuration File
on top has apiversion & kind

consists of 3 parts

- metadata (f.e. name)
- spec: for every part of configuration; attributes specific to the kind we create
- status: automatically generated and added by Kubernetes -> will automatically compare desired vs actual state (basis of self-healing); updated continously; status is coming from etcd
    - to access the status
kubectl get deployment nginx-deployment -o yaml

- stored with application code

### Template
bluetprint to a pod: has own metadata -> config applies to pod

### Labels & Selectors
- Metadata contains the label
- spec part contains the selectors
- Pods get a Label
- tell the deployment to match all the labels to create the connection -> deployment knows which pods belong to it
- service can be connected using the selector

service.yaml
```
spec:
    selector:
        app: nginx
```

deployment.yaml
```
metadata:
    labels:
        app: nginx
spec:
    selector:
        matchLabels:
            app: nginx
    template:
        metadata:
            labels:
                app: nginx
```

### Ports
- Service has a port where it is accessible at
- service needs to know to which pod at which port it needs to forward request

service.yaml
```
spec:
  selector:
    app: nginx
  ports:
    - protocol: tcp
      port: 80   # Port number where the service will be accessible within the cluster
      targetPort: 8080  # Port number on which your application is listening
```
deployment.yaml
```
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 8080
```

### Simple setup using service & deployment

```sh
kubectl apply -f nginx-deployment.yaml
kubectl apply -f nginx-service.yaml

# are they correctly connected?
kubectl describe service nginx-service
# output shows the correct selector, target port and correct endpoint ip -> it must be ip addresses of the pods
# how to find ip address of pod?
kubectl get pod -o wide
```

### Demo Project
- Mongo-db & mongo-express
- Simple web application with its database
- flow: client -> external service (mongo express) -> mongo-express pod -> internal service (mongo db) -> mongo db pod
- order of creation matter -> we need secrets before we reference them in the deployment

### Secrets
secret.yaml
```yaml
data:
  mongo-root-username: dXNlcm5hbWU= #base64 encoded, but not encrypted -> not safe!
```
This can be referenced, AFTER it was created in deployment.yaml

```yaml
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: mongo-root-username
```

### ConfigMap
- external configuration
- centralized
- other components can access it
- as with secret: order of execution matters!
```yaml
          - name: ME_CONFIG_MONGODB_SERVER
            valueFrom:
                configMapKeyRef:
                    name: mongodb-configmap
                    key: mongo-database-url

```

### Service (intro)
- either internal or external
- clusterIp = internal service is the default; only gives internal ip address
- LoadBalancer = external service; also gives external ip address
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongo-express-service
spec:
  selector:
    app: mongo-express # connects to the pods with the label
  type: LoadBalancer # <- means that the service will be accessible from outside the cluster = external service
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8081
      nodePort: 30000 # <- this is the port that will be used to access the service from outside the cluster
```

## K8s Namespaces (Detail)

- resources can be organised in namespaces
- a cluster can have multiple namespaces
    - it is like a virtual cluster inside a cluster
- out of box namespaces:
    - kube-system: do not edit/create anything here -> for system processes
    - kube-public: publicly accessible data, configmap with cluster information
    - kube-node-lease: heartbeats of nodes, avialability of nodes
    - default: used if no new namespace is created
- kubectl create namespace NAME
- better: use configuration file

### When is a namespace needed?
if only default namespace is used -> filled quickly; no overview

- for better overview: group recouces in namespaces (f.e. database, monitoring, elastic stack, nginx/ingress)
- to avoid conflicts: if multiple teams work on the same application it can lead to conflicts (if resource has same name, but different config
- for environments in the same cluster (staging, development, ..) and now the namespaces can share the elastic stack namespace for example
- resource sharing: for different versions in production -> might need the same shared resources
- to limit access to resources on namespaces -> each team has own isolated env; also resource quota can be divided between teams

### Characteristics of Namespaces
- most resources of another namespace cannot be accessed (f.e. configmap/secret)
- services can be shared between namespaces (database_url: NAMESPACE.SERVICE)
- volume & node live globally in the cluster, cannot live in a namespace
- by default components are created in default namespace

### Apply Namespaces
- kubectl apply -f FILE --namespace=my-namespace
- directly in file in metadata <- preferred
```
        metadata:
            name: NAME
            namespace: NAMESPACE
```

- change the default/active namespace
- kubectl config set-context --current --namespace=my-namespace
    - after using this, the namespace for current context is set, meaning all subsequent commands will use it

#### Kubens
- even more convenvient tool
- kubens is a tool to switch between Kubernetes namespaces (and configure them for kubectl) easily
- install kubectx, automatically installs kubens

```sh
kubens #see list of namespaces
kubens my-namespace #switch to namespace
```


## Services (Detail)
- pods are ephemeral, are destroyed frequently -> in order to have a stable ip address services are needed
- also provides load balancing

### Types of services

Cluster Ip

- default
- = internal service -> only accessible within the cluster
- is accessible at a certain ip address & port
- is the entrypoint after ingress
- service forwards the request to one of the pods
    - which pod(s)? -> by the selector it matches all the replicas
    - which port? -> defined in targetPort attribute -> has to match the port where the container inside the pod is listening at
- randomly selects to which pods the request is forwarded (load balancer)
- multi port services
    - inside the pod, another container is running (f.e. for monitoring)
    - one service now is responsible for different endpoints (mongodb application and mongodb-exporter f.e.)
    - the service now also needs to have multiple ports open, one for each container it forwards the request to
```yaml
  ports:
    - name: mongodb
      protocol: TCP
      port: 27017
      targetPort: 27017
    - name: mongodb-exporter
      protocol: TCP
      port: 9216
      targetPort: 9216
```

Headless service

- if client/pod want to talk to a specific pod
- not randomly selected
- use case: stateful applications (database) -> pod replicas are not identical; for example mysql + replica -> only the main instance is allowed to write to db; replicas are syncing and only for reading data
- kubernetes provides dns lookup service to return single ip address (ClusterIp); if clusterIp is set to none it returns the pod ip address instead
- is used alongside the ClusterIp service, for specific operations
- headless service has no load balancing, it is just used to talk to a specific pod

NodePort

- external service
- external traffic accessible on a fixed port for each worker node
- instead of using an ingress, the browser request will come directly to worker node
- port exposed=nodePort value (has a fixed range)
- clusterip service to which nodeport service will route is automatically created
- not secure! -> only to test quickly

LoadBalancer
- external service
- becomes accessible externally through cloud providers load balancer
- nodePort and clusterIp services are created automatically
- only accessible through the load balancer


LoadBalancer is an extension of the NodePort service which is an extension of the ClusterIp service

## Ingress

- exposes http route to outside the cluster
- instead of an external service, ingress can be used
- domains can be assigned
- An Ingress may be configured to give Services externally-reachable URLs, load balance traffic, terminate SSL / TLS, and offer name-based virtual hosting
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: "foo.bar.com" #valid domain address
    http: #does not mean it is not https
      paths:
      - pathType: Prefix
        path: "/" # -> foo.bar.com/ 
        backend:
          service:
            name: my-internal-service
            port:
              number: 80 #internal service port
```

- forwards request from the host to the internal service

### Ingress Controller
- evaluates the rules
- manages redirects
- entrypoint to cluster
- needs to be installed -> multiple implementations (even 3rd party)

### Load Balancer
there are different ways to connect to the ingress

- ready-to-use hosting load balancer (f.e. aws): easy setup, forwards progress to ingress
- bare metal
    - some entrypoint needs to be configured
    - can be inside the cluster or outside as separate server
    - for example an external proxy: separate server -> no server in k8s cluster is accessible from outside, public ip address, entrypoint to cluster

### Ingress Controller in Minikube
- minikube addons enable ingress: enables k8s nginx implementation of ingress controller
- minikube acts differently that the "real" web.
- as we obviously do not have the domain "dashboard.com" registered, we will add it to the /etc/hosts file -> 127.0.0.1  dashboard.com
- run minikube tunnel (only needed for local development)

### Multiple patchs for same host

- multiple applications under the same domain

```
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /foo
        backend:
          service:
            name: service1
            port:
              number: 4200
      - path: /bar
        backend:
          service:
            name: service2
            port:
              number: 8080
```

### Multiple sub-domains / domains

```
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
        path: "/"
        backend:
          service:
            name: service1
            port:
              number: 80
  - host: bar.foo.com
    http:
      paths:
        path: "/"
        backend:
          service:
            name: service2
            port:
              number: 80
```

### Configuring TLS Certificate
```
spec:
  tls:
  - hosts:
      - https-example.foo.com
    secretName: testsecret-tls
```
secret
```
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
  namespace: default #needs to be the same namespace as ingress
data: #keys need to be names like this
  tls.crt: base64 encoded cert 
  tls.key: base64 encoded key
type: kubernetes.io/tls
```

## Volumes
- no data persistence out of the box
- if pod dies -> data is gone
- storage needs to be available on all nodes because we do not know where a pod (re)starts
- needs to survive when whole cluster crashes
- for DB or files

### Persistent Volume
- a cluster resource, created via yaml file
- needs actual physical storage (internal/external/cloud)
- K8s only offers the interface to the actual storage; which type of storage is needed needs to be decided by project/application needs
- also: storage needs to be created & managed outside of k8s
- are not namespaced! accessible by whole cluster

Local Volume Types
- violate requirements for data persistence: 1) tied to a specific node & 2) do not survice cluster crash

Remote Volume Types
- should be used to have data persistence

### Persistent volume claim
- Cluster Admin needs to create access to a volume (in the cluster or cloud)
- Application has to claim the Persistent volume
- this is done using a PVC -> defined in yaml
- in yaml, specific specifications are set (size, access mode, ..) -> which volume satisfies this claim will be used
- this PVC needs to be used in the pod specification to mount the volume to the pod
- this volume is then mounted to the container
```
spec:
    containers:
    - name: mysql
      image: mysql
      volumeMounts:
      - mountPath: /var/lib/mysql
        name: site-data
        subPath: mysql
    volumes:
    - name: site-data
      persistentVolumeClaim:
        claimName: my-lamp-site-data
```

### Benefits of Abstractions
- separation of concerns -> devs to not need to cary about the volume in detail

### Storage Class
- to avoid a confusing structures especially in big clusters
- provisions persistent volumes dynamically.. when PVC claims it
- Each StorageClass has a provisioner that determines what volume plugin is used for provisioning PVs
- internal provisioner (offerned by kubernetes) -> kubernetes.io
- external provisioner
- StorageClass = basically another abstraction level that abstracts the underlying storage provider

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: storage-class-name
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io1
  iopsPerGb: "10"
  fsType: ext4 
```
- is used in the PVC config
```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mypvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
  storageClassName: storage-class-name 
```
- Hierachy: Pod claims storage via PVC -> PVC requests storage from SC -> SC creates PV that meets the needs of the claim

### Empty Dir Volume
- is not a persistent volume
- lives as long as the pod is running
- is created when the pod is created
- ideal for temporary storage such as redis cache
```
volumes:
  - name: redis-data
    emptyDir: {}
```

## ConfigMap & Secret Volume Types
- volume types that are treated differently
- both are local volumes, but they are not managed by PVC, but by kubernetes itself with their own config files
- how to pass config files, containing sensitive data (for example for external services such as nginx or javascrip app properties) to kubernetes pods?
- ConfigMap & Secret are Local Volume Types

### ConfigMap and Secret for Mounting Files

- configMap and Secret cannot only be used to reference key value pairs, but also to mount files
-> see 10_kubernetes/12-ConfigMap-SecretVolume-Types


## StatefulSet
- stateful application = any application that stores data to keep track of state -> f.e. Databases; deployed using StatefulSet component
- stateless: each request is completely new; can connect to a statful application; deployed using Deployment
- to deploy StatefulSet either:
    - create all configuration files manually
    - use bundle of config files (f.e. Helm)

### Deployment vs StatfulSet
- replicating stateful applications is more difficult
- -> stateless pods are identical and interchangable; created/deleted in random order with random hashes; one service that load balances to any pod
- -> stateful pods cannot be created/deleted at the same time and cannot be randomly addressed because the replica pods are not identical. each pod has its own identity -> persistent identifier
- this persistent identifier is needed because there is only one main pod that updates data
- when db applications are scaled, only one pod is used to write, the other pods (replicas) are used to read data
- the pods do not use the same physical storage
- at any time, each pod must have the same data as the others -> contiously synchronized -> must be updated about each change


Pod State

- a pod can die, but the persistent volume is not coupled -> if a pod dies the PV gets re-attached to the same pod identifier
- important to use remote storage because local volumes storage is tied to a specific node

Pod Identity

- fixed ordered names (mysql-0, 1, 2, 3, ..)
- next pod is only created from previous and only created if the previous is up and running
- deletion is done reverse order
- each pod has an individual dns endpoint from service (f.e. mysql-0.svc2)
- -> when a pod restarts the ip address changes, but name and endpoint stay the same


## Managed Kubernetes Service (K8s in cloud)
- unmanaged cluster: spinning up a cluster from scratch, using (virtual) servers, setup up k8s, nodes, .. -> everything needs to be managed -> big overhead
- managed k8s service
    - most is done automatically
    - f.e. just choose how many worker nodes are needed
    - everything is pre-installed
    - control plane nodes are completely managed by platform (f.e. linode)
    - also storage should be handled automatically (depending on platform)
    - cloud provider's node balancer to scale / load balance
    - session stickiness -> one user will only land on the same client backend for subsequent requests (which is a huge win)
    - ssl via cert-manager
    - dependent on one cloud provider's features -> app gets closely tied to one provider, moving made difficult (vendor lock-in)

- setup & team grows -> automation is needed for creating, configuring etc -> terraform/ansible -> can also work with cloud provider

## Helm Package Manager

### Package Manager for Kubernetes
- Bundle of Yaml files
- use existing helm charts (for applications)
- or create own helm charts
- on public repositories such as artifact hub or search using helm search KEYWORD
- companies often use private registries

### Templating Engine
- f.e for multiple microservices most of Deployment and Service configurations are almost the same
- it makes no sense to create own files for minor changes such as the name
- -> Helm chart can define a common blueprint (template yaml config)
- -> dynamic values are replaced by placeholders (coming from another file values.yaml)
- instead of multiple yaml files -> just one yaml file
- practical for ci/cd -> values are replaced on the fly

### Same applications across different environments
- considering dev/stage/prod stage
- can share the same yaml file, but just replace env specific values

### Helm structure
- top level folder: name of chart
- Chart.yaml: meta info about chart
- values.yaml: values for the template files with default values
- charts folder: dependencies
- templates: the actual template files

```sh
helm install NAME
helm install --values=my-valuey.yaml NAME # install with own values file
helm upgrade NAME
helm rollback NAME

```

### Release Management
- keep track of chart executions
- all changes applied (for example update) are tracked and can be rollbacked


### Add Helm repository
`helm repo add bitnami https://charts.bitnami.com/bitnami` -> is executed against the cluster the machine is connected to (uses kubectl)
`helm search repo bitnami/mongodb`
check chart details https://github.com/bitnami/charts/tree/main/bitnami/mongodb 
``

## Demo Project Helm Demo

see Demo Readme

Flow:

- hostname, configured in ingress, is resolved  to ip address of NodeBalancer
- ingress controller resolves the rule and forwards request to internal mongoexpress service


## Deploy Image in Kubernetes from private Docker repo
worflow:
- commit triggers CI build
- CICD tools (jenkins) pushes to private registry
- -> how to get this image in the kubernetes cluster?

1. create secret component with docker registry credentials (manually by copying docker config data or using kubectl create secret)
2. use secret using imagePullSecrets

see 17-deploying-images-from-private-docker-repo

docker-secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: my-registry-key
data:
  .dockerconfigjson: BASE64 encoded string of docker config
type: kubernetes.io/dockerconfigjson
```

in deployment.yaml
```
# ...
  template:
    metadata:
      labels:
        app: my-app
    spec:
      imagePullSecrets:
        - name: my-registry-key # this key is used to pull the image from the private registry
      containers:
        - name: my-app
          image: NAME #replace with full image name: <your-repo>/<your-image>:<tag>
          imagePullPolicy: Always # force to pull the image from the registry, even if it already exists on host machine
          ports:
            - containerPort: 3000
```

## K8s operator
- mainly used for stateful operations
- for stateful applications each pod has its own state and identity, the order in which pods get added/deleted matters
- also, for each application (mysql, postgresql, elastiscsearch) the process is different -> no standard solution
- manual intervention is needed for stateful applications,  which is against the k8s idea
- -> operator solves this problem
- does the manual tasks
    - how to deploy the app
    - how to create cluster of replicas
    - how to recover
- task are automated and re-usable
- operator has the same control loop mechanism as k8s
- uses CRDs (custom resource definitions) = custom K8s component
- sets the domain/app specific knowledge on top of the core k8s concept/lifecycle
- operators exist for each appliction (f.e. mysql, postgresql, ..) -> created by domain experts (community, f.e. zalando)

## Authorization with RBAC
- role based access control
- least privilege rule -> should only have privileges they need
- role component
    - bound to namespace
    - define what resources can be accessed
    - what actions can be performed
- rolebinding component
    - binds role to user or group
    - can be used to bind role to service account
- clusterrole and clusterrolebinding
    - same as role and role binding (to admin group), but for the whole cluster
    - used for k8s admins
- how to create users/groups
  - relies on external sources such as static token files, certificates or 3rd party identity service (ldap)
  - api server needs to be configured to use these sources
- service accounts
  - not only people, but also applications can access the cluster
  - can be inside and outside the cluster (f.e. jenkins)
  - -> k8s service account component is used
- to check access of current user using can-i
  - `kubectl auth can-i get pods --as user --namespace default`
example of a role
```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"] # components such as Pods, Deployments, ..
  verbs: ["get", "watch", "list"] # actions that can be performed
  resourceNames: ["my-pod"] # more granular, only this pod can be accessed
```

## Microservices
- smaller independent applications
- less interconnected services
- how do they communicate?
  - service to service api calls
  - message broker (f.e. redis)
  - service mesh architecture -> each ms has its own helper application (f.e. istio)
- information needed from dev team
  - what microservices
  - which ms is talking to which
  - how are they talking
  - which database is used
  - on which port does each ms run
  - which ms is exposed to the outside
  - which env variables are expected
- prepare environment
  - deploy needed 3rd party services
  - create secrets and configmaps
- create deployment and service for each ms
  - decide if ms in same namespace or each ms in its own namespace


## Kubernetes best practices

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

### Always use more than 1 worker node in the cluster
- single point of failure with just one node
- even in simple applications
- each replica should run on a different node!

### Use labels for resources
- labels are key value pairs attached to k8s components, giving them custom identifier for other components

### Using Namespaces
- better organization in the cluster
- also good for access rights based on namespaces

## Security Best Practices

### Ensure Images are free of vulnerabilities
- third party is always a risk
- do manual or automatic checks (in build pipeline)

### No root access for containers
- containers should not run as root because it causes security risks
- in non-official images always check if it is running as root

```yaml
  securityContext:
    privileged: true # <-- dont do that
```

### Update cluster to latest K8s version
- security patches are important

## Use Helm Chart for Microservices
two ways:
- helm chart for each microservice, if the configurations are very different
- one shared helm chart for all microservices
- the two approaches can also be combined (use shared charts for common configurations and separate charts for specific configurations)

### Setup helm and File structure
- start with `helm create NAME` -> creates a new helm chart
- Chart.yaml: meta info about chart
- values.yaml: values for the template files with default values
- charts folder: dependencies
- templates: the actual template files
- .helmignore: files that should not be included in the chart/build

#### Values object
in a template file such as deployment.yaml
```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Values.name }}
```
The values can be passed in the values object:
- in the values.yaml file
- in a user supplied values file with -f flag
- in the command line with --set flag

The helm engine will then replace the placeholders with the values
- values should be named in camelCase
- can be defined flat or nested
  - appName vs app.name
  - attention: nested values are not easy to set from the command line

#### Environment variables in Helm
using range which is a go template function in a for-each-style loop
```yaml
    spec:
      containers:
        - name: {{ .Values.appName }}
          image: "{{ .Values.appImage }}:{{ .Values.appVersion }}"
          ports:
            - containerPort: {{ .Values.containerPort }}
          env:
              {{- range .Values.containerEnvVars}}
        - name: {{ .key }}
          value: {{ .value | quote }}
              {{- end}}
```
```yaml
containerEnvVars:
- name: ENV_VAR_ONE
  value: "valueone"
- name: ENV_VAR_TWO
  value: "valuetwo"
```
#### Values file
a yaml file that has the default values, which will mostly be overwritten by the application specific values

### Helm commands

```sh
helm create NAME
helm template -f FILE NAME #render chart template locally and display the output
helm template -f values/redis-values.yaml charts/redis/ # example
helm lint NAME # checks for errors
helm install NAME # install chart
helm install -f email-service-values.yaml emailservice microservice # install with own values file
helm install --dry-run ... #check generated manifest without installing the chart
helm ls # list all releases
helmfile sync # applies a helmfile
helmfile destroy # deletes all releases
```

### Deploy Helm to cluster
we can either 
- run helm install manually / using a script file (quite inefficient)
```sh
helm install -f values/email-service-values.yaml emailservice charts/microservice
helm install -f values/cart-service-values.yaml cartservice charts/microservice
helm install -f values/currency-service-values.yaml currencyservice charts/microservice
# ...
```
- or using a Helmfile (more elegant)
  - declarative way for deploying helm charts
  - yaml file
```yaml
releases:
  - name: rediscart
    chart: charts/redis
    values:
    - values/redis-values.yaml
    - appReplicas: "1"
    - volumeName: "redis-cart-data"

  - name: emailservice
    chart: charts/microservice
    values:
    - values/email-service-values.yaml
# ...
```

### Where to host helm files
- should be hosted in a git repository
- part of Infrastructure as code
- can be done:
  - with application code
  - in a separate repository (preferred)
