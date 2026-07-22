[[IAM]] [[ARN (Amazon Resource Name)]] [[Docker]] [[AWS EC2]]

# AWS ECR

> **Private Docker registry in AWS** — store images per region/account; IAM controls push/pull; integrates with ECS/EKS/Lambda/EC2. Not Docker Hub; not interchangeable without auth + URL change.

## Mental model

ECR holds **repositories** of **image manifests + layers** (OCI-compatible). Each region has its own registry endpoint: `{account}.dkr.ecr.{region}.amazonaws.com`. Pull/push uses **IAM** (or bot IAM user in legacy setups) + short-lived **authorization token** from `ecr:GetAuthorizationToken`.

```
docker push ──► ECR API (auth token) ──► layer upload ──► repository:tag
                                                              │
ECS/EKS/Lambda ◄── pull (execution role iam: ecr:* on repo ARN)
```

**Image scanning** (basic or enhanced) flags CVEs; **lifecycle policies** prune untagged/old images (cost control).

## Standard config / commands

### Login + push (CI or laptop)

```bash
AWS_REGION=us-east-1
ACCOUNT=123456789012
REPO=my-app

aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t $REPO:latest .
docker tag $REPO:latest $ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
docker push $ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
```

### Minimal IAM (CI push role)

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:GetAuthorizationToken"
  ],
  "Resource": "*"
},
{
  "Effect": "Allow",
  "Action": [
    "ecr:BatchCheckLayerAvailability",
    "ecr:PutImage",
    "ecr:InitiateLayerUpload",
    "ecr:UploadLayerPart",
    "ecr:CompleteLayerUpload"
  ],
  "Resource": "arn:aws:ecr:us-east-1:123456789012:repository/my-app"
}
```

### ECS/EKS pull (execution role)

- `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer` on repo ARN.
- **Same region** pull avoids cross-region data charge; replicate for multi-region DR.

### Lifecycle policy (untagged cleanup)

```json
{
  "rules": [{
    "rulePriority": 1,
    "description": "Expire untagged > 7 days",
    "selection": {
      "tagStatus": "untagged",
      "countType": "sinceImagePushed",
      "countUnit": "days",
      "countNumber": 7
    },
    "action": { "type": "expire" }
  }]
}
```

### VPC endpoint (no NAT for pull)

- Interface endpoint `com.amazonaws.region.ecr.api` + `ecr.dkr` + S3 gateway for layer storage path.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `no basic auth credentials` on push | `aws ecr get-login-password`; IAM | Login; CI role `GetAuthorizationToken` |
| `denied: repository does not exist` | Repo name/region/account in URL | Create repo; fix URI |
| ECS/EKS `CannotPullContainerError` | Execution role ECR perms; repo policy | Add ECR pull actions; private repo policy if cross-account |
| Pull works locally, fails in cluster | Cluster in private subnet without NAT/endpoint | ECR VPC endpoints |
| Image scan shows CVEs | Base image stale | Rebuild from patched base; block deploy on CRITICAL (policy) |
| Storage cost creep | Untagged manifests | Lifecycle policy; delete old tags |

## Gotchas

> [!WARNING]
> **Auth token expires in 12 hours** — CI must login each job (or use credential helper).

> [!WARNING]
> **Cross-account pull** needs **repository policy** on resource side, not only IAM on caller.

> [!WARNING]
> **Lambda container images** — max size limits; must be in **same region** as function.

> [!WARNING]
> **Tag mutability** — `MUTABLE` tags can be overwritten; prod often `IMMUTABLE` tags or digest pinning (`image@sha256:...`).

## When NOT to use

- **Public OSS images** — Docker Hub / ghcr.io unless mirroring into ECR for rate-limit/air-gap.
- **Large binary blobs unrelated to containers** — S3, not ECR.
- **Single tiny Lambda zip deploy** — container overhead may not pay off.

## Related

[[IAM]] · [[ARN (Amazon Resource Name)]] · [[Docker]] · [[AWS EC2]] · [[AWS Networking]]
