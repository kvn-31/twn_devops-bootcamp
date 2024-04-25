provider "aws" {
  region = "eu-central-1"
}

variable vpc_cidr_block {}
variable private_subnet_cidr_blocks {}
variable public_subnet_cidr_blocks {}

# query the availability zones available in the specified region (see provider definition)
data "aws_availability_zones" "azs" {}

module "myapp-vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.0"

  name            = "myapp-vpc"
  cidr            = var.vpc_cidr_block
  private_subnets = var.private_subnet_cidr_blocks
  public_subnets  = var.public_subnet_cidr_blocks
  azs             = data.aws_availability_zones.azs.names

  enable_nat_gateway = true
  # creates shared nat gateway for all private subnets -> all private subnets must route through this single nat gateway
  single_nat_gateway   = true
  enable_dns_hostnames = true

  tags = {
    "kubernetes.io/cluster/myapp-eks-cluster" = "shared" # k8s ccm can detect and use this tag to identify the vpc
  }

  public_subnet_tags = {
    "kubernetes.io/cluster/myapp-eks-cluster" = "shared" # k8s ccm can detect and use this tag to identify the subnets
    "kubernetes.io/role/elb" = "1" # elb = elastic load balancer -> for public subnets
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/myapp-eks-cluster" = "shared" # k8s ccm can detect and use this tag to identify the subnets
    "kubernetes.io/role/internal-elb" = "1" # internal elb = internal elastic load balancer -> for private subnets
  }
}
