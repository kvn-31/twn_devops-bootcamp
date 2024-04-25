module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.5"

  cluster_name = "myapp-eks-cluster"
  cluster_version = "1.27" # Kubernetes version
  cluster_endpoint_public_access = true # needed to access with kubectl, not secure for production

  enable_cluster_creator_admin_permissions = true # needs to be added in order to be able to access the cluster with kubectl

  subnet_ids = module.myapp-vpc.private_subnets # private subnets to handle the workload
  vpc_id = module.myapp-vpc.vpc_id

  eks_managed_node_groups = {
    dev = {
      min_size       = 1
      max_size       = 3
      desired_size   = 2

      instance_types = ["t2.small"]
    }
  }

  # optional tags
  tags = {
    environment = "development",
    application = "myapp"
  }
}
