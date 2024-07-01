# Deploy Docker using Ansible Roles

We are following the same goal as in [Ansible Docker](..%2F15_ansible-docker%2FREADME.md), but will create our own Ansible role to deploy Docker.

## Files
- `deploy-docker-new-user.yaml` - playbook to deploy Docker without using roles
- `deploy-docker-with-roles.yaml` - playbook to deploy Docker using a role, based on `deploy-docker-new-user.yaml`


## Roles
- `create_user`
- `start_containers`
