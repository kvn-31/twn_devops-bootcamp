import boto3

ec2_client_frankfurt = boto3.client('ec2', region_name='eu-central-1')
ec2_resource_frankfurt = boto3.resource('ec2', region_name='eu-central-1')

ec2_client_paris = boto3.client('ec2', region_name='eu-west-3')
ec2_resource_paris = boto3.resource('ec2', region_name='eu-west-3')

instanceIds_frankfurt = []

reservations_frankfurt = ec2_client_frankfurt.describe_instances()['Reservations']
# in the for loop we are collecting all instance ids to be able to add tags to all of them at once
for res in reservations_frankfurt:
    for instance in res['Instances']:
        instanceIds_frankfurt.append(instance['InstanceId'])


response = ec2_resource_frankfurt.create_tags(
    Resources=instanceIds_frankfurt,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        }
    ]
)



instanceIds_paris = []

reservations_paris = ec2_client_paris.describe_instances()['Reservations']
for res in reservations_paris:
    for instance in res['Instances']:
        instanceIds_paris.append(instance['InstanceId'])

response = ec2_resource_paris.create_tags(
    Resources=instanceIds_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        }
    ]
)
