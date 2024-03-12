# Create Fargate Profile for EKS cluster

## Introduction
This is an extension of [02-03-create-eks-cluster-with-autoscaling](..%2F02-03-create-eks-cluster-with-autoscaling%2FREADME.md).
We will create a Fargate profile for the EKS cluster, that runs next to our EC2 instances.

## Create IAM Role for Fargate
- Create Role - AWS Service - EKS-Fargate pod - Permissions: AmazonEKSFargatePodExecutionRolePolicy
- Add Fargate Profile to EKS Cluster (Compute Tab)
  - set the namespace as we have in `nginx-config-fargate.yaml`
```yaml
  namespace: dev
```
  - set the selectors (key:value pairs) -> profile:fargate
```yaml
      labels:
        app: nginx
        profile: fargate
```
- wait till the profile is created
- apply the `nginx-config-fargate.yaml` to the cluster
```bash
kubectl create ns dev
kubectl apply -f nginx-config-fargate.yaml
```

