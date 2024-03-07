# 09 - AWS Services

- post widely used cloud platform
- relevant services for us
    - ec2
    - s3 storage service
    - databases
    - vpc (firewall, network config)
    - IAM (identity service)
    - containers (elastic container service, ..)

## Scopes in AWS
- global scope (AWS Account, IAM users)
    - IAM
    - billing
    - Route53
- region scope
    - s3 buckets
    - vpc
    - dynamoDB
- az scopes
    - EC2
    - EBS
    - RDS

## IAM
- Identity and Access Management
- who is allowed to access services/resources
- create users / user groups
- Root user automatically created, used for billing etc, but better practice to create an admin user with less priviliges
- system users: f.e. for Jenkins
- arn = amazon resource identifier -> is another unique identifier

### IAM users vs Roles
- roles are useful between services
- users are assigned to human/system users
- a service also can have permissions and perform actions such as (EC2 management); policies cannot be assigned to aws services directly -> Instead service role is assigned and policies are assigned to the role
- role for each service -> policies specific for service
- role:
    - 1. assign role to aws service
    - 2. attach policies to that role
    

Policy = Group of permissions


## Create Admin user
- admin can have access to only UI or UI and console
- access to ui via email pw, to cli via access key
- for normal users: best practice to assign to group and attach policies to group; for admin, this can be left out
- policies we used
    - AdministratorAccess
    - //AdministratorAccess-Amplify
- login in ui with user -> security credentials -> create access key -> CLI

## Regions & Availability Zones
- AWS has mulitple data centers in each region -> to replicate data
- applications should be hosted nearest to end users or distributed to different regions

## Virtual Private Cloud (VPC)
- in each region vpc is created for a service (f.e EC2)
- vpc = own private network in the cloud for each specific region
- vpc spans all AZs (subnets) in that region
- virtual representation of physical network infrastructure
- subnet -> subnetworks of the vpc -> individually available zone -> private network inside a network
    - private subnet -> when you block all internet communication from outside in a subnet; other applications inside the VPC can access; f.e.: Database
    - public subnet -> allow external traffic (ports opened); f.e.: actual application endpoint
- each VPC has internal ip range -> can be changed (not for outside web traffic)
- vpc can then assign a public ip address pointing to an internal ip
- internet gateway: connects vpc to outside internet
- which ports are open to internet can be defined per subnet by NACLs (network access control lists)
- to configure access on instance level -> Security Group

## CIDR (classless Inter-Domain Routing)

- = range of ip addresses
- ip address in binary = 32 binary digits
- netmask = how many of those digits should be fixed
- the lower the number, the more ip addresses are in the ip range


Useful Links:

- IP Calculator: https://mxtoolbox.com/subnetcalculator.aspx
- IP Calculator with binary values: http://jodies.de/ipcalc
- Calculate sub-CIDR blocks: http://www.davidc.net/sites/default/subnets/subnets.html 

## Elastic Compute Cloud (EC2)

- virtual server

### Launch new EC2 instance

- make sure right region is selected
- click launch instance
- use parameters as required
- key pair: create in aws
- make sure to add security group (and prevent all ip addresses/ports from having access)

### Setup a new key pair
- after added in aws (f.e. launch ec 2 instance) a download of .pem was made
- this file needs to be used to ssh folder
- change access rights to chmod 400 .ssh/docker-server.pem -> only our user is allowed to read
- ssh -i .ssh/docker-server.pem ec2-user@IP -> ec2-user is the user created by default

### Install Docker on EC2 instance (with Amazon Linux)
- sudo yum update
- sudo yum install docker
- start docker daemon: sudo service docker start
- adding our user to docker group sudo usermod -aG docker $USER
- login & logout using exit
- groups -> should now show docker group
- now docker commands can be executed without sudo

### Open Port (inbound)
- navigate to security group
- add custom tcp with port

## Deploy to AWS using Jenkins (simple application)
- connect to EC2 server using ssh agent
- execute docker run on ec2 instance

### Jenkins Part:
- install ssh agent plugin
- create multi branch pipeline
- add credentials scoped to pipeline
    - add SSH username with priv key
    - add contents of the aws .pem file
- use credentials to connect via ssh agent in Jenkinsfile, but first allow jenkins ip in aws
- in Jenkinsfile: pull the image and do docker run
```
sshagent(['ec2-server-key']) {
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@IP ${dockerCmd}"
}
```
### AWS Part
- allow ssh inbound with jenkins ip
- also make sure the applicaiton is accessible


## Deploy to AWS using Jenkins and Docker compose

- Install docker compose on EC2 instance
- Adjust Jenkinsfile to execute docker-compose

### Install Docker compose

one examplary way: 

- sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose

see this guide: https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9

### Jenkins Part

We are simply copying and running the docker compose to our instance using scp

```
script {
                    echo 'deploying docker image to EC2...'
                    def dockerComposeCmd = "docker-compose -f docker-compose.yaml up --detach"
                    sshagent(['ec2-server-key']) {
                        // do a secure copy via ssh to server of docker compose
                        sh "scp docker-compose.yaml ec2-user@3.79.18.159:/home/ec2-user"
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@IP ${dockerComposeCmd}"
                    }
                }
```

