import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='eu-central-1')

volumes = ec2_client.describe_volumes(
    # Filter volumes by tag Name with value prod
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'prod'
            ]
        }
    ]
)['Volumes']


def create_volume_snapshot():
    for volume in volumes:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume['VolumeId'],
            Description='Snapshot created by boto3'
        )
        print(new_snapshot)


schedule.every(20).seconds.do(create_volume_snapshot)

while True:
    schedule.run_pending()
