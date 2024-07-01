# Terraform - Provision EC2

This folder contains a Terraform module that can be used to provision an EC2 instance on AWS.

It is slightly different from [Terraform - Provision EC2](..%2F..%2F12_terraform-provision-ec2%2FREADME.md)

The main difference: we are not using user_data to install docker and docker-compose. Instead, later we are using Ansible to install docker and docker-compose.

To use it, change the following variables in `variables.tf`:
- my_ip: set to your IP address
- avail_zone: set to the availability zone you want to use
- public_key_location: set to the location of your public key

Run the following commands to create an EC2 instance:
```bash
terraform init
terraform apply
```
