# Terraform - Provision EC2 using Provisioners

We automate the following tasks using Terraform:
- Create a VPC
- Create a subnet
- Create Route Table & Internet Gateway
- Provision an EC2 instance
- Install Docker and deploy nginx container
- Create a security group

The main goal of this project is to learn how to use Terraform with the example of an AWS project. To achieve this we utilized:
- various resources such as VPC, subnet, route table, internet gateway, EC2 instance, security group
- variables for data that is user specific, might change or should not be hard coded
- output to display the public IP of the EC2 instance
- data source to get the latest Amazon Linux 2 AMI image id
- the only difference to [12_terraform-provision-ec2.md](..%2F12_terraform-provision-ec2%2FREADME.md) is that provisioners are used to start the sh script instead of user data.


On creation the EC2 instance automatically executes the user data script. The script is used to install and start docker with a nginx image.

By creating the VPC, AWS automatically created a route table for us. The route table decides where the traffic will be forwarded in the VPC.

