# Configuration with Ansible

## Introduction

- tool to automate IT tasks
- used for repetitive tasks that system administrators frequently execute
    - example: updating systems, backups, reboots, create users, ...
    - especially having multiple servers makes these tasks time-consuming
- benefits of using Ansible
    - can execute all tasks on own machine (remotely)
    - configuration/installation/deployment steps in a single YAML file (instead of multiple scripts and manual steps)
    - re-use same file multiple times for different environments
    - more reliable and less likely for errors
- supports multiple platforms
    - Linux, Windows, network devices, cloud providers, ...
- Ansible is agentless
    - no need to install agent on target machine
    - uses SSH to connect to target machine
    - unique advantage: no need to install anything on target machine
- Alternatives
    - Puppet, Chef (use Ruby), SaltStack
    - Ansible is easier to learn and use
    - Puppet and Chef need installations (not agentless)

### Ansible Modules

- small programs that do the actual work
- get pushed to target server, do the work, and then get removed
- one module = one small specific task (like create/copy a file, install a package, ...)
- modules listed in the [documentation](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html)

### Ansible Collections, Galaxy, and Plugins
- until version 2.9, all modules were in one big package (ansible)
- it grew too big and was split into collections -> modularized
- ansible 2.10+ uses collections
  - ansible/ansible (ansible-base) = core modules
  - modules and plugins moved into various collections
- module vs collection vs plugins
  - collection = packaging format for bundling ansible content (playbooks, roles, modules, plugins)
  - collection can be installed independently
  - all modules are part of a collection -> modules are grouped together in collections
  - plugins = extensions to ansible functionality
- community.x shows a collection from the community
- `ansible-galaxy collection list` = list all installed collections
- ansible galaxy = the main hub for collections (community)
  - similar to npm for node.js
- `ansible-galaxy collection install X` = install a collection

Create own collection
- for bigger Ansible projects with multiple playbooks, roles, and modules
- required: galaxy.yml file -> contains metadata

### Ansible Playbook

- for a complex task we will have multiple modules in a certain sequence grouped together in a playbook
- see comments in the following yaml example
```yaml
---
- name: Update web servers
  hosts: webservers # hosts attribute defines the target
  remote_user: root # user to connect to the target
  vars: #variables to use for repeated values
    state: latest

  tasks:
  - name: Ensure apache is at the {{state}} version
    ansible.builtin.yum:
      name: httpd #arguments
      state: {{ state }} #arguments

  - name: Write the apache config file
    ansible.builtin.template:
      src: /srv/httpd.j2
      dest: /etc/httpd.conf
    
    # start of second play
- name: Update db servers # name of the play, plain english describes the t ask
  hosts: databases
  remote_user: root

  tasks:
    - name: Ensure postgresql is at the latest version
      ansible.builtin.yum:
        name: postgresql
        state: latest

    - name: Ensure that postgresql is started
      ansible.builtin.service:
        name: postgresql
        state: started
```
- a play = which task should be executed on which target with which user
- multiple play can be in one playbook
- hosts attribute refers to the inventory list in the hosts file
  - groups multiple ip addresses or host names together
```
mail.example.com

[webservers]
foo.example.com
bar.example.com

[dbservers]
one.example.com
two.example.com
10.0.0.1
```

### Idempotency
- a task is idempotent if it can be run multiple times without changing the result
- most Ansible modules are idempotent

### Ansible for Docker
- normally we have a Dockerfile that produces a Docker container
- with Ansible: same configuration we can create a Docker container, a vagrant container, deploy to cloud instance or bare metal server, ...
- = allows to reproduce the app across different environments
- can also manage the host where it is running
  - -> can manage the container but also the host level

### Ansible Tower
- UI Dashboard from Red Hat
- centrally store automation tasks
- across teams with configured access
- manage inventory

## Installation
- control node = machine where Ansible is installed
- manages target servers
- windows is not supported as control node
- two ways to install Ansible
  - on the local machine
  - on a remote server
- mac: `brew install ansible`
- manjaro linux: `sudo pacman -S ansible`
- python is a dependency because Ansible is written in python -> ansible can be installed with pip

## Configuration
- connect to remote servers
  - create ansible inventory file on host machine
    - list of target servers
    - default location `/etc/ansible/hosts` (etc/ansible might need to be created)
    ```
    IP ansible_ssh_private_key_file=~/.ssh/PRIVATEKEY ansible_user=root
    IP ansible_ssh_private_key_file=~/.ssh/PRIVATEKEY ansible_user=root
    ```
  - test the connection with `ansible all -i hosts -m ping` (all = all servers, -i = inventory file, -m = module)

## Inventory
- list of target servers
- can be grouped
- ```
  [webservers]
  IP ansible_ssh_private_key_file=~/.ssh/PRIVATEKEY ansible_user=root
  IP ansible_ssh_private_key_file=~/.ssh/PRIVATEKEY ansible_user=root
  ```
- vars can be used
- ```
  [webservers]
  IP
  IP2

  [webservers:vars]
  ansible_ssh_private_key_file=~/.ssh/PRIVATEKEY
  ansible_user=root
  ```

### EC2
```
[ec2]
ec2-3-71-1-186.eu-central-1.compute.amazonaws.com
ec2-3-76-226-32.eu-central-1.compute.amazonaws.com

[ec2:vars]
ansible_ssh_private_key_file=~/Downloads/ansible.pem
ansible_user=ec2-user
ansible_python_interpreter=/usr/bin/python3.9
```

### Manage Host Key Checking & SSH Keys
- allowed servers are stored in `~/.ssh/known_hosts`
- if a server is not in the list, the connection needs a manual confirmation
- can be avoided with `/etc/ansible/ansible.cfg` file (alternative location `~/.ansible.cfg`)
  - `host_key_checking = False`
  - if the infrastructure is ephemeral (servers are created and destroyed) this is a convenient option
  - not the biggest security problem, if servers live short
  - ansible config can also be done per project
- otherwise these manual steps would need to be done
  - `ssh-keyscan IP >> ~/.ssh/known_hosts` # add the server to known_hosts
  - `ssh-copy-id -i ~/.ssh/PRIVATEKEY.pub root@IP` # copy the public key to the server

## Commands
- `ansible [all/group] -i hosts -m ping` = test connection
- `ansible IP -i hosts -m ping` = ping by ip
