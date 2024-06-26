# Run Docker in Ansible

## Pre-Requisites
- aws ec2 instance
  - compared to an ubuntu droplet, aws ec2 instances have a different configuration (using amazon linux image)
  - by default python2 is installed instead of python3
  - can also be setup with terraform
    - `terraform init` & `terraform apply` in the `terraform` directory
    - we are using a hardcoded image id for now because the latest one showed troubles using yum
- create a project-vars file
  - fill in docker_password

## Ansible Playbook
The following steps are covered in this demo project:
- install and setup docker and docker-compose
- start docker containers using ansible docker community module (community.docker)

## Differences to the course
- amazon linux 2023 changed and removed python2, replaced it with python3 (see [documentation](https://docs.aws.amazon.com/linux/al2023/ug/python.html))
- -> some of the plays in the playbook are not needed anymore / need to be adapted 
