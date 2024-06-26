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

Helpful Modules
- register: store the output of a command
```yaml
- name: Ensure app is running
  shell: ps aux | grep node
  register: app_status
```
- debug: print a message
```yaml
- debug: msg={{ app_status.stdout_lines }} #uses app_status from register
```
- switch user
```yaml
  become: True
  become_user: nodeapp #switch to nodeapp user before executing tasks
```
- find module
```yaml
- name: Find nexus folder
  find: paths=/opt patterns=nexus-3* file_type=directory
  register: find_result
```
- blockinfile
```yaml
- name: Set run_as to nexus user
  blockinfile: # blockinfile module is used to add a block of text to a file
    path: /opt/nexus/bin/nexus.rc
    block: | # block of text
      run_as_user="nexus"
```
- lineinfile
```yaml
- name: Set run_as to nexus user
  lineinfile: #replace a line in a file
    path: /opt/nexus/bin/nexus.rc
    regexp: '^run_as_user='
    line: 'run_as_user="nexus"'
```
- pause (wait for amount of time)
```yaml
- name: Wait for nexus to start
  pause:
    minutes: 1
```
- wait_for (wait for something to happen/complete)


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
- FQCN = Fully Qualified Collection Name -> community.docker.docker_image as an example
  - for built-in modules, the collection is ansible.builtin but can be omitted because it is the default namespace
  - apt vs ansible.builtin.apt
  - it is still preferred to use the FQCN

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
  - command & shell module are not idempotent

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
- a hosts file can also be set as default in the ansible.cfg file
  - `inventory = /etc/ansible/hosts` in the `[defaults]` section of ansible config
  - normally each project has its own ansible config file

## Dynamic Expression in Strings
```yaml
    - name: Install docker-compose
      get_url:
        url: "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-{{lookup('pipe', 'uname -m')}}"
        dest: ~/.docker/cli-plugins/docker-compose
        mode: +x
```

## Jinja 2 Templating
- used in Ansible to create dynamic content
`url: "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-{{lookup('pipe', 'uname -m')}}"`

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

## Python vs Ansible
- in Python we need to check the status before executing a command
- Ansible and TF handle state checking for us
- Ansible is easier to write (Yaml)

## Registered Variables
- store the output of a command in a variable
- use the variable in a later task
- example:
```yaml
  tasks:
    - name: Create new user
      user:
        name: nodeapp
        comment: nodeapp admin
        group: admin #better practice would be do create a new group
      register: user_creation_result
    - debug: msg={{ user_creation_result }}
```

## Parameters using Variables
- dont use reserved words like `name` or `hosts` as variable names
- name should always start with a letter
- dont do things like: linux-name, linux name, linux.name or 13
- using curly braces (`- debug: msg={{ user_creation_result }}`) to use variables
- must be quoted to avoid YAML interpretation if it follows a colon -> `src: "{{ file_location }}"`
- set values for variables:
  - in the playbook
    - limitation: only for the playbook, not for the whole project which consists of multiple playbooks
```yaml
- name: Deploy nodejs app
  vars: 
  version: 1.0.0
```
- in the command line
    - `ansible-playbook -i hosts deploy-node.yaml --extra-vars "version=1.0.0"`
- external file (yaml syntax, extension can be left out)
    - vars:
    ```yaml
    version: 1.0.0
    ```
    - `ansible-playbook -i hosts deploy-node.yaml --extra-vars "@vars"` 
    - or specify the file in the playbook
    ```yaml
    - name: Deploy nodejs app
      vars_files:
        - vars
    ```
- in the inventory file
- there is a defined order in which variables are loaded -> see variable precedence


## Conditionals
- use `when` to execute a task only if a condition is met
- example:
```yaml
- name: Check if nexus folder already exists
  stat: path=/opt/nexus
  register: stat_result
- name: Rename nexus folder
  shell: mv {{ find_result.files[0].path }} /opt/nexus
  when: not stat_result.stat.exists
```

## Dynamic Inventory
- instead of manually adding servers to the inventory file, we can use a dynamic inventory
- can be used with cloud providers like AWS, Azure, ...
- this can be done using
  - dynamic inventory scripts
  - plugins (preferred)
- see the example in the demo_projects folder
- the ssh-key and user can be set in the ansible.cfg file
```
remote_user = ec2-user
private_key_file = ~/.ssh/MYKEY
```

## Password/Credentials
The following simpler ways exist:
- vars file
- use pw prompt
```yaml
  vars_prompt:
    - name: docker_password
      prompt: "Enter your docker password"
      private: yes
```

