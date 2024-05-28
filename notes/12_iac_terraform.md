# Terraform

- IAC (Infrastructure as Code)
- before we were created the cloud infrastructure manually (manually create EKS, VPC, EC2 instances, ...)
- IAC enables us to create, update, delete, replicate (dev vs stage vs prod) infrastructure in a programmatic way
    - easier collaboration
    - version control
    - automation
    - documentation
- automate and manage infrastructure
- not open source anymore, open source alternative is f.e. openTofu
- provisioning infrastructure (<-- terraform) and deploying applications are two separated tasks, might be done by
  different teams
- it covers the part of creating and managing infrastructure (initial setup, manage infrastructure, initial application
  setup), but it does NOT/is not made to manage the actual application (running an update etc) -> might be a job for Ansible

## Installation

- see [official website](https://developer.hashicorp.com/terraform/install)
- on Manjaro Linux simplest way is to use a package manager like pacman `sudo pacman -S terraform`

## Ansible vs Terraform

- they might sound like the same tools, but are for different purposes
- both: IaC
- Ansible: mainly configuration management tool
    - install/update software, configure operating systems, automate repetitive tasks
    - more mature
- Terraform: mainly provisioning tool
    - create, update, delete infrastructure
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

- The Terraform language is declarative -> describing an intended goal rather than the steps to reach that goal (
  imperative)
    - -> this makes terraform idempodent -> apply the same configuration x times -> always the same result, no need to
      remember the current state
- order of blocks and the files is generally not significant
- Terraform only considers implicit and explicit relationships between resources when determining an order of operations

```tf
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
  type        = list(string)
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
- `init` - initialize repo, download providers
- `refresh` - update the state file with the real-world infrastructure
- `plan` - create / show the execution plan to achieve the desired state
- `apply` - apply the execution plan
    - `terraform apply -auto-approve` to skip the confirmation
- `destroy` - destroy the resources/infrastructure, automatically destroy in right order
    - `terraform destroy -target TYPE.NAME` to destroy a specific resource
- `state` - get info about state; update state etc
    - `list` - list resources in state
    - `mv` - move item in state
    - `pull`- pull current state
    - `push` - update remote state from local state file
    - `replace-provider` - replace a provider in the state
    - `rm` - remove instances from state
    - `show` - show resource in the state

## Providers

- Terraform uses providers to interact with the infrastructure providers (AWS, Azure, ...)
- is code that knows how to talk to a specific technology
- there are official, 3rd party and community providers
- are not integrated, need to be installed

### Install and connect to provider

providers.tf

```tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.40.0"
    }
  }
}
```

main.tf

```tf
provider "aws" {
  region     = "eu-central-1"
  access_key = "" #dont hardcode
  secret_key = "" #dont hardcode
}
```

Initialize to install providers

```bash
terraform init #in the folder where main.tf and providers.tf sit, automatically generates files to .terraform
```

### Resource

resource example, consists of resource keyword, type and name

```tf
resource "aws_instance" "web" {
  ami           = "ami-a1b2c3d4"
  instance_type = "t2.micro"
}

```

example to reference between resources

```tf

resource "aws_vpc" "development-vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "dev-subnet-1" {
  vpc_id = aws_vpc.development-vpc.id #reference resource defined in same context
}
```

Use `terraform apply` to create the resources

### Data sources

- data sources allow data to be fetched or computed for use elsewhere in Terraform configuration
- queries the actual data, while "resource" creates new components

```tf
#data source to filter vpc with custom name "existing_vpc"
data "aws_vpc" "existing_vpc" {
  #arguments to filter vpc
  default = true
}

