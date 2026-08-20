[[AWS]] [[IAM]] [[KMS]] [[ARN (Amazon Resource Name)]] [[AWS Lambda]] [[AWS RDS]] [[aws STS (Security Token Service)]]

# AWS Secrets Manager

> **Secrets Manager** + **SSM Parameter Store** in one note — store secrets out of env/AMI/git; encrypt with KMS; grant decrypt via IAM (+ key policy). Rotation is Secrets Manager's differentiator.

## Mental model

| Service | Best for | Rotation |
|---------|----------|----------|
| **Secrets Manager** | DB creds, API keys; JSON secrets | Built-in Lambda rotation |
| **SSM Parameter Store** | Config + SecureString; hierarchy `/app/prod/db` | Manual / custom; cheaper |

Both use [[KMS]] for SecureString / secret encryption. Apps fetch at runtime with IAM — never bake into images.

```
App role ──► GetSecretValue / GetParameter
                  │
                  └── KMS Decrypt (key policy + IAM)
```

## Standard config / commands

### Secrets Manager

```bash
aws secretsmanager create-secret --name app/prod/db \
  --secret-string '{"username":"app","password":"..."}' \
  --kms-key-id alias/prod-secrets

aws secretsmanager get-secret-value --secret-id app/prod/db --query SecretString --output text
```

Rotation (RDS): attach rotation Lambda + enable rotation schedule; app must handle credential refresh (RDS Proxy helps).

### SSM Parameter Store

```bash
aws ssm put-parameter --name /app/prod/LOG_LEVEL --value info --type String
aws ssm put-parameter --name /app/prod/API_KEY --value '...' --type SecureString \
  --key-id alias/prod-secrets

aws ssm get-parameter --name /app/prod/API_KEY --with-decryption
aws ssm get-parameters-by-path --path /app/prod --recursive --with-decryption
```

### IAM sketch

- `secretsmanager:GetSecretValue` on secret ARN
- `ssm:GetParameter(s)` on parameter ARN
- `kms:Decrypt` on CMK (and **key policy** trusts the role)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `AccessDeniedException` GetSecretValue | IAM + resource policy; KMS | Grant role; fix key policy |
| Decryption fails | Wrong CMK; key disabled | Correct `kms-key-id`; re-enable key |
| Rotation breaks app | Old connections; cached secret | Short cache TTL; RDS Proxy IAM auth |
| Parameter not found | Path / region / account | Full name `/app/...`; right region |
| Rate exceeded | Hot GetSecretValue every request | Cache in-process with expiry; AppConfig for non-secrets |

## Gotchas

> [!WARNING]
> **Env vars in Lambda/ECS are not secret storage** — visible via GetFunctionConfiguration / task def.

> [!WARNING]
> **IAM Allow without KMS key policy** → decrypt fails ([[KMS]]).

> [!WARNING]
> **Secrets Manager pricing per secret / month** — Prefer SSM SecureString for large volumes of cheap config secrets; Secrets Manager for rotated credentials.

> [!WARNING]
> **Cross-account secret** — resource policy on secret + KMS grant; easy to miss one side.

## When NOT to use

- **Non-sensitive feature flags** — SSM String / AppConfig; don't pay Secrets Manager.
- **Password hashing for user logins** — bcrypt/Argon2 in app DB, not KMS encrypt.
- **Embedding secrets in Terraform state casually** — mark sensitive; prefer generation + SM; lock down state bucket.

## Related

[[IAM]] · [[KMS]] · [[ARN (Amazon Resource Name)]] · [[AWS Lambda]] · [[AWS RDS]] · [[aws STS (Security Token Service)]] · [[AWS]]