### Better way using shell script
If we have multiple commands to execute it is better practice to use a shell script

```
script {
                    echo 'deploying docker image to EC2...'
                    def shellCmd = "bash ./server-cmds.sh"
                    sshagent(['ec2-server-key']) {
                        sh "scp docker-compose.yaml ec2-user@3.79.18.159:/home/ec2-user"
                        sh "scp server-cmds.sh ec2-user@3.79.18.159:/home/ec2-user"
                        sh "ssh -o StrictHostKeyChecking=no ec2-user@3.79.18.159 ${shellCmd}"
                    }
                }
```

### Use dynamic image name / version

- in docker compose use image variable: image: ${IMAGE}
- docker compose is executed by shell script, so we need to set the variable there
- in shell script: export IMAGE=$1
- in jenkins file we need to define the parameter for the shell script, passing the image name: def shellCmd = "bash ./server-cmds.sh ${IMAGE_NAME}"


## AWS - CLI
- for programmatic access
- reproducibility, faster, easier

### AWS CLI Setup
- prerequisite: admin user (as written in IAM section above)
- use aws configure (see below)
- after setup the information is stored in ~/.aws/ -> config, credentials

### AWS Cli change user
various ways to achieve this:
- use aws configure set aws_access_key_id VALUE aws_secret_access_key VALUE -> will change default aws user for all commands
- using env variables (temporarily):
    - export AWS_ACCESS_KEY=VALUE
    - export AWS_SECRET_ACCESS_KEY=VALUE
    - optional: export AWS_DEFAULT_REGION=VALUE
    - now that the environment variables are set, aws cli uses them
    - those changes are only used in the current terminal and not set permanently


### AWS CLI Commands
- every service has subset of commands
- structure: aws <command (service)> <subcommand> [options, params]

#### AWS Configure
 
```sh
aws configure
aws configure set aws_access_key_id  "YOUR_ACCESS_KEY_ID"
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY= "YOUR_SECRET_ACCESS_KEY"
```


#### AWS EC2 Service

```sh
aws ec2 help
aws ec2 describe-security-groups --group-ids "YOUR_GROUP_ID"
aws ec2 describe-vpcs
aws ec2 create-security-group --group-name "YOUR_GROUP_NAME" --description "ENTER_DESCRIPTION" --vpc-id "YOUR_VPC_ID"
aws ec2 describe-subnets
aws ec2 describe-instances
aws ec2 describe-instances --filters Name="ENTER_FILTER_NAME",Values="ENTER_VALUE" --query "Reservations[].Instances[].InstanceId"
aws ec2 run-instances --image-id "YOUR_AMI_ID" --count "ENTER_NUMBER" --instance-type "YOUR_INSTANCE_TYPE" --key-name "YOUR_KEY_NAME" --security-group-ids "YOUR_SECURITY_GROUP_ID" --subnet-id "YOUR_SUBNET_ID"
aws ec2 authorize-security-group-ingress --group-id "YOUR_GROUP_ID" --protocol "ENTER_PROTOCOL" --port "YOUR_PORT_NUMBER" --cidr "YOUR_CIDR_BLOCK"
aws ec2 create-key-pair --key-name "YOUR_KEY_NAME" --query "ENTER_QUERY" --output text > "YOUR_PEM_FILE"
```

#### AWS IAM Service
  
```sh
aws iam help
aws iam create-group --group-name "YOUR_GROUP_NAME"
aws iam create-user --user-name "YOUR_USER_NAME"
aws iam add-user-to-group --user-name "YOUR_USER_NAME" --group-name "YOUR_GROUP_NAME"
aws iam get-group --group-name "YOUR_GROUP_NAME"
aws iam attach-user-policy --user-name "YOUR_USER_NAME" --policy-arn "YOUR_POLICY_ARN"
aws iam list-policies --query `Policies[?PolicyName=="`YOUR_POLICY_NAME`"].Arn` --output text
aws iam attach-group-policy --group-name "YOUR_GROUP_NAME" --policy-arn "YOUR_POLICY_ARN"
aws iam list-attached-group-policies --group-name "YOUR_GROUP_NAME"
aws iam create-login-profile --user-name "YOUR_USER_NAME" --password "YOUR_PASSWORD" --password-reset-required
aws iam get-user --user-name "YOUR_USER_NAME"
aws iam create-policy --policy-name "YOUR_POLICY_NAME" --policy-document "YOUR_FILE_NAME"
aws iam create-access-key --user-name "YOUR_USER_NAME"
```

#### Filter & Query
- using --filter -> filter for a filter and value; only return elements that match the criteria
- --query -> only return the information (f.e. an instanceId) specified
```sh
aws ec2 describe-instances --filters Name="ENTER_FILTER_NAME",Values="ENTER_VALUE" --query "Reservations[].Instances[].InstanceId"
```

## AWS & Terraform
- running all those commands manually is not an ideal solution
- -> automation tools (= Infrastrcute as Code) such as terraform provide
    - consistency & reproducibility
    - automation & speed
    - history

