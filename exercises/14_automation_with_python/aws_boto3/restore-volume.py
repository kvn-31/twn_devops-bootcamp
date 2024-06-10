import boto3

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

instance_id = 'i-046af867e846bb24b'

volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [
                instance_id
            ]
        }
    ]
)['Volumes']

instance_volume = volumes[0] #we expect to only have one volume attached to the instance

snapshots = ec2_client.describe_snapshots(
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [
                instance_volume['VolumeId']
            ]
        }
    ]
)

latest_snapshot = sorted(snapshots['Snapshots'], key=lambda x: x['StartTime'], reverse=True)[0]

# create new volume from latest snapshot
new_volume = ec2_client.create_volume(
    AvailabilityZone=instance_volume['AvailabilityZone'],
    SnapshotId=latest_snapshot['SnapshotId'],
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                }
            ]
        }
    ]
)

while True:
    vol = ec2_resource.Volume(new_volume['VolumeId'])
    if vol.state == 'available':
        # attach the new volume to the instance after it is ready to be attached
        ec2_resource.Instance(instance_id).attach_volume(
            Device='/dev/xvdb', # last letter is changed
            VolumeId=new_volume['VolumeId']
        )
        break
