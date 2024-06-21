# Deploy Nexus with Ansible

Before we deployed Nexus manually by ssh into server, download the nexus binary, install and run with the created nexus user.
All those steps can be automated using Ansible.

In `nexus.sh` all the manual tasks can be found for reference.

To execute the playbook run:
```bash
ansible-playbook deploy-nexus.yaml
```
