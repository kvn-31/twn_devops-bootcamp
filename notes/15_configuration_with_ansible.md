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


