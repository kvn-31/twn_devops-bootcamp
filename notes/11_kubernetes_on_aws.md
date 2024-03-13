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
- delete roles not used anymore
- delete cloudformation stacks (will remove vpc, subnets etc)

## EKS cluster with eksctl
- before we created the cluster manually (see [README.md](..%2Fexercises%2F10_kubernetes_on_aws%2F02-create-eks-cluster%2FREADME.md))
- takes time, not easy to replicate
- one of the easiest way to automate the creation of an EKS cluster is using eksctl (eks control)
- cluster will be created with default settings, but can be customized using cli options or a configuration file (yaml)

### Setup eksctl
- install using `sudo pacman -S eksctl` or system equivalent
- configure aws credentials

### Create EKS cluster with eksctl
These option will pretty much create the same cluster as in the previous example
```bash
eksctl create cluster \
--name demo-cluster \
--version 1.29 \
--region eu-central-1 \
--nodegroup-name demo-nodes \
--node-type t2.micro \
--nodes 2 \
--nodes-min 1 \
--nodes-max 3
```
The execution of this command will take a while (up to half an hour)

## Deploy to EKS from Jenkins
- we can use Jenkins to deploy to EKS
- steps to configure:
  - install kubectl in the jenkins container
  - install aws-iam-authenticator in the jenkins container (was installed in local machine automatically with eksctl)
  - create kubeconfig to connect to eks cluster
  - adjust Jenkinsfile to deploy to eks cluster

### Setup Jenkins (Docker) to deploy to EKS
- exec into the jenkins container as root
- install kubectl: download latest stable version of kubectl, chmod and move executable `curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl; chmod +x ./kubectl; mv ./kubectl /usr/local/bin/kubectl`
- install aws-iam-authenticator:
```bash
curl -Lo aws-iam-authenticator https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_linux_amd64
chmod +x ./aws-iam-authenticator
mv ./aws-iam-authenticator /usr/local/bin 
```
- create kubeconfig file
  - we will create the kubeconfig outside of the container on the host and then copy it into the container
  - use the template `config.yaml` taken from aws documentation
    - copy the contents of the `config.yaml` into a new file on the host (f.e. `vim config`)
    - replace `cluster-name` with the name of the eks cluster
    - replace `endpoint-url` with the api server endpoint url of the eks cluster
    - replace `certificate-authority-data` with the certificate-authority-data of the eks cluster (can be taken from local machine if already connected `~/.kube/config`)
    - exec into the jenkins container (as normal user, not root), cd ~ and print the path -> this is the home directory of the jenkins user
    - `mkdir .kube`
    - exit the container and on host machine copy the `config` file into the `.kube` directory of the jenkins user using `docker cp config "YOUR DOCKER CONTAINER ID":/var/jenkins_home/.kube/`
  - best practice: create AWS IAM user for Jenkins with limited permissions

Jenkins
- prerequisite: running pipeline job (in this case multi branch pipeline job)
- add credentials for the aws user to the pipeline job credentials
  - aws credentials (can be grabbed from local machine cat ~/.aws/credentials): 
    - secret: actual key id + id: for example -> jenkins_aws_access_key_id
    - secret: actual secret key + id: for example -> jenkins_aws_secret_access_key

Jenkinsfile
- Configure something like this
```
stage('deploy') {
            environment {
                AWS_ACCESS_KEY_ID = credentials('jenkins_aws_access_key_id')
                AWS_SECRET_ACCESS_KEY = credentials('jenkins_aws_secret_access_key')
            }
            steps {
                script {
                   echo 'deploying docker image...'
                   sh 'kubectl create deployment nginx-deployment --image=nginx'
                }
            }
        }
```
