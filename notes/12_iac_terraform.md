# Terraform
- IAC (Infrastructure as Code)
- before we were created the cloud infrastructure manually (manually create EKS, VPC, EC2 instances, ...)
- IAC enables us to create, update, delete, replicate (dev vs stage vs prod) infrastructure in a programmatic way
  - easier collaboration
  - version control
  - automation
  - documentation
- automate and manage infrastructure
- open source, declarative language
- provisioning infrastructure (<-- terraform) and deploying applications are two separated tasks, might be done by different teams

## Ansible vs Terraform
- they might sound like the same tools, but are for different purposes
- both: IaC
- Ansible: mainly configuration management tool
  - install/update software, configure operating systems, automate repetitive tasks
  - more mature
- Terraform: mainly provisioning tool
  - create, update, delete infrastructure
  - uses its own language (HCL)
  - relatively new
- common practice: use both tools together

## Terraform Architecture
2 main components:
- Terraform Core
  - responsible for reading configuration files, providing an execution plan, and applying changes
  - has two input sources: configuration files and state
  - core takes input and figures out what actions are necessary to achieve the desired state
  - uses providers to execute the plan
- Providers
  - for specific technologies such as AWS, Azure (IaaS), Kubernetes (PaaS), Fastly (SaaS)
  - each provider enables access to resources (Kubernetes -> namespaces etc)

### Terraform Configuration Files
- The Terraform language is declarative -> describing an intended goal rather than the steps to reach that goal (imperative)
- order of blocks and the files is generally not significant
- Terraform only considers implicit and explicit relationships between resources when determining an order of operations
```hcl
# this file makes no sense and should just show the syntax
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 1.0.4"
    }
  }
}

variable "availability_zones" {
  description = "A list of availability zones in which to create subnets"
  type = list(string)
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  # Referencing the base_cidr_block variable allows the network address
  # to be changed without modifying the configuration.
  cidr_block = var.base_cidr_block
}
```

### Terraform Commands
- `refresh` - update the state file with the real-world infrastructure
- `plan` - create / show the execution plan to achieve the desired state
- `apply` - apply the execution plan
- `destroy` - destroy the resources/infrastructure
