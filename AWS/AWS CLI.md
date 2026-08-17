[[AWS CLI]] [[AWS CLI installation]] [[INDEX]]

# AWS CLI

> AWS CLI v2 — identity, EC2, S3, Lambda, and operational flags.

---

## Commands

### Global flags

From [[AWS CLI]].

```bash
aws <service> <operation> \
  --region us-east-1 \
  --profile production \
  --output table \
  --query 'Reservations[].Instances[].InstanceId'
```

### Identity

From [[AWS CLI]].

```bash
aws sts get-caller-identity
aws iam list-users
aws iam list-attached-role-policies --role-name AppRole
```

### EC2

From [[AWS CLI]].

```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 start-instances --instance-ids i-0abc
aws ec2 describe-security-groups --group-ids sg-0abc
```

### S3

From [[AWS CLI]].

```bash
aws s3 ls s3://my-bucket/
aws s3 cp ./local.txt s3://my-bucket/path/
aws s3 sync ./dist s3://my-bucket/ --delete
```

### Lambda

From [[AWS CLI]].

```bash
aws lambda list-functions
aws lambda invoke --function-name hello --payload '{}' out.json
aws logs tail /aws/lambda/hello --follow
```

### ECR

From [[AWS CLI]].

```bash
aws ecr describe-repositories
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
```

### Route 53

From [[AWS CLI]].

```bash
aws route53 list-hosted-zones
aws route53 list-resource-record-sets --hosted-zone-id Z1234567890ABC
```

### CloudFormation / IaC adjacency

From [[AWS CLI]].

```bash
aws cloudformation deploy --template-file template.yaml --stack-name my-stack --capabilities CAPABILITY_IAM
```

### Pagination

From [[AWS CLI]].

```bash
aws ec2 describe-instances --max-items 10 --starting-token <token>
```

### Help discovery

From [[AWS CLI]].

```bash
aws ec2 help
aws ec2 run-instances help
```


## Installation & configure

### Linux (x86_64)

From [[AWS CLI installation]].

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip awscliv2.zip
sudo ./aws/install
aws --version   # aws-cli/2.x ...
```

### macOS

From [[AWS CLI installation]].

```bash
brew install awscli
```

### Named profile

From [[AWS CLI installation]].

```bash
aws configure --profile staging
aws s3 ls --profile staging
```

### Environment variables

From [[AWS CLI installation]].

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...      # required for temporary credentials
export AWS_DEFAULT_REGION=us-east-1
```

```bash
aws configure sso
aws sso login --profile my-sso-profile
```

```bash
aws sts get-caller-identity
```

```bash
complete -C aws_completer aws
```