resource "aws_subnet" "dev-subnet-1" {
  vpc_id            = data.aws_vpc.existing_vpc.id #reference data source defined in same context
  cidr_block        = "10.0.10.0/24"
  availability_zone = "eu-central-1a"
}
```

### Provider, Resource, Data

- provider is like importing a library
- resource/data is like a function using this library
    - resource creates something
    - data fetches something that was already created

## Changing Resources

- resources can be named using tags (key-value pairs in aws)
- to change the name

```tf
resource "aws_vpc" "development-vpc" {
  cidr_block = "10.0.0.0/16"
  tags       = {
    Name : "development" #Name key is reserved for name of the resource
  }
}
```

- to remove a resource, just remove it from the configuration file and run `terraform apply` <-- better way
- alternatively use `terraform destroy -target TYPE.NAME` to remove <-- not recommended because the configuration file
  is not updated after destroying the resource

## Terraform State

- how does Terraform keep track of the current state?
- `terraform.fstate` - file that gets generated on apply and stores state of real world resources in managed
  infrastructure
- `terraform.fstate.backup` - stores the previous state
- `terraform state ACTION` can be used to get detailed info or update state
- normally should not be changed, but applied by terraform with the config file

## Output Values

- are like function return values
- which values should be returned after creation?
- one value per output

```tf
output "dev-vpc-id" {
  value = aws_vpc.development-vpc.id
}
```

after running `terraform apply`

```bash
#...
Outputs:
dev-vpc-id = "vpc-..."
```

## Variables

- can be passed as parameter for values that are used multiple times
- also for different environments, where env specific values are passed from outside
    - for this multiple tfvars file would be created, then file name needs to passed for apply
- 3 ways to pass value to a variable
    - `terraform apply` -> prompt to enter a value, for testing / trying out new values
    - `terraform apply -var "VARNAME=10.0.30.0/24"` command line argument
    - defining variables files `terraform.tfvars` -> file with this name is automatically picked up by terraform, best
      practice

main.tf

```tf
variable "subnet_cidr_block" {
  description = "subnet cidr block"
}

resource "aws_subnet" "dev-subnet-1" {
  cidr_block = var.subnet_cidr_block
}
```

terraform.tfvars

```tf
subnet_cidr_block = "10.0.40.0/24"
```

### Default values and Type constraints

```tf
variable "subnet_cidr_block" {
  description = "subnet cidr block"
  default     = "10.0.0.0/16" #will be used if terraform cannot find a value
  type        = string #type, can be string, number, bool, object, array etc
}
```

More detailed type constraints

```tf
variable "cidr_blocks" {
  description = "cidr blocks"
  type        = list(object({
    cidr_block = string
    name       = string
  }))
}

resource "aws_vpc" "development-vpc" {
  cidr_block = var.cidr_blocks[0].cidr_block
}
#####
###
tags       = {
  Name : "${var.env_prefix}-vpc" #<-- string interpolation
}
###
```
tfvars
```tf
cidr_blocks = [
  {cidr_block = "10.0.0.0/16", name = "dev-vpc"},
  {cidr_block = "10.0.10.0/24", name = "dev-subnet"}
]
```

## Environment Variables
- credentials must not be hardcoded and checked into a repository, but can be defined as env variables
- different ways to set
  - `export KEY=VALUE` then `terraform apply` -> terraform is able to pick it up; limited to context; good for testing purposes
  - globally configured credentials (for example aws after running aws configure), depends on provider which env variables can be picked up
  - using TF environment variable `export TF_VAR_avail_zone="eu-central-1a"` -> TF_VAR prefix tells terraform to pick it up 
```tf
variable avail_zone {
} #automatically picks up TF_VAR_avail_zone, if it is set
```

## Git
- do not check in
  - .terraform
  - state files
  - tfvars -> might contain sensitive data, might be different for each team member


## Best practices
- create infrastructure from scratch
- leave default created by AWS as is (like default VPC)
- create as much as possible with IaC to be able to delete and replicate later -> less manual actions needed

## Automate AWS EC2 Key Pair Creation
- normally we would need to manually create a keypair in aws console, download, chmod400, add to ssh agent, ..
- with terraform we can automate this process

```tf
resource "aws_key_pair" "ssh-key" {
  key_name = "server-key"
  public_key = file(var.public_key_location) #path to public key
}

# ...
# reference the key pair in the instance
resource "aws_instance" "web" {
  ami           = "ami-a1b2c3d4"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.ssh-key.key_name
}
```

```bash
ssh -i /path/to/private/key ec2-user@public-ip
# or if using the default key
ssh ec2-user@public-ip
```

## Execute commands on EC2 instance (on creation)
Important to know: this command is handed over to the cloud provider (f.e. aws) and is executed after terraform is finished -> terraform has no control.
We only get the info about it with ssh to the server and debugging.
```tf
resource "aws_instance" "myapp-server" {
  user_data                   = file("entry-script.sh")
  user_data_replace_on_change = true # -> instance is destroyed and recreated if user_data changes
}
```

## Provisioners
- provisioners can be used for behaviors that cannot be achieved with terraform
- they are not recommended and should be used as last resort
- there may be unexpected behavior
- breaks concept of idempotency (running the same command multiple times should have the same result)

### Provisioner - Remote Exec - Alternative to User Data
- remote-exec provisioner is used to execute a script on a remote machine after it is created
- it connects via ssh using Terraform

### Provisioner - File
- to copy files to the remote machine
- source - source file or folder
- destination - absolute path
```tf
provisioner "file" {
    source = "entry-script.sh"
    destination = "/home/ec2-user/entry-script-on-ec2.sh"
  }
