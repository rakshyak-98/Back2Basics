
```bash
aws configure
aws sts get-caller-identity
aws sts get-caller-identity --query Account --output text; # get only specific fields
```

```bash
aws iam delete-access-key --access-key-id <access key id>;
```

### Query
```shell
aws ec2 describe-regions --query "Regions[].RegionName";
```

### IAM

```bash
aws iam list-users;
aws iam list-users --query "Users[].UserName";
aws iam list-attached-user-policies --user-name <your-username>; 
```

```bash
aws iam get-user
aws iam list-access-keys
aws iam create-access-key

```

#### STS (security Token Service)

```bash
alias whoami-aws='aws sts get-caller-identity --query "Arn" --output text'
```

> [!INFO]
> STS -> service tells you which AWS account you are connected to, which IAM user or role you are currently using, if you credentials are valid and not expired.

- providers temporary security credentials for users and applications to access aws securely access AWS services without needing long-term IAM credentials.
- temporary access keys, secret keys, and session tokens. Automatically expire after a set time (default: 1 hour, can be extended up to 12 hours).
- supports [[single-sign-on (SSO)]] and third party identity providers.

> [!INFO] STS is more secure than Long-Term Credentials
> - no need to store permanent IAM user credentials.
> - Automatically expires, reducing security risks.

```shell
aws sts get-caller-identity;
```
- returns your user id, account id, ARN (useful for debugging permissions).
