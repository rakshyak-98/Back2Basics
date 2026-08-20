[[AWS]] [[IAM]] [[aws STS (Security Token Service)]] [[ARN (Amazon Resource Name)]] [[single-sign-on (SSO)]]

# AWS CLI

> Install, authenticate, and query AWS APIs from the shell — **v2** is the current path. Prefer SSO / roles over long-lived access keys.

## Mental model

The CLI is a thin client over AWS APIs: credentials (env / profile / SSO / instance role) + region + optional `--profile` → signed request. **`aws sts get-caller-identity`** is the health check for “who am I?” Output is shaped with `--query` (JMESPath) and `--output` (`json` / `table` / `text` / `yaml`).

```
aws <service> <verb> [flags]
     │
     ├── credentials chain (env → shared file → SSO → IMDS)
     └── --region / --profile / --query / --output
```

Deep role assumption lives in [[aws STS (Security Token Service)]]; policy debug in [[IAM]].

## Standard config / commands

### Install (Linux x86_64)

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

Autocomplete:

```bash
sudo apt install -y bash-completion
complete -C "$(command -v aws_completer)" aws
echo 'complete -C "$(command -v aws_completer)" aws' >> ~/.bashrc
```

### Auth

```bash
# Prefer SSO / Identity Center for humans
aws sso login --profile prod
aws sts get-caller-identity --profile prod

# Legacy / break-glass: access keys (avoid for apps)
aws configure   # Access key, secret, region, output
aws configure set output table
aws configure get output
```

```bash
# Who am I? (account, ARN, user/role id)
aws sts get-caller-identity
aws sts get-caller-identity --query Account --output text

alias whoami-aws='aws sts get-caller-identity --query "Arn" --output text'
```

> [!INFO]
> AWS does not show secrets in console for IAM access keys after creation. Local file `~/.aws/credentials` holds keys if you used `aws configure` — treat as secrets.

### Query / output

```bash
aws ec2 describe-regions --query "Regions[].RegionName" --output text
aws iam list-users --query "Users[].UserName"
aws iam list-attached-user-policies --user-name "$USER"
aws iam list-access-keys
```

### Rotate / revoke access key

```bash
aws iam create-access-key --user-name "$USER"
# … switch to new key, then:
aws iam delete-access-key --access-key-id AKIA... --user-name "$USER"
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unable to locate credentials` | Env, `~/.aws/credentials`, SSO session | `aws sso login` or `aws configure`; check `AWS_PROFILE` |
| `ExpiredToken` | SSO / assumed-role session | Re-login; re-assume role ([[aws STS (Security Token Service)]]) |
| Wrong account / region | `get-caller-identity`; `AWS_REGION` | Fix profile/region; unset stale env vars |
| `AccessDenied` | IAM policy; SCP; wrong ARN | [[IAM]] simulate; check resource ARN |
| Paginated empty results | Default page size | Use `--max-items` / `--starting-token` or `--no-paginate` carefully |
| JMESPath returns `None` | Wrong path / casing | Test with `--output json` first |

## Gotchas

> [!WARNING]
> **Long-lived IAM user keys on laptops** — prefer SSO; keys leak into shell history and CI logs.

> [!WARNING]
> **`AWS_ACCESS_KEY_ID` in env overrides profile** — stale env vars silently use the wrong identity.

> [!WARNING]
> **CLI v1 vs v2** — install path and `aws configure` behavior differ; standardize on v2.

> [!WARNING]
> **`--cli-binary-format raw-in-base64-out`** required for many binary payloads (e.g. Lambda invoke) on newer CLI.

## When NOT to use

- **Application runtime credentials** — use SDK default chain + roles, not shelling out to `aws`.
- **Complex IaC** — Terraform / CDK for durable infra; CLI for ops and one-offs.
- **Auditing every API call** — use [[CloudTrail]], not CLI history.

## Related

[[AWS]] · [[IAM]] · [[aws STS (Security Token Service)]] · [[ARN (Amazon Resource Name)]] · [[single-sign-on (SSO)]] · [[CloudTrail]]
