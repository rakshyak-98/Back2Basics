[[AWS cli installation]] · [[IAM]] · [[AWS EC2]] · [[AWS ECR]] · [[Route53]]

# AWS cli commands

> The AWS CLI maps almost every AWS API to `aws <service> <operation>` — combine `--query`, `--output`, and JMESPath filters to script infrastructure without clicking the console.

---

## Global flags

```bash
aws <service> <operation> \
  --region us-east-1 \
  --profile production \
  --output table \
  --query 'Reservations[].Instances[].InstanceId'
```

| Flag | Use |
|------|-----|
| `--region` | Override default region |
| `--profile` | Named credential profile |
| `--output` | `json`, `table`, `text`, `yaml` |
| `--query` | JMESPath filter on response |
| `--dry-run` | Where supported, validate without applying |

## Identity

```bash
aws sts get-caller-identity
aws iam list-users
aws iam list-attached-role-policies --role-name AppRole
```

## EC2

```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"
aws ec2 start-instances --instance-ids i-0abc
aws ec2 describe-security-groups --group-ids sg-0abc
```

## S3

```bash
aws s3 ls s3://my-bucket/
aws s3 cp ./local.txt s3://my-bucket/path/
aws s3 sync ./dist s3://my-bucket/ --delete
```

## Lambda

```bash
aws lambda list-functions
aws lambda invoke --function-name hello --payload '{}' out.json
aws logs tail /aws/lambda/hello --follow
```

## ECR

```bash
aws ecr describe-repositories
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
```

## Route 53

```bash
aws route53 list-hosted-zones
aws route53 list-resource-record-sets --hosted-zone-id Z1234567890ABC
```

## CloudFormation / IaC adjacency

```bash
aws cloudformation deploy --template-file template.yaml --stack-name my-stack --capabilities CAPABILITY_IAM
```

Many teams prefer Terraform; CLI remains essential for ad hoc operations and CI scripts.

## Pagination

Large lists auto-paginate with `--no-paginate` to disable, or use:

```bash
aws ec2 describe-instances --max-items 10 --starting-token <token>
```

## Help discovery

```bash
aws ec2 help
aws ec2 run-instances help
```

## Recall

- How do you filter `describe-instances` to running instances in one AZ?
- What command confirms which account your credentials belong to?

## Sources

- [AWS CLI Command Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html)
- [Using the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
