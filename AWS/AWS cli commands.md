[[AWS]] [[AWS cli installation]] [[IAM]] [[aws STS (Security Token Service)]] [[AWS EC2]]

# AWS cli commands

> AWS CLI — signed HTTP to AWS APIs; start with “who am I?”, then IAM/EC2 queries with `--query`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Every command is an API call under a principal (user/role). `sts get-caller-identity` is the stethoscope. JMESPath `--query` slices JSON.

```txt
aws <service> <operation> [--profile] [--region] [--query] [--output]
```

---

## Standard config / commands

```bash
aws configure
aws sts get-caller-identity
aws sts get-caller-identity --query Account --output text
alias whoami-aws='aws sts get-caller-identity --query Arn --output text'

# IAM
aws iam get-user
aws iam list-users --query 'Users[].UserName'
aws iam list-access-keys
aws iam create-access-key
aws iam delete-access-key --access-key-id AKIA…
aws iam list-attached-user-policies --user-name alice

# EC2 / regions
aws ec2 describe-regions --query 'Regions[].RegionName'
aws ec2 describe-instances --filters Name=instance-state-name,Values=running
```

| Knob | Why it matters |
|------|----------------|
| `--profile` | Multi-account / SSO profiles |
| `--region` | Many resources are regional |
| `--query` | Avoid piping giant JSON to `jq` for simple fields |
| STS session | Temp creds beat long-lived keys ([[aws STS (Security Token Service)]]) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDenied` | Identity + policy + SCP | `get-caller-identity`; fix IAM/resource policy |
| Empty describe | Wrong region | Set `--region` / config |
| `InvalidClientTokenId` | Bad/deleted key | Rotate key; fix profile |
| SSO mystery failures | Token cache | `aws sso login --profile …` |
| `--query` returns `None` | Wrong JMESPath | Test without query; fix path |
| Pager hangs | `less` on big output | `--no-cli-pager` or `AWS_PAGER=""` |

---

## Gotchas

> [!WARNING]
> **Global vs regional services** — IAM is global; EC2 is not. Always know which.

> [!WARNING]
> **`--output text` flattens** — fine for scripts; use `json` when nesting matters.

> [!WARNING]
> **Deleting access keys** — confirm `list-access-keys` so you don’t brick automation.

---

## When NOT to use

- **Declarative infra at scale** — Terraform/CloudFormation.
- **App runtime AWS access** — SDK + role, not shelling out to CLI.
- **Audited break-glass only** — still log; prefer SSO short sessions.

---

## Related

[[AWS cli installation]] [[IAM]] [[aws STS (Security Token Service)]] [[ARN (Amazon Resource Name)]] [[AWS EC2]]
