# Ansible and Terraform

This project is an extension to [Ansible-docker](..%2F15_ansible-docker%2FREADME.md).
In the main.tf we are executing the ansible commands using the `local-exec` provisioner. This can lead to timing issues and is not always recommended. To avoid the problem that  the ec2 server is not ready, yet we added a play in Ansible that waits for the server to be ready.

This also means we do not need the hosts file in the ansible directory anymore as we are passing the ip address of the freshly created instance to the ansible-playbook command.
Also, the hosts attribute is set to all in the playbook file for simplification.

Variables that needed to be passed to the ansible-playbook command are added to terraform.tfvars file.

## Steps to execute the project
`terraform init` - to initialize the terraform directory
`terraform apply` - to create the instance -> this will automatically run the ansible playbook

