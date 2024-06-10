import boto3
from operator import itemgetter

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


# for every volume we will only keep the latest 2 snapshots, delete the rest
for volume in volumes:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=[
            'self'
        ],
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [
                    volume['VolumeId']
                ]
            }
        ]
    )['Snapshots']

    # sort the list by date
    snapshots_sorted_by_date = sorted(snapshots, key=itemgetter('StartTime'), reverse=True)

    # keep the first 2 snapshots
    for snap in snapshots_sorted_by_date[2:]:
        #delete snapshot
        response = ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print(response)
