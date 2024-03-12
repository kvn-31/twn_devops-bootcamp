## Steps

1. Create EKS IAM Role
2. Create VPC for Worker Nodes
3. Create EKS Cluster (Control Plane nodes)
4. Connect kubectl with cluster
5. create EC2 IAM role for node group
6. Create Node Group (Worker nodes) and attach to EKS Cluster
7. Configure auto scaling
8. Deploy application to EKS Cluster

> Important: create the AWS resources using the same user as the one used in the CLI.
> 
> Also: the chosen settings of this cluster, just needed to fit for the demo. In a real world scenario, the settings might be different.

### Create EKS IAM Role
- Create Role - AWS Service - EKS-Cluster - Permissions: AmazonEKSClusterPolicy

### Create VPC for Worker Nodes
- default VPC is not optimised for EKS because we need to implement K8s and AWS specific networking rules
- the VPC is created for the worker nodes, not the control plane
- we need specific firewall config to allow communication between the control plane and the worker nodes
- EKS is running on a different VPC -> managed by AWS
- Worker Nodes are running in our VPC -> managed by us
- best practice: configure private and public (Elastic load balancer) subnets
- through the IAM role, Kubernetes can change VPC configurations
- as a lot of rules need to be implemented, the easiest is to use a CloudFormation template
- in this case we use a [template](https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml) that creates private and public subnets
- Create VPC 

### Create EKS Cluster (Control Plane nodes)
- Create EKS Cluster
- Cluster service role: choose the one created in the first step
- VPC: choose the vpc created in the second step and the security group
- Cluster Endpoint Access:
  - public access: The cluster endpoint is accessible from outside your VPC. Worker node traffic will leave your VPC to connect to the endpoint.
  - private access: cluster endpoint is only accessible from the VPC; means we would need to install kubectl on the worker nodes and connect to it
  - public and private: the cluster endpoint is accessible from outside the vpc, worker nod traffic will stay withing vpc <-- chosen
- Add-Ons: CoreDNS, kube-proxy, vpc-cni

### Connect kubectl with cluster
- `aws eks update-kubeconfig --name NAME` create a kubeconfig file that allows us to connect to the cluster
- `kubectl cluster-info` to verify the connection

### Create EC2 IAM role for node group
- worker nodes run worker processes such as Kubelet
- Kubelet (k8s agent  that schedules and manages pods) needs the permission to execute all these tasks
- Create role - EC2 - Policies:
  - AmazonEKSWorkerNodePolicy
  - AmazonEC2ContainerRegistryReadOnly # needed to pull images from ECR
  - AmazonEKS_CNI_Policy # needed for the CNI (common network interface) = internal networking -> communicate with other worker nodes etc

### Create Node Group (Worker nodes) and attach to EKS Cluster
- we need to create worker groups and connect to the control plane
- in compute tab - create node group
  - IAM role: the one created in the previous step
  - AMI type: Amazon Linux 2
  - Capacity type: On-Demand
  - Instance type: t3.small
  - Disk size: 20GB
  - Desired size: 2 -> auto-scaling -> when load increases, more nodes are added
  - Min size: 2
  - Max size: 2
  - networking
    - subnets should be automatically selected
    - Enable Configure remote access to nodes
- Can always be scaled up increasing the node group scaling configuration
- With node group all necessary processes are installed (containerd, kubectl, ..)
      
## Configure auto scaling
- auto-scaling group was automatically created with the node group in aws
- ec2 instances inside the worker node need permissions to communicate with the auto-scaling group -> create policy
- create policy - JSON - paste the following:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:DescribeLaunchConfigurations",
        "autoscaling:DescribeTags",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup",
        "ec2:DescribeLaunchTemplateVersions"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
```
- attach policy to the existing node group IAM role
- edit the `cluster-autoscaler-autodiscover.yaml` file to the needs (or follow the instructions below for a later edit)
- `kubectl apply -f cluster-autoscaler-autodiscover.yaml` apply cluster autodiscover from https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
- `kubectl edit deployment -n kube-system cluster-autoscaler` <-- this edit is only needed if the `cluster-autoscaler-autodiscover.yaml` was not edited beforehand
  - add `cluster-autoscaler.kubernetes.io/safe-to-evict: "false"` metadata/annotations
  - replace `YOUR-CLUSTER-NAME` with the actual cluster name
  - below ^this line add
  ```
  - —balance-similar-node-groups
  - —skip-nodes-with-system-pods=false
    ```
  - replace the version in `image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.XX.X` to match the current kubernetes version running in the cluster
    - to do this, find the appropriate version here: https://github.com/kubernetes/autoscaler/tags
- `kubectl get pod -n kube-system` find the name of the cluster autoscaler pod
- `kubectl logs -n kube-system AUTOSCALER-POD` check the logs

## Deploy application to EKS Cluster
we want to create an external service (type LoadBalancer) with an AWS (cloud-specific) load balancer attached to it
- `kubectl apply -f nignx-config.yaml`
- -> in aws ec2 a load balancer has automatically been created

## Test the scaling under artifical load
- `kubectl edit deplyoment nginx` - increase replica count to 20 -> pods get created -> resources are not enough (some are in pending state) -> autoscaler needs to configure additional ec2 instances 
- `kubectl get nodes` -> nodes should have spun up
