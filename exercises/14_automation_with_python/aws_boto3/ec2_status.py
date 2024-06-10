import boto3

ec2_client = boto3.client('ec2', region_name='eu-west-3')
ec2_resource = boto3.resource('ec2', region_name='eu-west-3')

# commented as not needed anymore, was just used to demonstrate the describe_instances method
# instances = ec2_client.describe_instances()
# for reservation in instances['Reservations']:
#     for instance in reservation['Instances']:
#         print(f"Status of instance {instance['InstanceId']} is {instance['State']['Name']}")

statuses = ec2_client.describe_instance_status()
for status in statuses['InstanceStatuses']:
    ins_status = status['InstanceStatus']['Status']
    sys_status = status['SystemStatus']['Status']
    state = status['InstanceState']['Name']
    print(f"Instance {status['InstanceId']} is {state} with Instance status: {ins_status}, System status: {sys_status}")