## Terraform and Ansible
- Terraform can be used to create the infrastructure and then use Ansible to configure it
- see the example in the demo_projects folder
```tf
resource "aws_instance" "myapp-server" {
  # ...
}

resource "null_resource" "configure_server" {
  # whenever the myapp-server instance is created, this null resource will be triggered
  triggers = {
    instance_id = aws_instance.myapp-server.public_ip
  }
  # execute the ansible command on the local machine
  provisioner "local-exec" {
    working_dir = "PATH"
    command     = "ansible-playbook --inventory ${aws_instance.myapp-server.public_ip}, --private-key ${var.private_key_location} --user ec2-user deploy-docker-new-user.yaml"
  }
}
```

## Ansible and K8s
- Automate deployment into K8s clusters
- example setup
  - use terraform to spin up the K8s cluster (in AWS)
  - use Ansible to connect to the K8s cluster and deploy the app
- kubernetes.core.k8s module can be used
  - basically as both share YAML syntax, the same content can be used for k8s and Ansible
- a simple example
```yaml
---
- name: Deploy application in new namespace
  hosts: localhost # executing locally, connecting to remote cluster
  tasks:
    - name: Create a k8s namespace
      kubernetes.core.k8s:
#        kubeconfig: ... by default it will use ~/.kube/config, which is the default location for kubeconfig
        name: my-app
        api_version: v1
        kind: Namespace
        state: present
```

## Python and Ansible Modules
- Ansible modules are written in Python
- often, dependencies need to be installed
- the best way to achieve this (especially on Linux) is to use a virtual environment
```bash
python3 -m venv .venv #creates a virtual environment
source .venv/bin/activate #activates the virtual environment
# pip3 install ...
```
- to assure ansible is using the right (local) python interpreter, the following command can be used
```bash
ansible-playbook deploy-docker-new-user.yaml --extra-vars "ansible_python_interpreter=/path/to/python"
```
- this can also be done using vars in the playbook
```yaml
  vars:
    ansible_python_interpreter: ./.venv/bin/python
```
- or in the inventory file

## Ansible in Jenkins Pipeline
- before: for each tool we wanted to execute in the pipeline we had to install the tool on the Jenkins server / container
- for Ansible: we use a dedicated server for Ansible (common practice)
- in short, the steps were:
  - create droplet for jenkins
  - create droplet for ansible
    - install ansible on server OR do it in jenkins pipeline
  - create two ec2 instances (which will then be modified using ansible)
  - store keys for ec2 instances and for ansible server in jenkins
  - in jenkinsfile:
    - copy ansible files and the key for the ec2 instances to the ansible server
    - execute ansible playbook on the ansible server
- see Java-Maven-App project feature/ansible for more details (such as Jenkinsfile)

## Ansible Roles
- a way to organize playbooks, especially when they get bigger
- group content in roles
- to easily reuse and share with others
- break up playbooks into smaller parts
- a role: ~ a package for tasks
- multiple plays can then use the role
- a role consists of
  - tasks
  - static files
  - vars -> parameterize the role, default vars can be overwritten
  - custom modules
- standard file structure, easy to maintain and reuse
  - see [documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)
- there are also community roles, can be found on ansible galaxy and git repositories
- example of Ansible yaml
```yaml
- name: Create new linux user
  hosts: all
  become: yes
  roles:
    - role: create_user #ansible automatically looks for a role with this name in roles directory
```
- role: (main.yaml sits in roles/create_user/tasks)
```yaml
- name: Create new linux user
  user:
    name: new-user
    groups: adm,docker
```

### Files in Roles
- need to be located in roles/ROLENAME/files
- can be referenced in main.yaml of role
```yaml
- name: Copy docker compose file
  ansible.builtin.copy:
    src: docker-compose.yaml #ansible will look for this file in the files directory of the role -> roles/ROLENAME/files
    dest: /home/new-user/docker-compose.yaml
```

### Variables in Roles
- in roles/ROLENAME/vars/main.yaml
- there is a defined order in which variables are loaded -> see variable precedence
- values provided by the command line are the highest priority, but second is already the defined variable in the role

### Defaults in Roles
- in roles/ROLENAME/defaults/main.yaml
- these are the default values for the variables, can be overwritten by vars

## Commands
- `ansible [all/group] -i hosts -m ping` = test connection
- `ansible IP -i hosts -m ping` = ping by ip
- `ansible-playbook -i hosts playbook.yaml` = run playbook
- `ansible-playbook playbook.yaml -vv` = verbose output
- `ansible-playbook -i inventory_aws_ec2.yaml deploy-docker-new-user.yaml` = run playbook with dynamic inventory
- `ansible-inventory -i inventory_aws_ec2.yaml --graph` = show inventory graph
