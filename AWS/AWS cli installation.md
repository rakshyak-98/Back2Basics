[[AWS cli commands]] · [[IAM]] · [[aws STS (Security Token Service)]]

# AWS cli installation

> The AWS CLI is the command-line client for AWS APIs — install v2, configure credentials through profiles or environment variables, and verify with `sts get-caller-identity`.

---

## Install AWS CLI v2

### Linux (x86_64)

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip
unzip awscliv2.zip
sudo ./aws/install
aws --version   # aws-cli/2.x ...
```

### macOS

```bash
brew install awscli
```

Or download the macOS pkg from [AWS CLI install page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

### Windows

Download and run the MSI installer from AWS documentation.

## Configure credentials

Interactive:

```bash
aws configure
# AWS Access Key ID, Secret, default region, output format (json)
```

Files:

- `~/.aws/credentials` — access keys per profile
- `~/.aws/config` — region, output, role assumption

### Named profile

```bash
aws configure --profile staging
aws s3 ls --profile staging
```

### Environment variables

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...      # required for temporary credentials
export AWS_DEFAULT_REGION=us-east-1
```

Prefer **IAM roles** and `aws sso login` over long-lived keys on laptops.

## SSO (IAM Identity Center)

```bash
aws configure sso
aws sso login --profile my-sso-profile
```

## Verify

```bash
aws sts get-caller-identity
```

Returns account, ARN, and user/role ID — confirms authentication works.

## Shell completion

```bash
complete -C aws_completer aws
```

Add to `~/.bashrc` for persistent completion.

## Recall

- When is `AWS_SESSION_TOKEN` required?
- Why store profiles in `~/.aws/config` vs exporting keys in every shell?

## Sources

- [Installing or updating the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
