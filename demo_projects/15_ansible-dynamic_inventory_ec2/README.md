# Ansible Dynamic Inventory EC2

In order to avoid copying and pasting IP addresses of EC2 instances, we want to use Ansible's dynamic inventory to automatically fetch the IP addresses of EC2 instances.

To start with, 3 ec2 instances using provided Terraform configuration were created.

## Inventory File
- needs to end with `aws_ec2.yaml` (using aws_ec2 plugin)
- to test the file run `ansible-inventory --list -i aws_ec2.yaml`
- a filter for tag name was added (commented)
- a `keyed_groups` was added to group the servers by the tag name
  - this allows us to differentiate between servers with different tags
  - see the output of `ansible-inventory --graph -i aws_ec2.yaml`
```
  |--@aws_ec2:
  |  |--ec2-3-79-232-133.eu-central-1.compute.amazonaws.com
  |  |--ec2-3-64-252-215.eu-central-1.compute.amazonaws.com
  |  |--ec2-35-159-94-24.eu-central-1.compute.amazonaws.com
  |--@tag_Name_prod_server:
  |  |--ec2-3-79-232-133.eu-central-1.compute.amazonaws.com
  |--@tag_Name_dev_server:
  |  |--ec2-3-64-252-215.eu-central-1.compute.amazonaws.com
  |  |--ec2-35-159-94-24.eu-central-1.compute.amazonaws.com
```
  

## Terraform
In order to get a public IP address we needed to set `enable_dns_hostnames = true` in the vpc.
Also, for testing purposes the ec2-server names were set to be either `dev-server` or `prod-server` (hard-coded).

In contrary to the course, we are using AL2023 image as it showed a better compatibility.

## Ansible
In ansible.cfg we added the `remote_user = ec2-user` and `private_key_file = ~/.ssh/KEYFILE` to avoid specifying the user and key file.

## Helpful commands
1. Run `terraform init` to download the necessary plugins
2. Run `terraform apply` to create the EC2 instances
3. Run `ansible-inventory --list -i aws_ec2.yaml` to see the dynamic inventory

## Get it running
Run `ansible-playbook -i inventory_aws_ec2.yaml deploy-docker-new-user.yaml` to run the playbook

This will automatically take the IP addresses of the EC2 instances and run the playbook on them.
