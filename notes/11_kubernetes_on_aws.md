# Kubernetes on AWS

## Container Services on AWS
- how to manage containers once deployed to AWS ecr2?
- -> need an automation tool like docker swarm, kubernetes, mesos, nomad, ..
- aws provides ECS (Elastic Container Service) and EKS (Elastic Kubernetes Service)

### ECS
- ecs cluster contains all services used to manage containers
- ecs offers a control plane
- benefits
  - for less complex applications
  - ecs control panel is free

### ECS (Elastic Container Service) using EC2
- the virtual machines run on ec2 instances, connected to the ecs cluster
  - container runtime
  - ecs agent (connects to the ecs cluster)
- downsides: the virtual machines still need to be managed, also server operating system updates, docker runtime etc
- benefit: full access and control of infrastructure

### ECS hosted on AWS Fargate
- if we also want to delegate infrastructure management to AWS, we can use Fargate
- alternative to ec2 instances
- instead of creating ec2 instances, we create fargate instances and connect to the ecs cluster
- no need to provision and manage servers
- fargate analyses containers and automatically provisions the required resources
- benefit: no need to manage infrastructure, on demand, only infrastructure used is paid for, scales up and down without fixed resources defined beforehand
- downside: less control over infrastructure

### EKS (Elastic Kubernetes Service)
- alternative to ECS
- manages kubernetes clusters
- benefits 
  - not locked into aws, can use kubernetes on other cloud providers
  - easier to migrate (depending on how many aws services are used)
- eks deploys and manages kubernetes control plane nodes
- k8s control plane services already installed on them and fully managed by aws
- high availability - control plane nodes replicated across multiple availability zones
- we can use ec2 instances or fargate even on the same cluster

### EKS with EC2 instances
- self-managed
- -> need to manage infrastructure for worker nodes
- can have multiple pods on once virtual machine/instance

### EKS with NodeGroup
- semi managed
- worker nodes are grouped in a node group
- aws creates, deletes ec2 instances, but we need to configure the node group
- no auto scaling

### EKS with Fargate
- fully managed worker nodes
- serverless -> no ec2 instances
- 1 pod per virtual machine
- all the vms created are running in aws managed account, not in our account
- limitation: no support for stateful applications, no support for DaemonSets

Fargate Profile
- applies pod selection rules which specify which pods should use Fargate

### EKS cluster - using both Fargate and NodeGroup
- we can use both fargate and nodegroup in the same cluster
- for example if we want to use fargate, but also need to support stateful applications

### Create an EKS cluster
steps:
- provision eks cluster
- create worker nodes (f.e. nodegroup of ec2 instances or fargate)
- connect node group to eks cluster
- deploy applications to eks cluster

## Amazon ECR
- repository for storing, managing, and deploying docker images
- alternative to docker hub or nexus
- benefits
  - fully integrated with aws
  - easy to connect and configure
- downside: only works with aws

## Setup an EKS cluster
see [README.md](..%2Fexercises%2F10_kubernetes_on_aws%2F02-create-eks-cluster%2FREADME.md)

### Auto-scaling
- after creating a node group, an auto-scaling group is automatically created
- it will automatically add/remove instances depending on the load
- tradeoff:
  - save costs, but ...
  - provisioning new ec2 instance takes time

## Cleanup EKS cluster
- remove nodegroups and fargate profiles
- delete cluster
