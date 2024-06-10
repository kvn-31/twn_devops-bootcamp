# Automation with Python
- doing repetitive tasks manually is waste of time
- python can automate these tasks
- can also provision infrastructure

## Boto3
- AWS SDK for Python
- see [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Setup
- `pip install boto3`
- connect to aws account
  - setup aws cli -> if already done boto3 will take this information from the cli

### Use different region without changing cli
- create a client using a named parameter
```python
import boto3

es2_client = boto3.client('ec2', region_name='us-west-1')
all_available_vpcs = es2_client.describe_vpcs()

```

### Use created resource to interact with it
- in comparison to terraform we do not need to specify ids etc, but we can use the returned object
```python
new_vpc = ec2_resource.create_vpc(CidrBlock='10.0.0.0/16') # returns a whole vpc object which can be used to interact with it
new_vpc.create_subnet(
  CidrBlock='10.0.1.0/24'
)
new_vpc.create_subnet(
  CidrBlock='10.0.2.0/24',
)
```

## Terraform vs Boto3 with Python
- terraform manages state of infrastructure
  - knows the current state
  - knows differences between desired and current state
  - is idempotent -> multiple executions of same config file will always result in same end result
  - declare the end result
- boto3 with python is a low level way to interact with aws
  - python has no state
  - write code for actions
  - more low level
  - gives more control
  - more complex logic can be implemented
  - python allows to do more than just infrastructure provisioning

## Scheduled Tasks
- popular schedular library is `schedule`
