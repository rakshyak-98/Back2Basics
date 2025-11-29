
```bash
aws configure
aws sts get-caller-identity
```

```bash
aws iam list-access-keys
aws iam create-access-key

aws configure
```

```bash
aws iam delete-access-key --access-key-id <access key id>;
```

### Query
```shell
aws ec2 describe-regions --query "Regions[].RegionName";
```

### User
```
aws sts get-caller-identity; # check which user logged in with.
aws iam list-attached-user-policies --user-name <your-username>; 
aws iam list-users;
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
