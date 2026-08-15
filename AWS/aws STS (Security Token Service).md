[[IAM]] [[ARN (Amazon Resource Name)]] [[AWS EC2]] [[AWS Lambda]] [[AWS cli commands]]

# aws STS (Security Token Service)

> STS issues temporary security credentials after a principal proves it may assume a role — production AWS access should flow through STS rather than static access keys.

## Interview Relevance

STS interviews cover AssumeRole, temporary credentials, and federation — why long-lived keys are avoided.

## Sources

- [AWS STS API Reference](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html) — deep-dive
- [Temporary security credentials in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) — overview

## Technical Details

### What STS provides

STS returns **temporary credentials** (access key ID, secret access key, session token) with a defined expiration. Callers use these credentials like long-lived keys, but they expire automatically and can be scoped with session policies.

Common operations:

| API | Purpose |
|-----|---------|
| `AssumeRole` | Cross-account or same-account role assumption |
| `AssumeRoleWithWebIdentity` | OIDC/SAML federation (GitHub Actions, Google, etc.) |
| `GetSessionToken` | MFA-protected session from IAM user |
| `GetCallerIdentity` | Who am I right now? |

### AssumeRole flow

```
Principal (user, role, service)
        │
        ▼
  sts:AssumeRole  ──►  Evaluate trust policy on target role
        │
        ▼
  Temporary credentials (15 min – 12 hours typical)
        │
        ▼
  AWS API calls signed with session credentials
```

The **trust policy** on the role defines who may call `AssumeRole`. The **permission policy** on the role defines what the session may do. An optional **inline session policy** further restricts the session for that single assumption.

### Where you meet STS daily

- **EC2 instance profiles** — metadata service delivers rotating role credentials.
- **Lambda execution roles** — runtime receives temporary credentials automatically.
- **CI/CD OIDC** — pipeline assumes a deployment role without storing secrets.
- **Cross-account access** — account A's role trusts account B's principal.

### CLI example

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/CrossAccountReader \
  --role-session-name deploy-job

aws sts get-caller-identity
```

Export the returned `AccessKeyId`, `SecretAccessKey`, and `SessionToken` into the environment for subsequent CLI calls, or use `aws sts assume-role` with `--profile` and role chaining in `~/.aws/config`.

## Mistakes to Avoid

| Error | Typical cause |
|-------|----------------|
| `AccessDenied` on AssumeRole | Trust policy does not list your principal |
| `ExpiredToken` | Session exceeded `DurationSeconds` |
| `RegionDisabledException` | STS regional endpoint issue in opt-in regions |
