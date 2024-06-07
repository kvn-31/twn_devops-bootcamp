import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

new_vpc = ec2_resource.create_vpc(CidrBlock='10.0.0.0/16')
new_vpc.create_subnet(
    CidrBlock='10.0.1.0/24'
)
new_vpc.create_subnet(
    CidrBlock='10.0.2.0/24',
)
new_vpc.create_tags(
    Tags=[
        {
            'Key': 'Name',
            'Value': 'my_vpc'
        }
    ]
)
print(new_vpc.id)

all_available_vpcs = ec2_client.describe_vpcs()
vpcs = all_available_vpcs['Vpcs']

for vpc in vpcs:
    print(vpc['VpcId'])
    cird_block_assoc_sets = vpc['CidrBlockAssociationSet']
    for cird_block_assoc in cird_block_assoc_sets:
        print(cird_block_assoc['CidrBlock'])
