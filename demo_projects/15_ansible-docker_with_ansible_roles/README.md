# Deploy Docker using Ansible Roles

We are following the same goal as in [Ansible Docker](..%2F15_ansible-docker%2FREADME.md), but will create our own Ansible role to deploy Docker.

This project combines the knowledge of the previous projects:
- using a dynamic inventory
- creating EC2 instance using Terraform

To run the ansible script using the dynamic inventory run `ansible-playbook -i inventory_aws_ec2.yaml deploy-docker-with-roles.yaml`.
To test if the inventory is working use `ansible-inventory --graph -i inventory_aws_ec2.yaml`

See roles/start_containers for a simple example of a role using
- defaults
- files
- tasks
- vars

## Files
- `deploy-docker-new-user.yaml` - playbook to deploy Docker without using roles
- `deploy-docker-with-roles.yaml` - playbook to deploy Docker using a role, based on `deploy-docker-new-user.yaml`


## Roles
- `create_user`
- `start_containers`