```

### Provisioner - Local Exec
- invokes a local executable after a resource is created -> locally not on the created resource
- alternative: use Local provider by Hashicorp


### Alternatives to Provisioners
- as stated above provisioners should not be used as they break the concept of idempotency
- alternatives:
  - use a configuration management tool like Ansible/puppet
  - execute scripts separate from terraform (f.e. as ci cd step)

### Provisioner Failure
- if a provisioner fails, the resource is marked as tainted and will be recreated on the next apply
- it might still be created and running

## Modules
- without modules:
  - huge file
  - no overview
  - complex configurations
- modules are like functions in programming
  - input variables like function arguments
  - output values like return values
- a module groups resources together
- instead of creating modules, we can use existing modules (f.e. from the terraform registry)
- by referencing a module the needed providers are automatically installed using terraform init
- -> modules have provider dependencies
- common practice:
  - main.tf
  - outputs in outputs.tf
  - variables in variables.tf
  - providers.tf
- files do not need to be linked, Terraform automatically picks them up

### Create a module
- in /modules create a folder with the module name
- create main.tf, variables.tf, outputs.tf, ...
- structure: root module + child modules sitting in /modules
  - child module: module that is called by another configuration
- terraform init needs to be run after adding and referencing a module in root

### Module Input
- input variables are defined in module/variables.tf
- they are passed to the module in the root module
- the module uses the input variables to create resources

```tf
module "myapp-subnet" {
  source = "./modules/subnet"
  avail_zone = var.avail_zone
  default_route_table_id = aws_vpc.myapp-vpc.default_route_table_id
}
```

### Module Output
- if we need to pass values from the module to the root module/or another module we need the output
- output is like a return value of a function
- defined in module/outputs.tf

```tf
output "subnet" {
  value = aws_subnet.myapp-subnet-1 #exports the whole object as output
}
```
- reference in root module
```tf
resource "aws_instance" "myapp-server" {
  subnet_id              = module.myapp-subnet.subnet.id
}
```

## Automate Provisioning EKS
- problem: no version control (history)
- no simple replication of infrastructure possible
- no simple clean-up

### Terraform in Jenkins (+AWS)
- create credentials in aws, add as secret in Jenkins
- install Terraform inside Jenkins container
  - ssh into server, exec into jenkins docker container as root
  - https://developer.hashicorp.com/terraform/install
- TF configuration to provision server
- adjust Jenkinsfile to run TF commands

set variable values from ci/cd pipeline
- use terraform env variables
- TF_VAR_name
```Jenkinsfile
        stage("provision server") {
            environment {
                TF_VAR_env_prefix = 'test'
            }
```
in Jenkinsfile
will set the defined variable env_prefix
```tf
variable env_prefix {
  default = "dev"
}
```

#### Reference output from TF in Jenkinsfile
- example: ip of dynamically created ec2 instance is needed for further steps
- output the ip in TF
- read the output in Jenkinsfile and save to env variable
```Jenkinsfile
EC2_PUBLIC_IP = sh(
              script: "terraform output NAMEOFOUTPUT",
              returnStdout: true
            ).trim()
```

### Remote State
- problem: working in a team/with ci cd pipeline, multiple people working on the same infrastructure having their own TF state
- -> each user/ci server must make sure to have the latest state
- solution: remote state
  - store the state in a remote location (f.e. S3 bucket)
  - all users/ci servers can access the state
  - state is backed up

```tf
terraform {
  required_version = ">= 0.12"
  backend "s3" {
    bucket = "kvn-tf-s3-bucket" # bucket has to be created in aws before
    key    = "myapp/state.tfstate"
    region = "eu-central-1"
  }
}
```


## Best Practices
- Only change state file through terraform commands - never directly edit it
- Always use remote state
- Use state locking -> lock the state file to prevent multiple users from changing it at the same time
  - configure in storage backend (S3, ...)
- backup state file
  - enable versioning in storage backend
- one state file per environment
- host tf scripts in own git repo
  - collaboration
  - version control
- same procedures for infrastructure as for code
  - code review
  - testing
- execute terraform commands in ci/cd pipeline
  - avoid manual execution
  - -> single location for all changes
