# Boto3

The purpose of this project is to learn some basic functionality of boto3 in python.

- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

The following tasks are performed in this project:
- create a new vpc with subnets in `main.py`
- ec2 status check in `ec2_status.py` (pre-requisite: create ec2 instances, for example using terraform)
  - uses `schedule` to run the check regularly
- add env tags to ec2 instances in `ec2_tags.py` (pre-requisite: create ec2 instances, for example using terraform)
- eks cluster info in `eks_info.py` (pre-requisite: create eks cluster, for example using terraform)
- EC2 Volume Backup and Restoration with Python
  - Every ec2 instance has its own volume. This project demonstrates how to create a snapshot of the volume and how to restore the volume from the snapshot.
  - Pre-requisites: create two ec2 instances (one with name dev one with name prod, can be done manually)
  - add same tags to the volumes
  - Goals: 
    - automatically go through all instances and create a snapshot of the volume
    - go through all snapshots per volume and only keep the latest 2
