# Ansible Dynamic Inventory EC2

In order to avoid copying and pasting IP addresses of EC2 instances, we want to use Ansible's dynamic inventory to automatically fetch the IP addresses of EC2 instances.

To start with, 3 ec2 instances using provided Terraform configuration were created.

## Ansible Playbook

## Inventory File
- needs to end with `aws_ec2.yaml` (using aws_ec2 plugin)
