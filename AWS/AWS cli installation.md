[[AWS]] [[AWS cli commands]] [[IAM]] [[aws STS (Security Token Service)]]

# AWS cli installation

> AWS CLI v2 — install the binary, then point it at keys or SSO so `aws` talks to your account.

---

## Index

- [[#Prerequisites]]
- [[#Installation aws cli]]
- [[#Verification]]
- [[#Mental model]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Triage (when things break)]]
- [[#Related]]

## Prerequisites

…

## Installation aws cli

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version

# bash completion
sudo apt install -y bash-completion
complete -C "$(command -v aws_completer)" aws
echo 'complete -C "$(command -v aws_completer)" aws' >> ~/.bashrc

aws configure   # Access key, secret, region, output (json|table|text|yaml)
aws configure set output table
aws configure get output
```

You cannot “reveal” IAM secret keys from AWS after creation — only from Secrets Manager, SSM, or your local `~/.aws/credentials` if you stored them.

```bash
cat ~/.aws/credentials   # local only — protect this file
```

---

## Verification

```bash
# smoke test
```

## Mental model

**Say it in one breath:** CLI reads `~/.aws/credentials` + `config` (or environment/instance role), signs API calls, prints JSON/table. v2 is the current installer path on Linux.

```txt
awscliv2.zip → ./aws/install → /usr/local/bin/aws
aws configure / sso login → API calls
```

---

## Gotchas

> [!WARNING]
> **Long-lived access keys on laptops** — prefer SSO / IAM Identity Center.

> [!WARNING]
> **v1 vs v2 packages** — distro `awscli` apt may be old; use official v2 bundle.

> [!WARNING]
> **Credentials file is plaintext** — `chmod 600`; never commit.

---

## When NOT to use

- **In-instance automation with a role** — skip keys; use instance profile.
- **Complex multi-step infra** — Terraform/CDK; CLI for operations/debug.
- **Windows-only shops** — MSI install path differs (same concepts).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `aws: command not found` | PATH / install prefix | Reinstall; symlink `/usr/local/bin/aws` |
| `Unable to locate credentials` | Empty profile; wrong `AWS_PROFILE` | `aws configure`; unset bad env |
| `ExpiredToken` | SSO/session aged out | `aws sso login`; refresh assume-role |
| Wrong account actions | `get-caller-identity` | Fix profile/region; see [[AWS cli commands]] |
| Completer silent | `aws_completer` missing | Reinstall v2; fix `complete -C` |
| SSL / proxy errors | Corp proxy | `HTTP_PROXY`/`AWS_CA_BUNDLE` |

---

## Related

[[AWS cli commands]] [[IAM]] [[aws STS (Security Token Service)]] [[ARN (Amazon Resource Name)]]
