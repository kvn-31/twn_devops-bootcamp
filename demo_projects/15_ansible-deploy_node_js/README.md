# Deploy Node Js app with Ansible

In this small demo project we will deploy a simple nodejs application to a server using Ansible.

## Pre-requisites
- droplet / server
- packed node.js application (tar.gz)

## Ansible Playbook
This project contains an anisble playbook that covers the following steps:
- install node.js & npm on server
- copy an artifact and unpack
- start the application
- confirm the application is running

The playbook is executed with the `ansible-playbook` command.

```bash
ansible-playbook -i hosts deploy-node.yaml
```
