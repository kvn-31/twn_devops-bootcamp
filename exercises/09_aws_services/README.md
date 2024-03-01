This folder contains a base for a react and nodejs application that was used to learn AWS services.
Below, a changePwdPolicy.json file is used to set a password policy for the IAM users. It was used to test the AWS CLI.

To use the changePwdPolicy.json, insert the AWS account number

```
"Resource": "arn:aws:iam::<account-number>:user/${aws:username}"
```
